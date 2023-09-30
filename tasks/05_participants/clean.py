#!/usr/bin/env python3

from common import db_config, sql


if __name__ == "__main__":
    """Undo all changes this task might have made."""

    # First, drop the participants table.
    drop_query = "DROP TABLE IF EXISTS participants"

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(f"Attempting to drop {db_config.participants} table...")
            c.execute(drop_query)
    except Exception as e:
        raise Exception(f"Failed to drop {db_config.participants} table") from e
    else:  # no exception
        print(f"Dropped {db_config.participants} table")

    finally:
        c.close()
        cnx.close()

    # Then reset any entries in the error_log that occurred during this task.
    error_query = "UPDATE error_log SET participants_parse_error = NULL"

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print(
                f"Attempting to clean {db_config.error_log} table's "
                "participants_parse_error column..."
            )
            c.execute(error_query)
    except Exception as e:
        raise Exception(f"Failed to clean {db_config.error_log} table") from e
    else:  # no exception
        print(f"Successfully cleaned {db_config.error_log} table")

    finally:
        c.close()
        cnx.close()
