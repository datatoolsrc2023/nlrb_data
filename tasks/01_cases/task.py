def main():
    import cases
    from common import app_config, sql
    import petl as etl

    # get cases PETL table from deduped cases table
    cnx = sql.db_cnx()
    cases_query = f"""
                  SELECT *
                  FROM {app_config.schema}.{app_config.cases_raw_deduped};
                  """
    cases_tbl = etl.fromdb(cnx, cases_query)

    # set header for cases PETL table
    # add extra columns, and clean data
    clean_head = cases.clean_header(cases_tbl)
    insert_tbl = cases.clean_data(clean_head)

    # insert cleaned cases into DB
    try:
        sql.petl_insert(cnx, insert_tbl, app_config.cases)
    except Exception as e:
        print(f'Error inserting into {app_config.cases}: {e}')


if __name__ == '__main__':
    main()
