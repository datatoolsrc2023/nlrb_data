#!/usr/bin/env python3

def main():
    import cases
    from common import db_config, sql
    import polars as pl

    # Read case data from cases_raw table
    cnx_str = sql.db_cnx_str()

    query = f"""
            SELECT *
            FROM {db_config.schema}.{db_config.cases_raw};
            """

    df = pl.read_database(query, cnx_str)

    # Add extra columns, clean data, and deduplicate
    # cases by case_number and date_filed
    df = cases.clean_data(df)

    # Insert cleaned cases into DB
    try:
        print(f'Inserting cases data into {db_config.cases} table')
        df.write_database(db_config.cases, cnx_str, if_exists='append')
    except Exception as e:
        print(f'Error inserting into {db_config.cases}: {e}')


if __name__ == '__main__':
    main()
