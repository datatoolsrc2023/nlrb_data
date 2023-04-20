#!/usr/bin/env python3

from common import app_config, sql
import sys


if __name__ == '__main__':
    """Drop cases_raw table"""

    with sql.db_cnx() as cnx:
        cnx.begin()
        with cnx.cursor() as c:
            # Drop raw cases table
            query = f"""
                    DROP TABLE IF EXISTS
                    {app_config.schema}.{app_config.cases_raw}
                    """
            try:
                print(f'Dropping {app_config.cases_raw} table')
                c.execute(query)
                cnx.commit()
            except Exception as e:
                print(f"Failed to drop {app_config.cases_raw}: {e}")
                sys.exit(1)
