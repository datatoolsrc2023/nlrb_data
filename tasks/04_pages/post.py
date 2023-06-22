#!/usr/bin/env python3

from common import db_config, sql

if __name__ == "__main__":
    """
    Confirm the scraper has finished by ensuring all case_ids from the cases table
    appear in the pages table.
    """

    count_query = (
                    "select (select count(*) from cases) - (select count(*) from pages)"
                    " as row_diff;"
                )
                

    try:
        with sql.db_cnx() as cnx, cnx.cursor() as c:
            c.execute(count_query)
            count = c.fetchone()[0]
            """
            so, basically just instead of doing a big comparison,
            it's like....if count is 0, you're done!
            but if there's an error, just catch it here.
            """
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
                f"{count} case ids {db_config.cases} left to scrape into pages table.  "
                "                Rerun `make` to continue scraping."
            )

    finally:
        cnx.close()
