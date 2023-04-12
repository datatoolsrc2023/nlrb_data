#!/usr/bin/env python3

import petl as etl
import re


def clean_header(cases_tbl):
    # TODO use a dict for new header
    header = etl.header(cases_tbl)
    clean_header = [h.replace(' ', '_').replace('&', 'and')
                    .replace('Employees_on_charge/petition',
                             'employees_involved')
                    .replace('Status', 'case_status')
                    .replace('Allegations', 'allegations')
                    .replace('Participants', 'participants')
                    .lower() for h in header]
    clean_header = [(re.sub(r'^union$', 'union_name', h))
                    for h in clean_header]
    cases_tbl = etl.setheader(cases_tbl, clean_header)
    return cases_tbl


def main():

    import argparse
    import common
    from Common.connection import Connection
    from Common import config, db_config
    from Common.db_helpers import petl_cnx, petl_insert, exec_sql_file
    from os import listdir

    input_dir = config.input_dir
    input_files = [input_dir + x for x in
                   listdir(input_dir)
                   if 'csv' in x]

    # parse command line arguments
    parser = argparse.ArgumentParser(
         prog='ingest',
         description='Loads data from CSV(s) into cases_raw table'
    )
    parser.add_argument('-f', '--filename')
    parser.add_argument('-l', '--lines', default='all')
    args = parser.parse_args()
    files = [args.filename] if args.filename else input_files

    # create raw cases table if not exists
    cnx = Connection(db_config)
    raw_cases_sql = config.sql_dir + 'cases_raw.sql'
    exec_sql_file(cnx, raw_cases_sql)

    # load data from CSVs into raw table
    petl_cnx = petl_cnx(host=db_config.host,
                        user=db_config.user,
                        password=db_config.password,
                        database=db_config.database)

    for csv in files:
        cases_tbl = etl.fromcsv(csv)
        if args.lines != 'all':
            cases_tbl = etl.head(cases_tbl, int(args.lines))
        print(f'Processing {args.lines} lines of {csv}...')
        insert_tbl = clean_header(cases_tbl)
        try:
            petl_insert(petl_cnx, insert_tbl, config.cases_raw)
        except Exception as e:
            print(f'Error loading to DB: {e}')
            raise e


if __name__ == '__main__':
    main()
