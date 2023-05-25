import concurrent.futures
import logging
import sys

from common import sql
import scraper


# set up the log
logging.basicConfig(filename='scrape.log', filemode='a', encoding='utf-8', level=logging.INFO)

def main():
    # use the db's `cases` and `pages` table to get a list of pages to scrape
    with sql.db_cnx() as cnx, cnx.cursor() as c:
        print('Fetching cases left to scrape.')
        cases = scraper.case_pages_to_fetch(cursor=c)
        if len(cases) == 0:
            c.close()
            
            
            print('Scrape completed.')
            return 

        print('...remaining to scrape:', len(cases))
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
        with sql.db_cnx() as cnx, cnx.cursor() as curs:
            print('===============================\nTidying up post-scrape.')
            scraper.clean_empty_text_rows(cursor=curs)
            cases = scraper.case_pages_to_fetch(cursor=curs)
            print(f'Scrape stopped with {len(cases)} cases remaining.')
        
        cnx.close()
        # sys.exit(0)
        


if __name__ == "__main__":
    main()
    
    
