import concurrent.futures
import logging

from common import sql
import scraper


# set up the log
logging.basicConfig(
    filename="scrape.log", filemode="a", encoding="utf-8", level=logging.INFO
)

# define how many threads/workers to scrape simultaneously
max_workers = 5


def main():
    query = """
            SELECT t1.id, t1.case_number
            FROM cases t1
                LEFT JOIN pages t2 ON t1.id = t2.case_id
                WHERE t2.case_id IS NULL;
            """

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            print("Fetching cases left to scrape.")
            c.execute(query)
            cases = [x for x in c.fetchall()]
    except Exception as e:
        print("Unable to gather remaining cases.")
        raise (e)
    else:  # no exception
        if len(cases) == 0:
            print("Scrape already completed.")
            return
        else:
            print("...remaining to scrape:", len(cases))
    finally:
        c.close()
        cnx.close()

    # run the scraper. can tune the `max_workers` for multi-threading.
    # note that each thread/worker opens and closes a connection to the db.
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(scraper.scraper, cases)

    # if manually ending scraper, update and display the number of cases remaining
    except KeyboardInterrupt:
        print("Scrape stopped!")
        executor.shutdown(cancel_futures=True, wait=False)

    else:
        print("Task completed.")

    # Whether the task has completed or been manually stopped,
    # do some tidying, and check how many cases remain to scrape.
    finally:
        try:
            with sql.db_cnx() as cnx:
                print("Attempting to count remaining cases and clean empty rows...")
                c = cnx.cursor()

                # remove any rows with an empty raw_text
                c.execute(
                    """
                    DELETE FROM pages WHERE raw_text = '';
                    """
                )

                # then count how many cases remain to scrape
                count_query = (
                    "select (select count(*) from cases) - (select count(*) from pages)"
                    " as row_diff;"
                )
                c.execute(count_query)
                num_cases = c.fetchone()[0]

        except Exception as e:
            print("Unable to count remaining case pages or unable to clean empty rows.")
            raise e
        else:
            print("Successfully cleaned empty rows.")
            print(f"Remaining cases to scrape: {num_cases}")
        finally:
            c.close()
            cnx.close()


if __name__ == "__main__":
    main()
