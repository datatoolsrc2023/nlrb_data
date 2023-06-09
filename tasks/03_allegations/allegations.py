from collections import namedtuple
from common import db_config
import re

# Match cases like 8(a)(1) and 8(a)(1)(A)
# '(?:\([A-Z]+\))?' is an optional non-matching group for the last (A)
# Could also just do something like this:
# '(\d(?:\([0-9a-zA-Z]+\))?) (.+)'
pat = '(\d\([a-z]+\)(?:\(\d+\))?(?:\([A-Z]+\))?) (.+)'
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

    if db_config.db_type == 'sqlite':
        query = '''INSERT INTO allegations
                    (case_id, code, description, raw_text)
                    VALUES (?, ?, ?, ?)
                '''
    elif db_config.db_type == 'postgresql':
        query = """INSERT INTO allegations
                    (case_id, code, description, raw_text)
                    VALUES (%s, %s, %s, %s);
                """

    try:
        for r in parse_lines(raw):
            if r.parse_error:
                print(f'\tERROR CASE({case_row["case_number"]}): {r.raw}')

            cursor.execute(query, (case_id, r.code, r.desc, r.raw))

    except Exception as e:
        raise Exception('Unable to parse allegations') from e
    finally:
        cursor.close()
