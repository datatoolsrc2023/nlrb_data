#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Confirm cases_raw table has rows."""

    query = 'SELECT count(*) FROM cases_raw'

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(query)   
    except Exception as e:
        raise Exception(f'Unable to count rows in {db_config.cases_raw} table') from e
    else: # no exception
        count = c.fetchone()[0]
        if count == 0:
            raise Exception(f'Expected {db_config.cases_raw} table '
                            'to be populated, but '
                            'found 0 records')  
        print(f'Found {count} rows in {db_config.cases_raw}')
    finally:
        c.close()
        cnx.close()
