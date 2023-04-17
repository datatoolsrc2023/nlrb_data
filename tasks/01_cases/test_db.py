from common import app_config, sql
import psycopg2
import sys

if __name__ == '__main__':
    """Confirm database meets expectations."""

    error = False
    count = 0

    with sql.db_cnx() as cnx:

        # Test that cases_raw_deduped has rows
        with cnx.cursor() as c:
            query = f"""
                    SELECT count(*)
                    FROM {app_config.schema}.{app_config.cases_raw_deduped};
                    """
            try:
                c.execute(query)
                count = c.fetchone()[0]
                if count == 0:
                    error = True
                    print(f'Expected {app_config.cases_raw_deduped}'
                          'table to be populated,',
                          'found 0 records')
            except (psycopg2.ProgrammingError, psycopg2.OperationalError) as e:
                print('Could not count rows in'
                      f'{app_config.cases_raw_deduped}: {e}')

        # Test that cases table exists
        with cnx.cursor() as c:
            query = f"""
                    SELECT table_name from information_schema.tables\
                    WHERE table_schema = '{app_config.schema}'\
                    AND table_name = '{app_config.cases_raw}';
                    """
            try:
                result = c.execute(query)
                if result == 0:
                    error = True
                    print(f'Expected {app_config.cases_raw} to exist,'
                          'but table does not exist')
            except psycopg2.ProgrammingError as e:
                print(f'Could not test for table existence: {e}')

    if error:
        sys.exit(1)
