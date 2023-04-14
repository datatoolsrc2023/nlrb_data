from common import app_config, sql
import sys


def main():
    cnx = sql.db_cnx()

    """
    Deduplicate cases_raw table
    into cases_raw_deduped table
    and create cases table.
    """

    error = False

    cnx = sql.db_cnx()
    cnx.begin()
    c = cnx.cursor()

    # Deduplicate cases_raw table into cases_raw_deduped table
    statements = sql.get_query_lines_from_file('dedup_cases_raw.sql')

    try:
        print(f'Deduplicating {app_config.cases_raw} table',
              f'into {app_config.cases_raw_deduped}')
        for statement in statements:
            print(statement)
            c.execute(statement)
        cnx.commit()
    except Exception as e:
        error = True
        print(f'Failed to deduplicate table'
              f'{app_config.cases_raw_deduped}: {e}')
        print('Rolling back')
        cnx.rollback()

    # Create cases table
    statements = sql.get_query_lines_from_file('cases.sql')

    try:
        print(f'Creating {app_config.cases} table')
        for statement in statements:
            print(statement)
            c.execute(statement)
        cnx.commit()
    except Exception as e:
        error = True
        print(f'Failed to create table'
              f'{app_config.cases}: {e}')
        print('Rolling back')
        cnx.rollback()

    # Clean up gracefully, then exit with error if needed
    c.close()
    cnx.close()

    if error:
        sys.exit(1)


if __name__ == '__main__':
    main()
