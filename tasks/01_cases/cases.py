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
