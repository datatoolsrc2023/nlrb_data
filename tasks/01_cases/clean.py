#!/usr/bin/env python3

from common import app_config, sql
import sys


if __name__ == '__main__':
    """Undo all changes this task might have made."""

    cnx = sql.db_cnx()
    cnx.begin()
    c = cnx.cursor()

    # Drop cases table
    error = False
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

    # Clean up gracefully, then exit with error if needed
    c.close()
    cnx.close()

    if error:
        sys.exit(1)
