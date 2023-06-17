#!/usr/bin/env python3

from common import db_config, sql


if __name__ == "__main__":
    """Confirm database meets expectations."""

    cases_query = "SELECT COUNT(*) from cases;"
    pages_query = "SELECT COUNT(*) from pages;"

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(cases_query)
            count = c.fetchone()[0]
            if count == 0:
                raise Exception(
                    f"Expected {db_config.cases} table to be populated"
                    "found 0 records."
                )
            c.execute(pages_query)
            count = c.fetchone()[0]
            if count != 0:
                raise Exception(
                    f"Expected {db_config.pages} table to be empty, "
                    f"found {count} records."
                )
    except Exception as e:
        print("Issue communicating with db.")
        raise e
    else:
        print(
            f"{db_config.cases} and {db_config.pages} "
            "cases and pages tables expectations met."
        )
    finally:
        c.close()
        cnx.close()
