#!/usr/bin/env python3

from common import sql

import allegations as alleg

from psycopg2.extras import DictCursor

def main():
    """Run the migration."""

    allegations_query = """
    SELECT id, case_number, allegations_raw
    FROM cases
    WHERE allegations_raw IS NOT NULL
    AND allegations_raw <> ''
    AND allegations_parse_error IS NULL
    ;
    """

    # cnx = sql.db_cnx(cursor_factory=DictCursor)
    try:
        with sql.db_cnx(cursor_factory=DictCursor) as cnx, cnx.cursor() as c:
            c = cnx.cursor()
            c.execute(allegations_query)
            n = c.rowcount
            print(f'Cases with allegations: {n}')
            for row in c:
                alleg.process_allegations(cnx.cursor(), row)
    except Exception as e:
        print(f'Error: {e}')
        print('Rolling back.')
    else: # no exception
        print('Migration complete.')
    finally:
        cnx.close()


if __name__ == '__main__':
    main()
