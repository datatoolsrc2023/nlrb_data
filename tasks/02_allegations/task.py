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

    cnx = sql.db_cnx(cursor_factory=DictCursor)
    try:
        c = cnx.cursor()
        n = c.execute(allegations_query)
        print(f'Cases with allegations: {n}')
        for row in c:
            print(c)
            alleg.process_allegations(cnx.cursor(), row)
        cnx.commit()
        print('Migration complete.')
    except Exception as e:
        print(f'Error: {e}')
        print('Rolling back.')
        cnx.rollback()
    finally:
        c.close()
        cnx.close()


if __name__ == '__main__':
    main()
