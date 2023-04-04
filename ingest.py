import config
from os import listdir
import pymysql
import petl as etl
import re
import sys


def clean_header(cases_tbl):
    header = etl.header(cases_tbl)
    clean_header = [h.replace(' ', '_').replace('&', 'and')
                    .replace('Employees_on_charge/petition',
                             'employees_involved')
                    .replace('Status', 'case_status')
                    .replace('Allegations', 'allegations_raw')
                    .replace('Participants', 'participants_raw')
                    .lower() for h in header]
    clean_header = [(re.sub(r'^union$', 'union_name', h))
                    for h in clean_header]
    cases_tbl = etl.setheader(cases_tbl, clean_header)
    print(etl.header(cases_tbl))
    return cases_tbl


def convert_filed_date(val, row):
    split_date = row.date_filed.split('/')
    return split_date[2] + '-' + split_date[0] + '-' + split_date[1]


def convert_closed_date(val, row):
    split_date = row.date_closed.split('/')
    return split_date[2] + '-' + split_date[0] + '-' + split_date[1]


def clean_data(cases_tbl):
    clean_tbl = etl.addfield(cases_tbl, 'docket_activity_raw', None, 13)
    clean_tbl = etl.addfields(clean_tbl, [
        ('allegations_parse_error', 0),
        ('participants_parse_error', 0),
        ('docket_activity_parse_error', 0)
    ])
    clean_tbl = etl.convert(clean_tbl, 'date_filed',
                            convert_filed_date, pass_row=True)
    clean_tbl = etl.convert(clean_tbl, 'date_closed',
                            convert_closed_date, pass_row=True)
    return clean_tbl


def insert_into_db(cases_tbl, tablename):
    connection = pymysql.connect(host=config.host,
                                 user=config.user,
                                 database=config.database)
    connection.cursor().execute('SET SQL_MODE=ANSI_QUOTES')
    result = etl.fromdb(connection, f'SELECT count(*) from {tablename}')
    db_count = list(etl.values(result, 'count(*)'))[0]
    # if there's already data in the DB table,
    # append to the table instead of truncating
    if db_count > 0:
        etl.appenddb(cases_tbl, connection, tablename)
    else:
        etl.todb(cases_tbl, connection, tablename)
    return True


def main():
    case_files_dir = 'case_files'
    to_parse = [sys.argv[1]] if len(sys.argv) > 1\
        else [case_files_dir + '/' + x for x in listdir(case_files_dir)
              if 'csv' in x]
    lines = int(sys.argv[2]) if len(sys.argv) > 2 else 'all'

    tablename = 'cases'

    for csv in to_parse:
        cases_tbl = etl.fromcsv(csv)
        if lines != 'all':
            cases_tbl = etl.head(cases_tbl, lines)
        print(f'Processing {lines} lines of {csv}...')
        clean_head = clean_header(cases_tbl)
        clean_tbl = clean_data(clean_head)
        insert_into_db(clean_tbl, tablename)
        try:
            insert_into_db(clean_tbl, tablename)
        except Exception as e:
            print(f'Error loading to DB: {e}')


if __name__ == '__main__':
    main()
