import requests
from common import paths
from collections import namedtuple


def fetch_case_page(case_number: str) -> tuple():
    fetch_error = None
    
    try:
        page = requests.get(f'https://www.nlrb.gov/case/{case_number}')
    
    except Exception as e:
        print(f'Error: {e}')
        fetch_error = e


    write_error = None
    
    output_path = paths.data / f"page_files/{case_number}.html"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(page.text)
    
    except Exception as e:
        print(f'Error: {e}')
        write_error=e
    
    Page = {'case_number': case_number, 
            'fetch_error': fetch_error,
            'write_error': write_error,}

    return Page


def write_to_database():