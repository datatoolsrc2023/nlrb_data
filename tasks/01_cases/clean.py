#!/usr/bin/env python3

from common import app_config, sql
import sys


if __name__ == '__main__':
    """Undo all changes this task might have made."""

    error = False

    with sql.db_cnx() as cnx:

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
                error = True
                print(f"Failed to drop {app_config.cases}: {e}")

        # Drop cases_raw_deduped table
        with cnx.cursor() as c:
            query = f"""
                    DROP TABLE IF EXISTS
                    {app_config.schema}.{app_config.cases_raw_deduped}
                    """
            try:
                print(f'Dropping {app_config.cases_raw_deduped} table')
                c.execute(query)
                cnx.commit()
            except Exception as e:
                error = True
                print(f"Failed to drop {app_config.cases_raw_deduped}: {e}")

    # Exit with error if needed

    if error:
        sys.exit(1)
