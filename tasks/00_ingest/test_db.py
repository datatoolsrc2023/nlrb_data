#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Confirm cases_raw table exists"""

    query = f"""
            SELECT * FROM pg_tables
            WHERE tablename = 'cases_raw';
            """

    try:
        with sql.db_cnx() as cnx, cnx.cursor() as c:
            c.execute(query)
            if not c.fetchone():
                raise Exception(f'{db_config.cases_raw} table does not exist')
    except Exception as e:
        raise Exception(f'Could not test for existence of {db_config.cases_raw}') from e
    else: # no exception
        print(f'{db_config.cases_raw} table exists')
    finally:
        cnx.close()
