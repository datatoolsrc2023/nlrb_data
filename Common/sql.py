from . import paths

def get_query_lines_from_file(filename: str) -> list[str]:
    """Takes a filename - only the basename! - and returns query lines as a list."""
    absolute = paths.sql / filename

    # Just let this raise an error for caller to catch
    with open(absolute, 'r') as f:
        sql = f.read()

    statements = sql.strip().split(';')
    statements = (s.strip() for s in statements)
    statements = (s for s in statements if len(s) > 0)
    statements = (' '.join(s.split()) for s in statements)
    return list(statements)
