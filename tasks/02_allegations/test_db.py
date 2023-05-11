#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Confirm database meets expectations."""

    cases_query = 'SELECT COUNT(*) c from cases'
    allegations_query = 'SELECT COUNT(*) c from allegations'

    try:
        with sql.db_cnx() as cnx:
            c_cases = cnx.cursor()
            c_allegations = cnx.cursor()
            print('Attempting to count cases and allegations...')
            c_cases.execute(cases_query)
            c_allegations.execute(allegations_query)
    except Exception as e:
        raise Exception(f'Could not count cases or allegations') from e
    else:
        cases_count = c_cases.fetchone()[0]
        if cases_count == 0:
            raise Exception(f'Expected {db_config.cases} table '
                            'to be populated, found 0 records')
        allegations_count = c_allegations.fetchone()[0]
        if allegations_count != 0:
            raise Exception(f'Expected 0 allegations, found {allegations_count}')
        print(f'{db_config.cases} and {db_config.allegations} '
              'table count expectations met')
    finally:
        c_cases.close()
        c_allegations.close()
        cnx.close()
