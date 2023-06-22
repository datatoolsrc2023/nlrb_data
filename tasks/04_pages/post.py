#!/usr/bin/env python3

from common import db_config, sql

if __name__ == "__main__":
    """
    Confirm the scraper has finished by ensuring the cases and pages tables
    have the same number of rows.
    """

    count_query = (
                    "select (select count(*) from cases) - (select count(*) from pages)"
                    " as row_diff;"
                )
                
    print("Checking that pages were scraped successfully.")
    try:
        with sql.db_cnx() as cnx, cnx.cursor() as c:
            c.execute(count_query)
            count = c.fetchone()[0]
        
    except Exception as e:
        raise Exception(f"Could not count rows in {db_config.pages} table: {e}")

    else:  # no exception
        if count == 0:
            print(
                f"All {db_config.cases} successfully scraped "
                f"and inserted into {db_config.pages}."
            )
        else:
            print(
                f"{count} case ids from {db_config.cases} remain to scrape into pages table.  "
                "                Rerun `make task post` to continue scraping."
            )

    finally:
        cnx.close()
