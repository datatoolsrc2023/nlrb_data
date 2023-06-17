#!/usr/bin/env python3

from common import db_config, sql
if __name__ == '__main__':
    """
    Cofirm the scraper has finished by ensuring all case_ids from the cases table
    appear in the pages table.
    """

    pages_query = 'SELECT count(case_id) FROM pages'
    comparison_query = """
                SELECT t1.id FROM cases t1 
                    LEFT JOIN pages t2 ON t1.id = t2.case_id 
                    WHERE t2.case_id IS NULL;
                    """

    try:
        with sql.db_cnx() as cnx, cnx.cursor() as c:
            c.execute(pages_query)
            count = c.fetchone()[0]
            if count == 0:
                raise Exception(f'Expected {db_config.pages} table '
                                'to be populated, '
                                'but found 0 records')
    except Exception as e:
        raise Exception(f'Could not count rows in {db_config.pages} table: {e}')
    
    try:
        with cnx.cursor() as c:
            c.execute(comparison_query)
            remaining_cases = [x for x in c.fetchall()]
            count = len(remaining_cases)

    except Exception as e:
        raise Exception(f'Could not count reamining pages to scrape: {e}')
    
    else: # no exception
        if count == 0:
            print(f'All {db_config.cases} successfully scraped and inserted into {db_config.pages}.')
        else: 
            print(f'{count} case ids {db_config.cases} left to scrape into pages table.\
                  Rerun `make` to continue scraping.')
        
    finally:
        cnx.close()
    