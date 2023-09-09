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
    participants_query = """
    SELECT c.id as case_id, c.case_number, c.participants_raw, e.participants_parse_error, p.raw_text
FROM cases c
INNER JOIN error_log e ON c.id = e.case_id
LEFT JOIN pages p ON c.id = p.case_id
WHERE p.raw_text IS NOT NULL
  AND p.raw_text <> ''
  AND e.participants_parse_error IS NULL
  OR e.participants_parse_error = true
  limit 1000;
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
        logging.warning(f"Unable to query database..")
        raise e

    else:
        print("Database queried successfully!")
        print(f"Pages with participants: {n}")
        print("Processing participants...")
    finally:
        c.close()
        cnx.close()

    t1 = time.time()
    try:
        with sql.db_cnx() as cnx:
            for row in tqdm(result):
                participants.process_participants(cnx, row)

    except Exception as e:
        c = cnx.cursor()
        c.execute("select count(*) from pages;")
        t = time.time() - t1
        part_rate = round((n - c.rowcount) / t, 2)
        logging.warning(
            f"Parsed {c.rowcount} rows out of {n} in {round(t, 2)}s: {part_rate}p/s."
        )

        raise e
    else:
        print("...participants processed successfully!")
    finally:
        cnx.close()
    logging.info(f"Completed parsing of {n} rows in {round(time.time() - t1, 2)}")


if __name__ == "__main__":
    main()
