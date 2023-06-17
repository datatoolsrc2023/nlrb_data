#!/usr/bin/env python3

from common import db_config, sql


if __name__ == "__main__":
    """Ensure pages table is created."""

    statements = sql.get_query_lines_from_file(f"{db_config.db_type}/pages.sql")

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print("Attempting to create pages table")
            for statement in statements:
                c.execute(statement)
    except Exception as e:
        print(f"Unable to create pages table: {e}")
        raise (e)
    else:  # no exception
        print("Pages table successfully created.")
    finally:
        c.close()
        cnx.close()
