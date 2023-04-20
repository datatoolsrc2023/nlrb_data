#!/usr/bin/env python3

import petl as etl
import re


def clean_header(cases_tbl: etl.Table) -> etl.Table:
    """
    Takes a PETL table, replaces spaces and other special characters
    in column names with underscores, changes a few specific column names,
    and makes all column names lowercase. We do this instead of just using
    a dict to rename column headers because we handle two different types
    of cases (Charge and Representation) that have slightly different
    sets of columns.
    """
    header = etl.header(cases_tbl)
    clean_header = [h.replace(' ', '_').replace('&', 'and')
                    .replace('Employees_on_charge/petition',
                             'employees_involved')
                    .replace('Status', 'case_status')
                    .lower() for h in header]
    clean_header = [(re.sub(r'^union$', 'union_name', h))
                    for h in clean_header]
    cases_tbl = etl.setheader(cases_tbl, clean_header)
    return cases_tbl
