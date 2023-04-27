#!/usr/bin/env python3

from common import db_config, sql
import sys
import pymysql


if __name__ == '__main__':
    """Confirm cases_raw table has rows."""

    count = 0

    with sql.db_cnx() as cnx:
        with cnx.cursor() as c:
            query = f"""
                    SELECT count(*)
                    FROM {db_config.schema}.{db_config.cases_raw};
                    """

            try:
                c.execute(query)
                count = c.fetchone()[0]
                if count == 0:
                    print(f'Expected {db_config.cases_raw}',
                          'table to be populated,',
                          'found 0 records')
                    sys.exit(1)
            except (pymysql.err.ProgrammingError,
                    pymysql.err.OperationalError) as e:
                print(f'Could not count cases: {e}')
