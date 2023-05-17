from common import Connection, db_config, paths
import os
from scraper import add_to_pages_table
from tqdm import tqdm


"""
had done an initial scrape of JUST pages, wanted to add them to the mysql db, 
while also refactoring, so did this one-off script to add page html files 
to the pages table in the 
"""

def page_files_to_db():
    cnx = Connection(db_config)
    for p_file in tqdm(os.listdir(paths.pages)):
        with open(paths.pages / p_file, 'r', encoding='utf-8') as file_to_write:
            case_id = int(p_file.split('_')[0])
            case_number = p_file.split('_')[1].replace('.html','')
            raw_text = file_to_write.read()
            with cnx.cursor() as curs:
                add_to_pages_table(cursor=curs,
                                case_id=case_id,
                                case_number=case_number,
                                error=False,
                                raw_text=raw_text)
    cnx.commit()
    cnx.close()


if __name__ == '__main__':
    page_files_to_db()

    