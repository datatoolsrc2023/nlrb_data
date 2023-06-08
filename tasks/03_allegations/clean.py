#!/usr/bin/env python3

from common import db_config, sql 


if __name__ == '__main__':
    """Undo all changes this task might have made."""

    drop_query = 'DROP TABLE IF EXISTS allegations'
    update_query = 'UPDATE error_log SET allegations_parse_error = NULL'

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f'Attempting to drop {db_config.allegations} table '
                  f'and reset allegations_parse_error in {db_config.error_log} table to NULL...')
            c.execute(drop_query)
            c.execute(update_query)
    except Exception as e:
        print(f'Failed to drop table and/or reset '
              f'allegations_parse_error in {db_config.error_log} table')
        raise e
    else: # no exception
        changed = c.rowcount
        print(f'Dropped {db_config.allegations} table and '
              f'reset allegations_parse_error = NULL in {db_config.error_log} table '
              f'for all {changed} case records')
    finally:
        c.close()
        cnx.close()
