from common import db_config, sql


if __name__ == '__main__':
    """Confirm cases table exists."""

    count = 0

    cnx = sql.db_cnx()
    c = cnx.cursor()
    query = f"""
            SELECT * FROM pg_tables
            WHERE tablename = '{db_config.cases}';
            """

    try:
        c.execute(query)
        if not c.fetchone():
            raise ValueError(f'Expected {db_config.cases} to exist,',
                             'but table does not exist')
    except:
        print(f'Could not test for table existence')
        raise
    else:
        print('table exists')
    finally:
        cnx.close()
