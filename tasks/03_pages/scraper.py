import requests
from common import paths, Connection, db_config
from collections import namedtuple
import pymysql
from os import listdir
from pathlib import Path



def case_pages_to_fetch(cursor):
    
    e = None
    try:
        cursor.execute("SELECT id, case_number FROM cases;")
        cases_case_numbers = [x for x in cursor.fetchall()]
        
        cursor.execute("SELECT case_id, case_number FROM pages;")
        pages_case_numbers = [x for x in cursor.fetchall()]

        print('case #s:', len(cases_case_numbers), 'page #s:', len(pages_case_numbers))

        case_numbers_to_search = set(cases_case_numbers) - set(pages_case_numbers)
        print('to search:', len(case_numbers_to_search))

        
        
        return list(case_numbers_to_search)
        
    except pymysql.err.ProgrammingError as e:
        print("Gather from cases table! {e}")
       
        return []

def check_if_page_already_scraped(case_number: str, output_path: str = paths.pages) -> bool:
    extant_pages = listdir(output_path)
    if f"{case_number}.html" in extant_pages:
        return True
    else:
        return False


def check_if_scraped_info_in_db(cursor, case_number: str):
    exeception = None
    try:
        cursor.execute('SELECT COUNT(*) FROM pages WHERE case_number = %s;', 
                       (case_number,))
        count = cursor.fetchone()[0]
        print(count)
        if count == 0:
            return False
        else:
            return True
    except pymysql.err.ProgrammingError as exception:
        print('Check if scraped info in db! {exception}')


def fetch_case_page(case_number: str, output_path: Path = paths.pages) -> tuple():
    fetch_error = False
    
    try:
        case_response = requests.get(f'https://www.nlrb.gov/case/{case_number}')
    
    except Exception as e:
        print(f'Error: {e}')
        fetch_error = True
    
    fetched = {
        'case_number': case_number, 
        'fetch_error': fetch_error,
        'response': case_response,
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
