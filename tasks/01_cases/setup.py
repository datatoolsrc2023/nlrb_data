#!/usr/bin/env python3

from common import db_config, sql


def main():
    """Create cases table"""

    statements = sql.get_query_lines_from_file(f'{db_config.db_type}/cases.sql')

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f'Attempting to create {db_config.cases} table...')
            for statement in statements:
                c.execute(statement)
    except:
        print(f'Failed to create {db_config.cases}')
    else:
        print(f'Created {db_config.cases} table')
    finally:
        c.close()
        cnx.close()


if __name__ == '__main__':
    main()
