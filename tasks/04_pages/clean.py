from common import sql, db_config


def main():
    """Drop pages table."""

    query = 'DROP TABLE IF EXISTS pages'

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f'Attempting to drop {db_config.pages} table')
            c.execute(query)
    except Exception as e:
        print(f'Failed to drop {db_config.pages} table')
        raise e
    else: # no exception
        print(f'Dropped {db_config.pages} table')
    finally:
        c.close()
        cnx.close()


if __name__ == "__main__":
    main()