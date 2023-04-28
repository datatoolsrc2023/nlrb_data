#!/usr/bin/env python3

from common import db_config, sql

from psycopg2.extras import DictCursor


if __name__ == '__main__':
    """Confirm database meets expectations."""

    cases_query = 'SELECT COUNT(*) c from cases'
    allegations_query = 'SELECT COUNT(*) c from allegations'

    try:
        with sql.db_cnx(cursor_factory=DictCursor) as cnx, cnx.cursor() as c:
            c.execute(cases_query)
            count = c.fetchone()[0]
            if count == 0:
                raise Exception(f'Expected {db_config.cases} table '
                                'to be populated, found 0 records')
            c.execute(allegations_query)
            count = c.fetchone()[0]
            if count != 0:
                raise Exception(f'Expected 0 allegations, found {count}')
    except Exception as e:
        raise Exception(f'Could not count cases or allegations') from e
    else:
        print(f'{db_config.cases} and {db_config.allegations} '
              'table count expectations met')
    finally:
        cnx.close()
