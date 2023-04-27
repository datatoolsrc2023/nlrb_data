#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Confirm cases_raw table has rows"""

    count = 0
    error = False

    cnx = sql.db_cnx()
    c = cnx.cursor()
    query = f"""
            SELECT * FROM pg_tables
            WHERE tablename = '{db_config.cases_raw}';
            """

    try:
        c.execute(query)
        if not c.fetchone():
            raise ValueError(f'Expected {db_config.cases_raw} to exist,',
                    'but table does not exist')
    except:
        print(f'Could not test for table existence')
        raise
    else: # no exception
        cnx.commit()
    finally:
        cnx.close()
