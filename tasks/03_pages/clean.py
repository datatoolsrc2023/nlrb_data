import pathlib
import os

from common import sql, paths
from tqdm import tqdm


"""
Makefile removes all .html files with size 0
"""

def clean_table_empties(cursor):
    # remove rows from pages table that have an empty raw_text
    print(f'Checking for and removing rows from `pages` table with an empty text...')
    print('(This may take some time if the pages table is well populated.)')
    try:
        cursor.execute(
            """
            DELETE FROM pages WHERE LENGTH(raw_text) = 0;
            """)

    except Exception as e:
        print(f"Error deleting rows from pages table: {e}")


def scraped_files_clean(cursor, directory: pathlib.Path):
    """
    remove any scraped .html page files that haven't been logged in pages table,
    and subsequently remove any pages rows that don't have a downloaded html file
    """
    print(f'Removing .html files not in pages table, removing rows without downloaded .html.')

    try:
        cursor.execute(
            """
            SELECT case_id FROM pages;
            """
        )
        c_ids = set([x[0] for x in cursor.fetchall()])
        file_ids = set([int(file.split('_')[0]) for file in os.listdir(directory)])
        
        # for each case_id in the pages table,
        # check if there's an associated file with the same case_id
        # if there's not, remove the row
        for c_id in c_ids:
            if c_id not in file_ids:
                cursor.execute(
                    f"""
                    DELETE FROM pages WHERE case_id = {c_id};
                    """
                    )
        
    except Exception as e:
        print(f"Error reading from pages table: {e}")  


    # then for each file,
    # if its id has no match in the table, remove it
    try:
        for file in os.listdir(directory):
            case_id = file.split('_')[0]
            if int(case_id) not in c_ids:
                os.remove(directory / file)
        

    except Exception as e:
        print(f'Error with {file}: {e}')


def main():
    with sql.db_cnx() as cnx:
        c = cnx.cursor()
        clean_table_empties(cursor=c)
        scraped_files_clean(cursor=c, directory=paths.pages)
    c.close()
    cnx.close()


if __name__ == "__main__":
    main()