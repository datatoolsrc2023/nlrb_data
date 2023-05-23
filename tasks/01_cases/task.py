#!/usr/bin/env python3

def main():
    import cases
    from common import db_config, sql
    import polars as pl
    from psycopg2 import sql as psql
    import psycopg2.extras
    import sqlite3

    # Read case data from cases_raw table
    cnx_str = sql.db_cnx_str()

    query = 'SELECT * FROM cases_raw'

    df = pl.read_database(query, cnx_str)

    # Add extra columns, clean data, and deduplicate
    # cases by case_number and date_filed
    df = cases.clean_data(df)

    # Insert cleaned cases into DB
    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f'Attempting to insert rows into {db_config.cases} table...')
            if db_config.db_type == 'sqlite':
                columns = ','.join(name for name in df.columns)
                placeholders = ','.join(['?' for _ in df.columns])
                insert_stmt = f"INSERT INTO cases ({columns}) VALUES({placeholders})"
                c.executemany(insert_stmt, df.rows())
            elif db_config.db_type == 'postgresql':
                columns = psql.SQL(",").join(psql.Identifier(name) for name in df.columns)
                placeholders = psql.SQL(",").join([psql.Placeholder() for _ in df.columns])

                insert_stmt = psql.SQL("INSERT INTO {} ({}) VALUES({});").format(
                psql.Identifier(db_config.cases), columns, placeholders
                )
                psycopg2.extras.execute_batch(c, insert_stmt, df.rows())
    except Exception as e:
        raise Exception(f'Error inserting into {db_config.cases}') from e
    else:
        print(f'Inserted rows into {db_config.cases} table')
    finally:
        c.close()
        cnx.close()


if __name__ == '__main__':
    main()
