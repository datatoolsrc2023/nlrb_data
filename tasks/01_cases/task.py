#!/usr/bin/env python3

def main():
    import cases
    from common import app_config, sql
    import polars as pl

    # Read case data from cases_raw table
    cnx_str = sql.db_cnx_str()

    query = f"""
            SELECT *
            FROM {app_config.schema}.{app_config.cases_raw};
            """

    df = pl.read_database(query, cnx_str)

    # Add extra columns, clean data, and deduplicate
    # cases by case_number and date_filed
    df = cases.clean_data(df)

    # Insert cleaned cases into DB
    try:
        print(f'Inserting cases data into {app_config.cases} table')
        df.write_database(app_config.cases, cnx_str, if_exists='append')
    except Exception as e:
        print(f'Error inserting into {app_config.cases}: {e}')


if __name__ == '__main__':
    main()
