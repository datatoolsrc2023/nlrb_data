#!/usr/bin/env python3

from common import db_config, sql

import allegations as alleg

if db_config.db_type == 'sqlite':
    import sqlite3


def main():
    """Run the migration."""

    allegations_query = """
    SELECT c.id, case_number, allegations_raw, allegations_parse_error
    FROM cases c
    INNER JOIN error_log e
    ON c.id = e.case_id
    WHERE allegations_raw IS NOT NULL
    AND allegations_raw <> ''
    AND allegations_parse_error IS NULL
    OR allegations_parse_error = true
    ;
    """

    # if code and description are both null in allegations table,
    # then there was an error parsing the raw allegations text
    error_log_query = """
    UPDATE error_log
    SET allegations_parse_error = CASE WHEN code is null and description is null THEN true
                                       WHEN code is not null and description is not null then false
                                       ELSE null
                                       END
    FROM allegations
    WHERE error_log.case_id = allegations.case_id
    ;
    """

    try:
        with sql.db_cnx() as cnx:

            # get allegations to process,
            # process allegations,
            # then update error_log table
            # in one transaction so if any of these steps
            # fail, the entire transaction is rolled back
            # and the allegations and error_log tables don't
            # get out of sync
            if db_config.db_type == 'sqlite':
                cnx.row_factory = sqlite3.Row

            c = cnx.cursor()

            # get allegations to process
            c.execute(allegations_query)

            # process allegations
            if db_config.db_type == 'sqlite':
                # sqlite3 doesn't make a rowcount attribute available
                # so to get the row count, we have to fetch all rows and
                # get the len() of the result
                result = c.fetchall()
                n = len(result)
            elif db_config.db_type == 'postgresql':
                # getting the postgresql rowcount attribute is
                # less memory intensive than fetching all rows
                result = c
                n = c.rowcount

            print(f'Cases with allegations: {n}')

            print(f'Processing allegations...')
            for row in result:
                alleg.process_allegations(cnx.cursor(), row)
            
            # update error_log col of allegations_parse_error table
            print(f'Attempting to update {db_config.error_log} table...')
            c.execute(error_log_query)

    except Exception as e:
        print(f'Unable to process allegations or update {db_config.error_log} table')
        raise e
    else: # no exception
        print(f'Processed allegations and updated {db_config.allegations} table')
        print(f'Updated {db_config.error_log} table')
    finally:
        c.close()
        cnx.close()


if __name__ == '__main__':
    main()
