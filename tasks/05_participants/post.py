#!/usr/bin/env python3

from common import sql


if __name__ == '__main__':
    """Confirm no records require attention."""

    count_query = 'SELECT COUNT(*) c FROM error_log WHERE participants_parse_error is TRUE'
    text_query = '''
                SELECT c.case_number, p.raw_text
                FROM cases c
                INNER JOIN participants p
                ON c.id = p.case_id
                INNER JOIN error_log e
                on c.id = e.case_id
                WHERE e.participants_parse_error is TRUE
                '''

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(count_query)
            count = c.fetchone()[0]
            if count != 0:
                print(f'Expected 0 parse errors, found {count}')
                c.execute(text_query)
                for case_number, raw_text in c.fetchall():
                    print(f'Case: {case_number} Raw text: {raw_text}')
    except Exception as e:
        print('Could not count or summarize participants parse errors')
        raise e
    else: # no exception
        print('Finished counting and summarizing participants parse errors')
    finally:
        c.close()
        cnx.close()
