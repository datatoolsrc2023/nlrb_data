#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Drop cases_raw table"""

    error = False

    cnx = sql.db_cnx()
    c = cnx.cursor()
    query = f"""
            DROP TABLE IF EXISTS
            {db_config.cases_raw}
            """
    try:
        print(f'attempting to drop {db_config.cases_raw} table')
        c.execute(query)
    except:
        print("failed to drop table")
        raise
    else: # no exception
        cnx.commit()
        print(f"dropped {db_config.cases_raw} table")
    finally:
        cnx.close()
