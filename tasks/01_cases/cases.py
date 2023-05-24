#!/usr/bin/env python3

import polars as pl


def clean_data(df: pl.DataFrame) -> pl.DataFrame:
    """
    Takes a polars dataframe,
    renames participants and allegations columns,
    adds docket_activity_raw column and
    converts date_filed and date_closed columns to Datetime
    using polars lazy computation.
    Returns a polars dataframe.
    """
    print('Cleaning data...')
    df = df.lazy().rename({
        'participants': 'participants_raw',
        'allegations': 'allegations_raw'
    }).with_columns(
        [
            pl.lit(None).alias('docket_activity_raw'),
            pl.col('date_filed').str.strptime(pl.Datetime, format='%m/%d/%Y')
            .cast(pl.Datetime),
            pl.col('date_closed').str.strptime(pl.Datetime, format='%m/%d/%Y',
                                               strict=False)
            .cast(pl.Datetime)
        ]
    ).select(
        ['case_type',
         'region',
         'case_number',
         'case_name',
         'case_status',
         'date_filed',
         'date_closed',
         'reason_closed',
         'city',
         'states_and_territories',
         'employees_involved',
         'allegations_raw',
         'participants_raw',
         'docket_activity_raw',
         'union_name',
         'unit_sought',
         'voters'
         ]).sort(by=['case_number', 'date_filed'], descending=True).\
            unique(subset=['case_number'],
                    keep='first', maintain_order=True).collect()

    return df
