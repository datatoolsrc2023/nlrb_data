import concurrent.futures
import logging

from common import db_config, Connection
import scraper


# set up the log
logging.basicConfig(filename='scrape.log', filemode='a', encoding='utf-8', level=logging.INFO)

def main():
    # use the db's `cases` and `pages` table to get a list of pages to scrape
    cnx = Connection(db_config)
    curs = cnx.cursor()  
    cases = scraper.case_pages_to_fetch(cursor=curs)
    print('remaining to scrape:', len(cases))
    curs.close()
    cnx.close()

    # run the scraper. can tune the `max_workers` for multi-threading.
    # note that each thread/worker opens and closes a connection to the db.
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(scraper.threaded_scraper, cases)

    # if manually ending scraper, update and display the number of cases remaining
    except KeyboardInterrupt:
        print('scrape stopped')

    finally:
        cnx = Connection(db_config)
        curs = cnx.cursor()  
        cases = scraper.case_pages_to_fetch(cursor=curs)
        print(f'stopped with {len(cases)} cases remaining to scrape.')
        curs.close()
        cnx.close()
        


if __name__ == "__main__":
    main()
    
    
