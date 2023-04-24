from common import db_config, Connection

import scraper
from tqdm import tqdm


def main():
    cnx = Connection(db_config)
    curs = cnx.cursor()  
    cases = scraper.case_pages_to_fetch(cursor=curs)
    # print(len(cases))
    for case_id,number in tqdm(cases):
        scraped_status = scraper.check_if_page_already_scraped(case_number=number)
        stored_status = scraper.check_if_scraped_info_in_db(cursor=curs, case_number=number)
        if scraped_status == False and stored_status == False:
            fetched = scraper.fetch_case_page(case_number=number)
            written = scraper.write_case_page(case_number=number, raw_page=fetched['response'])
            scraper.add_to_pages_table(cursor=curs,
                                       case_id=case_id, 
                                       case_number=number, 
                                       fetch_error=fetched['fetch_error'], 
                                       write_error=written['write_error'])
            cnx.commit()
    curs.close()
    cnx.close()     


if __name__ == "__main__":
    main()