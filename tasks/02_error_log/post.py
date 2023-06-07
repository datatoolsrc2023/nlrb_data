#!/usr/bin/env python3

from common import db_config, sql

if __name__ == '__main__':
    """Confirm error_log table has rows"""

    query = 'SELECT count(*) FROM error_log'

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(query)
    except Exception as e:
        print(f'Could not count rows in {db_config.error_log} table')
        raise e
    else: # no exception
        count = c.fetchone()[0]
        if count == 0:
            raise Exception(f'Expected {db_config.error_log} table '
                            'to be populated, '
                            'but found 0 records')
        print(f'Found {count} rows in {db_config.error_log} table')
    finally:
        c.close()
        cnx.close()
