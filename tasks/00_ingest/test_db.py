#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Confirm cases_raw table exists"""

    if db_config.db_type == 'sqlite3':
        query = f"""
                SELECT name FROM sqlite_master
                WHERE type='table'
                AND name='cases_raw';
                """
    elif db_config.db_type == 'postgresql':
        query = f"""
                SELECT * FROM pg_tables
                WHERE tablename = 'cases_raw';
                """

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(query)
    except Exception as e:
        raise Exception(f'Could not test for existence of {db_config.cases_raw}') from e
    else: # no exception
        if not c.fetchone():
            raise Exception(f'{db_config.cases_raw} table does not exist')
        print(f'{db_config.cases_raw} table exists')
    finally:
        c.close()
        cnx.close()
