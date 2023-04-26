#!/usr/bin/env python3

from common import db_config, sql
import sys


if __name__ == '__main__':
    """Drop cases_raw table"""

    with sql.db_cnx() as cnx, cnx.cursor() as c:
        query = f"""
                DROP TABLE IF EXISTS
                {db_config.schema}.{db_config.cases_raw}
                """
        try:
            print(f'Dropping {db_config.cases_raw} table')
            c.execute(query)
        except Exception as e:
            print(f"Failed to drop {db_config.cases_raw}: {e}")
            sys.exit(1)
