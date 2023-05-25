#!/usr/bin/env python3

def main():
    import cases
    from common import db_config, sql
    import polars as pl
    from psycopg2 import sql as psql
    import psycopg2.extras

    # Read case data from cases_raw table
    cnx_str = sql.db_cnx_str()

    query = 'SELECT * FROM cases_raw'

    df = pl.read_database(query, cnx_str)

    # Add extra columns, clean data, and deduplicate
    # cases by case_number and date_filed
    df = cases.clean_data(df)

    # Insert cleaned cases into DB
    columns = psql.SQL(",").join(psql.Identifier(name) for name in df.columns)
    values = psql.SQL(",").join([psql.Placeholder() for _ in df.columns])

    insert_stmt = psql.SQL("INSERT INTO {} ({}) VALUES({});").format(
    psql.Identifier(db_config.cases), columns, values
    )

    try:
        with sql.db_cnx() as cnx, cnx.cursor() as c:
            print(f'Attempting to insert rows into {db_config.cases} table...')
            psycopg2.extras.execute_batch(c, insert_stmt, df.rows())
    except Exception as e:
        raise Exception(f'Error inserting into {db_config.cases}') from e
    else:
        print(f'Inserted rows into {db_config.cases} table')
    finally:
        cnx.close()


if __name__ == '__main__':
    main()
