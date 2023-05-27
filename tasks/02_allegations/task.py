#!/usr/bin/env python3

from common import db_config, sql

import allegations as alleg

<<<<<<< HEAD
from psycopg2.extras import DictCursor
from tqdm import tqdm
=======
if db_config.db_type == 'sqlite':
    import sqlite3

>>>>>>> main

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

    try:
        with sql.db_cnx() as cnx:
            if db_config.db_type == 'sqlite':
                cnx.row_factory = sqlite3.Row
            c = cnx.cursor()
            c.execute(allegations_query)
    except Exception as e:
        print(f'Error: {e}')
        print('Rolling back.')
    else: # no exception
        if db_config.db_type == 'sqlite':
            result = c.fetchall()
            n = len(result)
        elif db_config.db_type == 'postgresql':
            # slightly less memory intensive than fetching all
            result = c
            n = c.rowcount
        print(f'Cases with allegations: {n}')
        print(f'Processing allegations...')
        for row in tqdm(result):
            alleg.process_allegations(cnx.cursor(), row)

        cnx.commit()
        print('Migration complete.')
    finally:
        c.close()
        cnx.close()


if __name__ == '__main__':
    main()
