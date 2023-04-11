#!/usr/bin/env python3

from common import db_config, Connection

from collections import namedtuple
import re

import pymysql

# Match cases like 8(a)(1) and 8(a)(1)(A)
# '(?:\([A-Z]+\))?' is an optional non-matching group for the last (A)
# Could also just do something like this:
# '(\d(?:\([0-9a-zA-Z]+\))?) (.+)'
pat = '(\d\([a-z]+\)\(\d+\)(?:\([A-Z]+\))?) (.+)'
pat = re.compile(pat)

Row = namedtuple('Row', 'code desc parse_error raw')

def parse_line(line: str) -> Row:
    m = pat.match(line)
    return Row(
            code=None if m is None else m.group(1),
            desc=None if m is None else m.group(2),
            parse_error=True if m is None else False,
            raw=line
            )


def parse_lines(s: str) -> list[(str, str)]:
    lines = (x.strip() for x in s.strip().split('\n'))
    # Ignore empty lines in case of "\n \n" or "\n\n"
    lines = (l for l in lines if l != "")
    rows = (parse_line(l) for l in lines if l != "")
    return rows


def process_allegations(cursor, case_row):
    raw = case_row['allegations_raw']
    case_id = case_row['id']

    exc = None
    try:
        okay = True
        for r in parse_lines(raw):
            if r.parse_error:
                print(f'\tERROR CASE({case_row["case_number"]}): {r.raw}')
                okay = False

            cursor.execute('''INSERT INTO allegations
                                (case_id, code, description, parse_error, raw_text)
                              VALUES (%s, %s, %s, %s, %s);
                              ''',
                              (case_id, r.code, r.desc, r.parse_error, r.raw))

        #TODO We might be good to dispense with this part altogether...
        #TODO How do I ensure this worked?
        cursor.execute('UPDATE cases SET allegations_parse_error = %s WHERE id = %s;',
                (0 if okay else 1, case_id))

    except Exception as e:
        print(f'Error: {e}')
        exc = e
    finally:
        cursor.close()
        if exc is not None:
            raise(exc)


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

    cnx = Connection(db_config)
    cnx.begin()
    try:
        c = cnx.dict_cursor()
        n = c.execute(allegations_query)
        print(f'Cases with allegations: {n}')
        for row in c:
            process_allegations(cnx.dict_cursor(), row)
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
