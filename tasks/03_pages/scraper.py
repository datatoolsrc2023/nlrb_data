import logging
import os
import requests
import time

from bs4 import BeautifulSoup as bs
from pathlib import Path

from common import paths, sql, db_config


def case_pages_to_fetch(cursor) -> list:
    try:
        # use a join to find all case ids from `cases` table
        # that are not yet in the scraped `pages` table
        cursor.execute(
            """
            SELECT t1.id, t1.case_number
            FROM cases t1
                LEFT JOIN pages t2 ON t1.id = t2.case_id
                WHERE t2.case_id IS NULL;
            """)
        
        # return a list of all case ids and numbers
        return [x for x in cursor.fetchall()]
        
    except Exception as e:
        print("Error gathering case numbers from tables: {e}")
        return []


def add_to_pages_table(case_id: int, 
                       case_number: str,
                       error: bool,
                       raw_text: str):
    
    # if loading extant .html page files, get case_id from cases table
    if case_id is None:
        try:
            with sql.db_cnx() as cnx:
                c = cnx.cursor()
                c.execute(f"""
                        SELECT t1.id
                        FROM cases t1
                        WHERE t1.case_number = '{case_number}';
                        """)
                case_id = c.fetchone()
                c.close()
                cnx.close()
        except Exception as e:
            print(f'Error with case_id as None: {e}')

    # insert relevant info to pages table in the db
    try:
        if db_config.db_type == 'sqlite':
                query = '''INSERT INTO pages
                            (case_id, case_number, error, raw_text)
                            VALUES (?, ?, ?, ?)
                        '''
        elif db_config.db_type == 'postgresql':
            query = """INSERT INTO pages (case_id, case_number, error, raw_text) 
                            VALUES (%s, %s, %s, %s);
                    """
                
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(query, (int(case_id), case_number, error, raw_text))        
            
    except Exception as e:
        print(f'Error adding page to {db_config.pages} table: {e}')
    finally:
        c.close()
        cnx.close()


def threaded_scraper(case_and_case_number: tuple):
    """
    
    """
    # scraper doesn't necessarily need to be run in threads
    
    # get some useful variables from the inputs
    case_id, case_number = case_and_case_number
    output_path = Path(paths.pages/f"{case_id}_{case_number}.html")
    
    # keep track of time
    t1 = time.time()    


    # try to scrape a page. 
    try:
        case_response = requests.get(f'https://www.nlrb.gov/case/{case_number}')
        case_response.raise_for_status()
    
    # if you get an error, log it, add error to `pages` table, return out of scraper
    except requests.exceptions.HTTPError as e:
        print(f'Error: {e}, case: {case_number}')
        logging.warning(f'{case_id}, {case_number}, fetch error: {e}')
        
        add_to_pages_table(case_id=case_id, 
                           case_number=case_number,
                           error=True,
                           raw_text=False)
        return
    
    soup = bs(case_response.text, 'lxml')
    if soup.article is None:
        print(f'Soup.article is none for: {case_number}')
        logging.warning(f'{case_id}, {case_number}, write error:{soup.article.prettify()}')
        add_to_pages_table(case_id=case_id,
                               case_number=case_number,
                               error=True,
                               raw_text=False)
        return

    page = soup.article.prettify()
    
    # then try to parse the requests respose, write relevant `<article>` section to an `.html` file
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(page)
            add_to_pages_table(case_id=case_id, 
                               case_number=case_number,
                               error=False,
                               raw_text=page)
        t2 = time.time()
        logging.info(f'{case_id}, {case_number}, time_elapsed: {round(t2-t1, 3)}')
    
    # if you get an error, log it, add error to `pages` table, return out of scraper
    except Exception as e:
        print(f'Error: {e}, case: {case_number}')
        logging.warning(f'{case_id}, {case_number}, write error:{e}')
        add_to_pages_table(case_id=case_id, 
                           case_number=case_number,
                           error=True,
                           raw_text=False)
        raise e


def clean_empty_text_rows(cursor):
    # first get a list of all cases with empty raw_text
    try:
        print('- removing .html files where raw_text length in pages table is 0.')
        cursor.execute(
            """
            SELECT * FROM pages WHERE LENGTH(raw_text) = 0;
            """)
        
        # return a list of all case ids and numbers
        case_id_and_number = [x for x in cursor.fetchall()]

        for case_id, case_number in case_id_and_number:
            os.remove(Path(paths.pages/f"{case_id}_{case_number}.html"))

        
    except Exception as e:
        print("Error gathering case numbers from tables: {e}")        
        
    # then delete the pages from the sql table
    try:
        print('- removing rows from pages table where raw_text length is 0.')
        cursor.execute(
            """
            DELETE FROM pages WHERE LENGTH(raw_text) = 0;
            """)

    except Exception as e:
        print("Error deleting rows from pages table: {e}")

        