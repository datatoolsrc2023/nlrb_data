#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Confirm cases_raw table has rows."""

    count = 0
    error = False

    cnx = sql.db_cnx()
    c = cnx.cursor() 
    query = f"""
            SELECT count(*)
            FROM {db_config.cases_raw};
            """

    try:
        c.execute(query)
        count = c.fetchone()[0]
        if count == 0:
            raise ValueError(f'Expected {db_config.cases_raw} table to be populated, found 0 records')     
    except:
        print('unable to count rows')
        raise
    else: # no exception
        cnx.commit()
    finally:
        cnx.close()
