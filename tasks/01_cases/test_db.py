from common import db_config, sql


if __name__ == '__main__':
    """Confirm cases table exists."""

    if db_config.db_type == 'sqlite':
        query = f"""
                SELECT name FROM sqlite_master
                WHERE type='table'
                AND name='cases';
                """
    elif db_config.db_type == 'postgresql':
        query = f"""
                SELECT * FROM pg_tables
                WHERE tablename = 'cases';
                """

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(query)
    except Exception as e:
        raise Exception(f'Could not test for existence of {db_config.cases} table') from e
    else:
        if not c.fetchone():
            raise Exception(f'Expected {db_config.cases} to exist, '
                            'but table does not exist')
        print(f'{db_config.cases} table exists')
    finally:
        c.close()
        cnx.close()
