#!/usr/bin/env python3

from common import db_config, sql
import sys


if __name__ == '__main__':
    """Drop cases table."""

    cnx = sql.db_cnx()

        # Drop cases table
    c = cnx.cursor()
    query = f"""
            DROP TABLE IF EXISTS
            {db_config.cases}
            """
    try:
        print(f'attempting to drop {db_config.cases} table')
        c.execute(query)
    except:
        raise ValueError(f"Failed to drop {db_config.cases}")
    else: # no exception
        cnx.commit()
        print('dropped table')
    finally:
        cnx.close()
