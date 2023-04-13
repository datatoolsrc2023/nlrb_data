#!/usr/bin/env python3

from common import app_config, sql
import sys


if __name__ == '__main__':
    """Undo all changes this task might have made."""

    error = False

    cnx = sql.db_cnx()
    cnx.begin()
    c = cnx.cursor()

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
        error = True
        print(f"Failed to drop {app_config.cases_raw}: {e}")

    # Clean up gracefully, then exit with error if needed
    c.close()
    cnx.close()

    if error:
        sys.exit(1)
