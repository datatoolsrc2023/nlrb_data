#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Confirm database meets expectations."""

    cases_query = 'SELECT COUNT(*) c from cases;'
    
    if db_config.db_type == 'sqlite':
        pages_query = f"""
                SELECT name FROM sqlite_master
                WHERE type='table'
                AND name='pages';
                """
    elif db_config.db_type == 'postgresql':
        pages_query = f"""
                SELECT * FROM pg_tables
                WHERE tablename = 'pages';
                """

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(cases_query)
            count = c.fetchone()[0]
            if count == 0:
                raise Exception(f'Expected {db_config.cases} table to be populated, found 0 records')
            c.execute(pages_query)
    except Exception as e:
        raise Exception(f'Issue communicating with db: {e}')
    else:
        print(f'{db_config.cases} and {db_config.pages} '
              'cases and pages tables expectations met.')
    finally:
        c.close()
        cnx.close()
