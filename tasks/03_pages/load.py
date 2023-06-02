from common import paths
import os
from scraper import add_to_pages_table
from tqdm import tqdm


def main():
    """
    Load zipped, previously scraped `.html` page files into pages table in nlrb_data database.
    Located in nlrb_data/data/pages_files
    """
    print(f"Attempting to load html pages from {paths.pages} into nlrb_data.db...")
    try:
        for p_file in tqdm(os.listdir(paths.pages)):
            with open(paths.pages / p_file, 'r', encoding='utf-8') as file_to_write:
                case_id = int(p_file.split('_')[0])
                case_number = p_file.split('_')[1].replace('.html','')
                raw_text = file_to_write.read()
                add_to_pages_table(case_id=None,
                                case_number=case_number,
                                error=False,
                                raw_text=raw_text)
    except Exception as e:
        print(f"Failed to load html into DB: {e}")

if __name__ == '__main__':
    main()

