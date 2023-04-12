import petl as etl
import pymysql


def petl_cnx(host, user, password, database):
    petl_cnx = pymysql.connect(host=host,
                               user=user,
                               password=password,
                               database=database)
    petl_cnx.cursor().execute('SET SQL_MODE=ANSI_QUOTES')
    return petl_cnx


def petl_insert(cnx, cases_tbl, tablename):
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


def exec_sql_file(cnx, sql_file):
    with open(sql_file, 'r') as f:
        query = f.read().split(';')
    if not query[-1]:
        query.pop()
    cnx.begin()
    try:
        c = cnx.cursor()
        for q in query:
            c.execute(q + ';')
        cnx.commit()
        print(f'Executed SQL from {sql_file}')
    except Exception as e:
        print(f'Error executing {sql_file}: {e}')
        cnx.rollback()
    finally:
        c.close()
