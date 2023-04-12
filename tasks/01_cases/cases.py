#!/usr/bin/env python3

import petl as etl


def clean_header(cases_tbl):
    print('Setting header...')
    header = etl.header(cases_tbl)
    clean_header = [h.replace('allegations', 'allegations_raw')
                    .replace('participants', 'participants_raw')
                    for h in header]
    cases_tbl = etl.setheader(cases_tbl, clean_header)
    return cases_tbl


def convert_filed_date(val, row):
    split_date = row.date_filed.split('/')
    return split_date[2] + '-' + split_date[0] + '-' + split_date[1]


def convert_closed_date(val, row):
    split_date = row.date_closed.split('/')
    return split_date[2] + '-' + split_date[0] + '-' + split_date[1]


def clean_data(cases_tbl):
    print('Cleaning data...')
    clean_tbl = etl.addfield(cases_tbl, 'docket_activity_raw', None, 13)
    clean_tbl = etl.addfields(clean_tbl, [
        ('allegations_parse_error', None),
        ('participants_parse_error', None),
        ('docket_activity_parse_error', None)
    ])
    clean_tbl = etl.convert(clean_tbl, 'date_filed',
                            convert_filed_date, pass_row=True)
    clean_tbl = etl.convert(clean_tbl, 'date_closed',
                            convert_closed_date, pass_row=True)
    return clean_tbl


def main():
    import common
    from Common.connection import Connection
    from Common.db_helpers import exec_sql_file, petl_insert
    import config
    import db_config
    import pymysql

    dedup_sql = config.sql_dir + 'dedup_cases_raw.sql'

    petl_cnx = pymysql.connect(host=db_config.host,
                               database=db_config.database,
                               user=db_config.user,
                               password=db_config.password)
    petl_cnx.cursor().execute('SET SQL_MODE=ANSI_QUOTES')

    # dedup cases_raw table
    exec_sql_file(petl_cnx, dedup_sql)

    # get cases PETL table from deduped cases table
    cases_query = f'SELECT * FROM {config.cases_deduped};'
    cases_tbl = etl.fromdb(petl_cnx, cases_query)

    # set header for cases PETL table
    # add extra columns, and clean data
    clean_head = clean_header(cases_tbl)
    insert_tbl = clean_data(clean_head)

    # create clean cases table if not exists
    cases_sql = config.sql_dir + 'cases.sql'
    exec_sql_file(petl_cnx, cases_sql)

    # insert cleaned cases into DB
    try:
        petl_insert(petl_cnx, insert_tbl, config.cases)
    except Exception as e:
        print(f'Error inserting into {config.cases}: {e}')


if __name__ == '__main__':
    main()
