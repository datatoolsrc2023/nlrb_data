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
    ;
    """

    error_log_query = """
    UPDATE error_log e
    SET allegations_parse_error = parse_error
    FROM allegations a
    WHERE e.case_id = a.case_id
    ;
    """

    try:
        with sql.db_cnx() as cnx:
            if db_config.db_type == 'sqlite':
                cnx.row_factory = sqlite3.Row
            c = cnx.cursor()
            c.execute(allegations_query)
    except Exception as e:
        print(f'Error: {e}')
    else: # no exception
        if db_config.db_type == 'sqlite':
            result = c.fetchall()
            n = len(result)
        elif db_config.db_type == 'postgresql':
            # slightly less memory intensive than fetching all
            result = c
            n = c.rowcount
        print(f'Cases with allegations: {n}')
        print(f'Processing allegations...')
        for row in result:
            alleg.process_allegations(cnx.cursor(), row)

        cnx.commit()
        print('Migration complete.')
    finally:
        c.close()
        cnx.close()

    # update error_log.allegations_parse_error
    # with values from allegations.parse_error
    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f'Attempting to update {db_config.error_log} table...')
            c.execute(error_log_query)
    except Exception as e:
        cnx.rollback()
        raise Exception(f'Unable to update {db_config.error_log} table') from e
    else: # no exception
        cnx.commit()
        print(f'Updated {db_config.error_log} table')
    finally:
        c.close()
        cnx.close()


if __name__ == '__main__':
    main()
