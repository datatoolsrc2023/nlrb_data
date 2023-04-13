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
