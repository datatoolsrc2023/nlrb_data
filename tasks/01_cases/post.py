#!/usr/bin/env python3

from common import db_config, sql

if __name__ == '__main__':
    """Confirm cases table has rows"""

    query = 'SELECT count(*) FROM cases'

    try:
        with sql.db_cnx() as cnx, cnx.cursor() as c:
            c.execute(query)
            count = c.fetchone()[0]
            if count == 0:
                raise Exception(f'Expected {db_config.cases} table '
                                'to be populated, '
                                'but found 0 records')
    except Exception as e:
        raise Exception(f'Could not count rows in {db_config.cases} table') from e
    else: # no exception
        print(f'{db_config.cases} table has rows')
    finally:
        cnx.close()
