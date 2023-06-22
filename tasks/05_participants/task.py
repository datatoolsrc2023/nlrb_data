#!/usr/bin/env python3
from tqdm import tqdm
import participants
from common import db_config, sql
import time


def main():
    participants_query = """
    SELECT c.id as case_id, c.case_number, c.participants_raw, e.participants_parse_error, p.raw_text
FROM cases c
INNER JOIN error_log e ON c.id = e.case_id
LEFT JOIN pages p ON c.id = p.case_id
WHERE c.participants_raw IS NOT NULL
  AND c.participants_raw <> ''
  AND e.participants_parse_error IS NULL
  OR e.participants_parse_error = true
  LIMIT 10000;
    """

    # if code and description are both null in allegations table,
    # then there was an error parsing the raw allegations text
    """error_log_query = 
    UPDATE error_log
    SET participants_parse_error = CASE WHEN code is null and description is null THEN true
                                       WHEN code is not null and description is not null then false
                                       ELSE null
                                       END
    FROM participants
    WHERE error_log.case_id = participants.case_id
    ;
    """

    # query = "SELECT * FROM pages limit 50"
    """Try block here"""
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
            print(f"Pages with participants: {n}")

            print("Processing participants...")
        
    except Exception as e:
        print("unable to query")
        raise e

    else:
        print("queried successfully!")
    finally:
        c.close()
        cnx.close()
    t1 = time.time()
    try:
        with sql.db_cnx() as cnx:
            for row in tqdm(result):
                participants.process_participants(cnx, row)

                # update error_log col of allegations_parse_error table
                # print(f'Attempting to update {db_config.error_log} table...')
                # c.execute(error_log_query)
    except Exception as e:
        raise e
    else:
        print("processed participants successfully!")
    finally:
        cnx.close()
        
    print(f"Completed parsing of {n} rows in  {round(time.time() - t1, 2)}s")


if __name__ == "__main__":
    main()
