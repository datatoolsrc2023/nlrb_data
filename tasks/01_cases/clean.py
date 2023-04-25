#!/usr/bin/env python3

from common import db_config, sql
import sys


if __name__ == '__main__':
    """Drop cases table."""

    with sql.db_cnx() as cnx:
        cnx.begin()

        # Drop cases table
        with cnx.cursor() as c:
            query = f"""
                    DROP TABLE IF EXISTS
                    {db_config.schema}.{db_config.cases}
                    """
            try:
                print(f'Dropping {db_config.cases} table')
                c.execute(query)
                cnx.commit()
            except Exception as e:
                print(f"Failed to drop {db_config.cases}: {e}")
                sys.exit(1)
