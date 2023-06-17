#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Undo all changes this task might have made."""

    drop_query = 'DROP TABLE IF EXISTS participants'
    
    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f'Attempting to drop {db_config.participants} table')
            c.execute(drop_query)
    except Exception as e:
        raise Exception(f'Failed to drop {db_config.participants} table') from e
    else: # no exception
        print(f'Dropped {db_config.participants} table')
    finally:
        c.close()
        cnx.close()
