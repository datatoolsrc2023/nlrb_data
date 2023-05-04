#!/usr/bin/env python3

from common import db_config, sql

from psycopg2.extras import DictCursor 


if __name__ == '__main__':
    """Undo all changes this task might have made."""

    drop_query = 'DROP TABLE IF EXISTS allegations'
    update_query = 'UPDATE cases SET allegations_parse_error = NULL'

    try:
        with sql.db_cnx(cursor_factory=DictCursor) as cnx, cnx.cursor() as c:
            print(f'Attempting to drop {db_config.allegations} table '
                  f'and reset allegations_parse_error in {db_config.cases} table to NULL')
            c.execute(drop_query)
            c.execute(update_query)
            changed = c.rowcount
    except Exception as e:
        raise Exception(f'Failed to drop table and/or reset '
                        f'allegations_parse_error in {db_config.cases} table') from e
    else: # no exception
        print(f'Dropped {db_config.allegations} table and '
              f'reset allegations_parse_error = NULL in {db_config.cases} table '
              f'for all {changed} case records')
    finally:
        cnx.close()
