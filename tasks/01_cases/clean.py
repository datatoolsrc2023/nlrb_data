#!/usr/bin/env python3

from common import app_config, sql
import sys


if __name__ == '__main__':
    """Drop cases table."""

    with sql.db_cnx() as cnx:
        cnx.begin()

        # Drop cases table
        with cnx.cursor() as c:
            query = f"""
                    DROP TABLE IF EXISTS
                    {app_config.schema}.{app_config.cases}
                    """
            try:
                print(f'Dropping {app_config.cases} table')
                c.execute(query)
                cnx.commit()
            except Exception as e:
                print(f"Failed to drop {app_config.cases}: {e}")
                sys.exit(1)
