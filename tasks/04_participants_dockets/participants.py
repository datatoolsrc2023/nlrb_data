from collections import namedtuple
import re

pat = ''
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


