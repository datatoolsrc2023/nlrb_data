#!/usr/bin/env python3

from common import sql

from psycopg2.extras import DictCursor 



if __name__ == '__main__':
    """Confirm no records require attention."""

    count_query = 'SELECT COUNT(*) c FROM allegations WHERE parse_error is TRUE'
    text_query = '''
                SELECT c.case_number, a.raw_text
                FROM cases c
                INNER JOIN allegations a
                ON c.id = a.case_id
                WHERE a.parse_error is TRUE
                '''

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print('Attempting to count and summarize allegations parse errors...')
            c.execute(count_query)
            count = c.fetchone()[0]
            if count != 0:
                print(f'Expected 0 parse errors, found {count}')
                c.execute(text_query)
                for case_number, raw_text in c.fetchall():
                    print(f'Case: {case_number} Raw text: {raw_text}')
    except Exception as e:
        raise Exception('Could not count or summarize allegations parse errors') from e
    else: # no exception
        print('Finished counting and summarizing allegations parse errors')
    finally:
        c.close()
        cnx.close()
