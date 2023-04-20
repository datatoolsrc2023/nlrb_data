import requests
from common import paths, Connection, db_config
from collections import namedtuple
import pymysql
from time import sleep
from os import listdir
from pathlib import Path


def gather_case_numbers_from_cases_table(cursor):
    
    e = None
    try:
        curs.execute("SELECT id, case_number FROM cases;")
        case_numbers = [x for x in curs.fetchall()]
        
        return list(set(case_numbers))
        
    except pymysql.err.ProgrammingError as e:
        print("Error! {e}")
       
        return []

def check_if_page_already_scraped(case_number: str, output_path: str = paths.pages) -> bool:
    extant_pages = listdir(output_path)
    if f"{case_number}.html" in extant_pages:
        return True
    else:
        return False


def fetch_case_page(case_number: str, output_path: Path = paths.pages) -> tuple():
    if check_if_page_already_scraped(output_path):
        return None
    
    fetch_error = False
    
    try:
        page = requests.get(f'https://www.nlrb.gov/case/{case_number}')
    
    except Exception as e:
        print(f'Error: {e}')
        fetch_error = True
    
    fetched = {
        'case_number': case_number, 
        'fetch_error': fetch_error,
        'raw_page': page,
     }

    return fetched


def write_case_page(case_number: str, raw_page: str, output_path: Path = paths.pages) -> tuple():
    write_error = False
    
    output_path = output_path / f"{case_number}.html"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(raw_page.text)
    
    except Exception as e:
        print(f'Error: {e}')
        write_error=True
    
    written = {'case_number': case_number, 
            'write_error': write_error,}

    return written



def add_to_pages_table(cursor, 
                       case_id: int, 
                       case_number: str, 
                       fetch_error: bool, 
                       write_error: bool):
    
    try:
        cursor.execute('''INSERT INTO pages (case_id, case_number, fetch_error, write_error)
                              VALUES (%s, %s, %s, %s);
                              ''',
                              (case_id, case_number, fetch_error, write_error)
        )        

    except pymysql.err.Error as e:
        print(f'Error: {e}')
    
        
      


cnx = Connection(db_config)
curs = cnx.cursor()  
cases = gather_case_numbers_from_cases_table(cursor=curs)
for case_id,number in cases:
    scraped_status = check_if_page_already_scraped(case_number=number)
    print(number, 'scraped_status:', scraped_status)
    if scraped_status == False:
        fetched = fetch_case_page(case_number=number)
        written = write_case_page(case_number=number, raw_page=fetched['raw_page'])
        add_to_pages_table(cursor=curs, 
                           case_id=case_id, 
                           case_number=number, 
                           fetch_error=fetched['fetch_error'], 
                           write_error=written['write_error'])

curs.close()
cnx.commit()
cnx.close()

# add_to_pages_table(curs, case_id=1618, case_number='28-CA-212340', fetch_error=False, write_error=False)
