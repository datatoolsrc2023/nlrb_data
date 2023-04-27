#!/usr/bin/env python3

from common import db_config, sql


def main():
    cnx = sql.db_cnx()

    """Create cases table"""

    cnx = sql.db_cnx()
    c = cnx.cursor()

    # Create cases table
    statements = sql.get_query_lines_from_file('cases.sql')
    try:
        print(f'Creating {db_config.cases} table...')
        for statement in statements:
            c.execute(statement)
    except:
        raise ValueError(f'Failed to create table '
                         f'{db_config.cases}')
    else:
        cnx.commit()
    finally:
        cnx.close()


if __name__ == '__main__':
    main()
