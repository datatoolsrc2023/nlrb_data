#!/usr/bin/env python3

import argparse
from common import db_config, sql, paths
import ingest
from os import listdir
import petl as etl


def main():

    csv_dir = paths.data / 'case_files'
    input_files = [csv_dir / x for x in listdir(csv_dir)
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

    cnx = sql.db_cnx()

    # load data from CSVs into cases_raw table
    for csv in files:
        cases_tbl = etl.fromcsv(csv)
        if args.lines != 'all':
            cases_tbl = etl.head(cases_tbl, int(args.lines))
        print(f'Processing {args.lines} lines of {csv}...')
        insert_tbl = ingest.clean_header(cases_tbl)
        try:
            sql.petl_insert(insert_tbl, cnx, db_config.cases_raw)
        except Exception as e:
            print('Error loading to DB')
            raise e


if __name__ == '__main__':
    main()
