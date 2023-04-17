#!/usr/bin/env python3

from common import app_config, sql
import sys


if __name__ == '__main__':
    """Undo all changes this task might have made."""

    error = False

    with sql.db_cnx() as cnx:
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
                # TODO can we call sys.exit(1) below the print statement?
                error = True
                print(f"Failed to drop {app_config.cases_raw}: {e}")

    # Exit gracefully if needed
    if error:
        sys.exit(1)
