#!/usr/bin/env python3
from tqdm import tqdm
import participants
from common import db_config, sql
import time
import logging


# set up a log for diagnostics/debugging
logging.basicConfig(
    filename="participants.log", filemode="a", encoding="utf-8", level=logging.INFO
)


def main():
    # Get the case_id, case_number, raw_participants column from the pages table
    # for cases that have participants.
    # This query can take some time for larger tables.

    participants_query = """
    SELECT p.case_id, p.case_number, p.raw_text
    FROM pages p
    JOIN error_log e ON p.case_id = e.case_id
    WHERE p.raw_text NOT LIKE '%Participants data is not available%'
    AND (e.participants_parse_error IS NULL
    OR e.participants_parse_error = true) LIMIT 1000;
    """

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(query=participants_query)

            if db_config.db_type == "sqlite":
                # sqlite3 doesn't make a rowcount attribute available
                # so to get the row count, we have to fetch all rows and
                # get the len() of the result
                result = c.fetchall()
                n = len(result)
            elif db_config.db_type == "postgresql":
                # getting the postgresql rowcount attribute is
                # less memory intensive than fetching all rows
                result = c
                n = c.rowcount
                result = result.fetchall()

    except Exception as e:
        print("Unable to query database.")
        logging.warning("Unable to query database..")
        raise e

    else:
        print("Database queried successfully!")
        print(f"Pages with participants: {n}")
    finally:
        # Tearing down the connection/cursor may take some time.
        print("closing cursor")
        c.close()
        print("closing connection")
        cnx.close()

    print("Processing participants...")
    t1 = time.time()
    try:
        with sql.db_cnx() as cnx:
            for row in tqdm(result):
                participants.process_participants(cnx, row)

    except Exception as e:
        c = cnx.cursor()
        c.execute("select count(*) from pages;")
        row_count = len(c.fetchall())
        t = time.time() - t1
        part_rate = round((n - row_count) / t, 2)
        logging.warning(
            f"Parsed {row_count} rows out of {n} in {round(t, 2)}s: {part_rate} p/s."
        )

        raise e
    else:
        print("...participants processed successfully!")
    finally:
        cnx.close()

    t = time.time() - t1
    logging.info(
        f"Parsed {n} rows in {round(t, 2)} seconds." f" ({round(n/t1,2)} rows/sec)"
    )


if __name__ == "__main__":
    main()
