#!/usr/bin/env python3

import re

import pymysql

# Match cases like 8(a)(1) and 8(a)(1)(A)
# '(?:\([A-Z]+\))?' is an optional non-matching group for the last (A)
# Could also just do something like this:
# '(\d(?:\([0-9a-zA-Z]+\))?) (.+)'
pat = '(\d\([a-z]+\)\(\d+\)(?:\([A-Z]+\))?) (.+)'
pat = re.compile(pat)

def parse_allegations(s: str) -> (str, str):
    lines = (x.strip() for x in s.strip().split('\n'))
    # Ignore empty lines in case of "\n \n" or "\n\n"
    lines = (l for l in lines if l != "")
    matches = ((pat.match(line), line) for line in lines)
    return [
            (m.group(1), m.group(2), None) if m is not None
            else (None, None, line)
            for m,line in matches
            ]


def process_allegations(cursor, case_row):
    raw = case_row['allegations_raw']
    case_id = case_row['id']

    exc = None
    try:
        okay = True
        for result in parse_allegations(raw):
            code, desc, err = result
            if err is not None:
                print(f'\tERROR CASE({case_row["case_number"]}): {err}')
                okay = False
                continue
            # Could executemany() here, but then we wouldn't be able to skip on err
            cursor.execute('INSERT INTO allegations (case_id, code, description) VALUES (%s, %s, %s);', (case_id, code, desc))

        # We could also check `if okay:` and mark a *successful* run,
        # but we'd have to update the data model a bit first.
        if okay:
            # Mark case with successful allegations parse
            #TODO How do I ensure this worked?
            cursor.execute('UPDATE cases SET allegations_parse_error = 0 WHERE id = %s;', (case_id))
        else:
            # Mark case with failed allegations parse
            cursor.execute('UPDATE cases SET allegations_parse_error = 1 WHERE id = %s;', (case_id))

    except Exception as e:
        print(f'Error: {e}')
        exc = e
    finally:
        cursor.close()
        if exc is not None:
            raise(exc)


def main():
    """Run the migration."""
    from connection import Connection
    from .. import db_config

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
        c = cnx.cursor()
        n = c.execute(allegations_query)
        print(f'Cases with allegations: {n}')
        for row in c:
            process_allegations(cnx.cursor(), row)
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
