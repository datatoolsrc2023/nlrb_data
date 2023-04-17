from common import app_config, sql
import psycopg2
import sys

if __name__ == '__main__':

    error = False

    with sql.db_cnx() as cnx:
        cnx.begin()

        # Drop cases_raw_deduped table
        with cnx.cursor() as c:
            query = f"""
                    DROP TABLE {app_config.schema}.
                    {app_config.cases_raw_deduped}
                    """
            try:
                c.execute(query)
                cnx.commit()
            except psycopg2.OperationalError as e:
                error = True
                print('Could not drop table'
                      f'{app_config.cases_raw_deduped}: {e}')
                cnx.rollback()

    # Exit gracefully

    if error:
        sys.exit(1)
