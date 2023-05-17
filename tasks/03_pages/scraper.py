import logging
import pymysql
import requests
import time

from bs4 import BeautifulSoup as bs
from pathlib import Path

from common import paths, Connection, db_config


def case_pages_to_fetch(cursor: Connection.cursor) -> list:
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
        
    except pymysql.err.ProgrammingError as e:
        print("Error gathering case numbers from tables: {e}")
        return []


def add_to_pages_table(cursor: Connection.cursor, 
                       case_id: int, 
                       case_number: str,
                       error: bool,
                       raw_text: str):
    
    # insert relevant info to pages table in the db
    try:
        cursor.execute('''INSERT INTO pages (case_id, case_number, error, raw_text)
                              VALUES (%s, %s, %s, %s);
                              ''',
                              (int(case_id), case_number, error, raw_text)
        )        
    except pymysql.err.Error as e:
        print(f'Error: {e}')
    
    return



def threaded_scraper(case_and_case_number: tuple,
                     output_dir: Path = paths.pages,
                     cnx: Connection = Connection(db_config)):
    # scraper doesn't necessarily need to be run in threads
    
    
    # get some useful variables from the inputs
    case_id, case_number = case_and_case_number
    output_path = Path(output_dir/f"{case_id}_{case_number}.html")
    
    # check if the page has already been scraped
    # will be able to refactor this out into the earlier case number gathering step
    # once get the logging read and db pages table updated
    if output_path.is_file() is True:
        return

    # keep track of time
    t1 = time.time()    

    # set up cursor to DB, will close 
    curs = cnx.cursor()

    # try to scrape a page. 
    try:
        case_response = requests.get(f'https://www.nlrb.gov/case/{case_number}')
        case_response.raise_for_status()
    
    # if you get an error, log it, add error to `pages` table, return out of scraper
    except requests.exceptions.HTTPError as e:
        print(f'Error: {e}, case: {case_number}')
        logging.warning(f'{case_id}, {case_number}, fetch error: {e}')
        add_to_pages_table(cursor=curs, 
                           case_id=case_id, 
                           case_number=case_number,
                           error=True,
                           raw_text=False)
        curs.close()
        cnx.commit()
        cnx.close()
        return

    # then try to parse the requests respose, write relevant `<article>` section to an `.html` file
    try:
        soup = bs(case_response.text, 'lxml')
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(soup.article.prettify())
            add_to_pages_table(cursor=curs, 
                           case_id=case_id, 
                           case_number=case_number,
                           error=False,
                           raw_text=soup.article.prettify())
    
    # if you get an error, log it, add error to `pages` table, return out of scraper
    except Exception as e:
        print(f'Error: {e}, case: {case_number}')
        logging.warning(f'{case_id}, {case_number}, write error:{e}')
        add_to_pages_table(cursor=curs, 
                           case_id=case_id, 
                           case_number=case_number,
                           error=True,
                           raw_text=False)
        curs.close()
        cnx.commit()
        cnx.close()
        return

    # then commit the page to  to the db and record in log    
    t2 = time.time()
    logging.info(f'{case_id}, {case_number}, time_elapsed: {round(t2-t1, 3)}')
    
    # commit and close
    curs.close()
    cnx.commit()
    cnx.close()

