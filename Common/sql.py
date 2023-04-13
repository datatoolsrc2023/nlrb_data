from . import paths
import Common.db_config as db_config
import petl as etl
import pymysql


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


def db_cnx(cursorclass=pymysql.cursors.Cursor):
    """Returns a database connection object"""
    # TODO maybe add a context manager to this?
    cnx = pymysql.connect(**db_config.db_config, cursorclass=cursorclass)
    return cnx


def petl_insert(cnx, cases_tbl, tablename):
    """Takes a database connection object, a PETL table, and
    a database tablename, and inserts data into the DB table.
    If there are more than 0 rows in the DB table, appends rows
    to the existing table"""
    result = etl.fromdb(cnx, f'SELECT count(*) from {tablename}')
    db_count = list(etl.values(result, 'count(*)'))[0]
    # if there's already data in the DB table,
    # append to the table instead of truncating
    if db_count > 0:
        print(f'Appending data to {tablename}...')
        etl.appenddb(cases_tbl, cnx, tablename)
    else:
        print(f'Truncating {tablename} and inserting data...')
        etl.todb(cases_tbl, cnx, tablename)
    return None
