from common import db_config, sql
import psycopg2
import sys

if __name__ == '__main__':
    """Confirm cases table exists."""

    count = 0

    with sql.db_cnx() as cnx, cnx.cursor() as c:
        query = f"""
                SELECT * FROM pg_tables
                WHERE schemaname = 'public'
                AND tablename = '{db_config.cases}';
                """

        try:
            c.execute(query)
            if not c.fetchone():
                error = True
                print(f'Expected {db_config.cases} to exist,',
                        'but table does not exist')
                sys.exit(1)
        except psycopg2.ProgrammingError as e:
            print(f'Could not test for table existence: {e}')
