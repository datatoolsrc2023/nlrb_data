import logging
import requests
import time

from bs4 import BeautifulSoup as bs

from common import sql, db_config


def add_page_row(case_id: int, 
                 case_number: str,
                 raw_text: str):
    
    # insert relevant info to pages table in the db
    try:
        if db_config.db_type == 'sqlite':
            query = '''INSERT INTO pages (case_id, case_number, raw_text)
                            VALUES (?, ?, ?)
                        '''
        elif db_config.db_type == 'postgresql':
            query = """INSERT INTO pages (case_id, case_number, raw_text) 
                            VALUES (%s, %s, %s);
                    """
                
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(query, (int(case_id), case_number, raw_text))        
            
    except Exception as e:
        print(f'Error adding page to {db_config.pages} table: {e}')
        raise e
    
    finally:
        c.close()
        cnx.close()


def scraper(case: tuple):
    """
    Fetches an NLRB case page and inserts the relevant .html to the DB
    The `case` parameter is a tuple of (case_id, case_number).
    `case_id` is the FK to the `cases` table primary key column.
    """
        
    # get some useful variables from the inputs
    case_id, case_number = case
    
    # keep track of time
    t1 = time.time()    

    # try to scrape a page. 
    try:
        case_response = requests.get(f'https://www.nlrb.gov/case/{case_number}')
        case_response.raise_for_status()
    
    # if you get an error, log it
    except requests.exceptions.HTTPError as e:
        print(f'Error: {e}, case: {case_number}')
        logging.warning(f'{case_id}, {case_number}, fetch error: {e}')
        raise e
    
    # access the relevant info in the html using beautifulsoup
    soup = bs(case_response.text, 'lxml')
    if soup.article is None:
        logging.warning(f'{case_id}, {case_number}, write error: soup.article is none')
    
    else:

        # write relevant `<article>` section as "raw_text" to pages table,
        # along with `case_id` (fk) and `case_number`
        try:
            add_page_row(case_id=case_id,
                        case_number=case_number,
                        raw_text=soup.article.prettify())
        
        # if you get an error, log it
        except Exception as e:
            print(f'Error: {e}, case: {case_number}')
            logging.warning(f'{case_id}, {case_number}, write error:{e}')
        
        else:
            t2 = time.time()
            logging.info(f'{case_id}, {case_number}, time_elapsed: {round(t2-t1, 3)}')

        