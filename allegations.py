#!/usr/bin/env python3

import re

import pymysql

# Match cases like 8(a)(1) and 8(a)(1)(A)
# '(?:\([A-Z]+\))?' is an optional non-matching group for the last (A)
# Could also just do something like this:
# '(\d(?:\([0-9a-zA-Z]+\))?) (.+)'
pat = '(\d\([a-z]+\)\(\d+\)(?:\([A-Z]+\))?) (.+)'
pat = re.compile(pat)

def _parse_allegations(s: str) -> (str, str):
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
        for result in _parse_allegations(raw):
            code, desc, err = result
            if err is not None:
                print(f'\tERROR CASE({case_row["case_number"]}): {err}')
                okay = False
                continue
            # Could executemany() here, but then we wouldn't be able to skip on err
            cursor.execute('INSERT INTO allegations (case_id, code, description) VALUES (%s, %s, %s);', (case_id, code, desc))

        # We could also check `if okay:` and mark a *successful* run,
        # but we'd have to update the data model a bit first.
        if not okay:
            # Mark case allegations with bad parse
            #TODO How do I ensure this worked?
            cursor.execute('UPDATE cases SET allegations_parse_error = 1 WHERE id = %s;', (case_id))

    except Exception as e:
        print(f'Error: {e}')
        exc = e
    finally:
        cursor.close()
        if exc is not None:
            raise(exc)


def test_regex():
    regex_tests = [
            {
                'description': 'Valid 3-term allegation',
                'case': '8(a)(3) Discharge (Including Layoff and Refusal to Hire (not salting))',
                'expected': ('8(a)(3)', 'Discharge (Including Layoff and Refusal to Hire (not salting))')
            },
            {
                'description': 'Valid 4-term allegation',
                'case': "8(b)(1)(A) Duty of Fair Representation, incl'g Superseniority, denial of access",
                'expected': ("8(b)(1)(A)", "Duty of Fair Representation, incl'g Superseniority, denial of access")
            },
            {
                'description': 'Invalid allegation (numeric second term)',
                'case': "8(8)(1)(A) Duty of Fair Representation, incl'g Superseniority, denial of access",
                'expected': None
            },
            {
                'description': 'Valid hypothetical third term greater than 9',
                'case': '8(b)(11)(A) Something I made up',
                'expected': ('8(b)(11)(A)', 'Something I made up')
            }
            ]
    for t in regex_tests:
        print('Testing:', t['description'])
        got = pat.match(t['case'])
        expected = t['expected']
        if expected is None and got is not None:
            print(f'Expected None, got {got.group(1)} and {group(2)}')
            return False
        if expected is not None and got is None:
            print(f'Expected {expected[0]}, {expected[1]}, got None')
            return False
        if expected is None and got is None:
            continue

        gots = got.group(1), got.group(2)
        if gots != expected:
            print(f'Expected\n{expected}\nGot\n{gots}')
            return False

    # Tests passed
    return True

def test_parse_allegations():
    tests = [
            {
                'description': 'Multiple valid allegations',
                'case': """8(a)(3) Discharge (Including Layoff and Refusal to Hire (not salting))
                8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
                8(a)(1) Coercive Statements (Threats, Promises of Benefits, etc.)
                """,
                'expected': [
                    ('8(a)(3)', 'Discharge (Including Layoff and Refusal to Hire (not salting))', None),
                    ('8(a)(1)', 'Concerted Activities (Retaliation, Discharge, Discipline)', None),
                    ('8(a)(1)', 'Coercive Statements (Threats, Promises of Benefits, etc.)', None)
                    ]
            },
            {
                'description': 'Test single line and trailing whitespace',
                'case': """8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
                """,
                'expected': [
                    ('8(a)(1)', 'Concerted Activities (Retaliation, Discharge, Discipline)', None)
                    ]
            },
            {
                'description': 'Empty lines are ignored',
                'case': """8(a)(1) Coercive Rules

                8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
                """,
                'expected': [
                    ('8(a)(1)', 'Coercive Rules', None),
                    ('8(a)(1)', 'Concerted Activities (Retaliation, Discharge, Discipline)', None)
                    ]
            },
            {
                'description': 'Mismatch fails gracefully',
                'case': """8(2)(1) Coercive Rules
                8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
                """,
                'expected': [
                    (None, None, '8(2)(1) Coercive Rules'),
                    ('8(a)(1)', 'Concerted Activities (Retaliation, Discharge, Discipline)', None)
                    ]
            }
        ]

    for t in tests:
        print('Testing:', t['description'])
        got = _parse_allegations(t['case'])
        expected = t['expected']
        if got != expected:
            print(f'Expected\n{expected}\nGot\n{got}')
            return False

    # Tests passed
    return True


if __name__ == '__main__':
    if not test_regex() or not test_parse_allegations():
        import sys
        sys.exit(1)

    print('Tests passed, beginning migration.')

    from connection import Connection
    import db_config

    allegations_query = """
    SELECT id, case_number, allegations_raw
    FROM cases
    WHERE allegations_raw IS NOT NULL AND allegations_raw<>''
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
