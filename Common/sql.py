from . import paths
import Common.db_config as db_config
import petl as etl
import psycopg2


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


def db_cnx(host=db_config.host,
           user=db_config.user,
           password=db_config.password,
           dbname=db_config.database,
           cursor_factory=psycopg2.extensions.cursor,
           **kwargs):
    return psycopg2.connect(user=user, host=host, password=password,
                            dbname=dbname, cursor_factory=cursor_factory,
                            **kwargs)


def db_cnx_str(host: str = db_config.host,
               user: str = db_config.user,
               password: str = db_config.password,
               port: str = db_config.port,
               database: str = db_config.database) -> str:
    return f'mysql://{user}:{password}@{host}:{port}/{database}'


def petl_insert(cases_tbl: etl.Table,
                cnx,
                schema: str,
                tablename: str) -> None:
    """
    Takes a database connection object, a PETL table, and
    a database tablename, and inserts data into the DB table.
    If there are more than 0 rows in the DB table, appends rows
    to the existing table.
    """
    result = etl.fromdb(cnx, f'SELECT count(*) as c from {tablename}')
    db_count = list(etl.values(result, 'c'))[0]

    if db_count > 0:
        print(f'Appending data to {tablename} table...')
        etl.appenddb(cases_tbl, cnx, tablename)
    else:
        print(f'Truncating {tablename} table and inserting data...')
        etl.todb(cases_tbl, cnx, tablename)
    return None
