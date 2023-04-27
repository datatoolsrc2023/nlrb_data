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


def db_cnx(host: str = db_config.host,
           user: str = db_config.user,
           password: str = db_config.password,
           database: str = db_config.database,
           sql_mode: str = db_config.sql_mode,
           cursorclass=pymysql.cursors.Cursor) -> pymysql.Connection:
    return pymysql.connect(user=user, host=host, password=password,
                           database=database, sql_mode=sql_mode,
                           cursorclass=cursorclass)


def db_cnx_str(host: str = db_config.host,
               user: str = db_config.user,
               password: str = db_config.password,
               port: str = db_config.port,
               database: str = db_config.database) -> str:
    return f'mysql://{user}:{password}@{host}:{port}/{database}'


def petl_insert(cases_tbl: etl.Table,
                cnx: pymysql.Connection,
                tablename: str) -> None:
    """
    Takes a database connection object, a PETL table, and
    a database tablename, and inserts data into the DB table.
    If there are more than 0 rows in the DB table, appends rows
    to the existing table.
    """
    result = etl.fromdb(cnx, f'SELECT count(*) from {tablename}')
    db_count = list(etl.values(result, 'count(*)'))[0]

    if db_count > 0:
        print(f'Appending data to {tablename} table...')
        etl.appenddb(cases_tbl, cnx, tablename)
    else:
        print(f'Truncating {tablename} table and inserting data...')
        etl.todb(cases_tbl, cnx, tablename)
    return None
