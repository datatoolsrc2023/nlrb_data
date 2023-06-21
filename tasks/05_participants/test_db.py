#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Confirm database meets expectations."""

    pages_query = 'SELECT COUNT(*) c from pages;'
    participants_query = 'SELECT COUNT(*) p from participants;'

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(pages_query)
            count = c.fetchone()[0]
            if count == 0:
                raise Exception(f'Expected {db_config.pages} table '
                                'to be populated, found 0 records')
            c.execute(participants_query)
    except Exception as e:
        raise Exception(f'Could not count cases or pages') from e
    else:
        print(f'{db_config.cases} and {db_config.participants} '
              'table count expectations met')
    finally:
        c.close()
        cnx.close()
