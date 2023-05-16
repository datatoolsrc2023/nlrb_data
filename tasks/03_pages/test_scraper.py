import unittest

import scraper
from common import Connection, db_config, paths



class TestCaseChecker(unittest.TestCase):
    def test_pages_to_fetch(self):
        cnx = Connection(db_config)
        curs = cnx.cursor()  
        cases = scraper.case_pages_to_fetch(cursor=curs, pages_dir=paths.pages)
        print('Number of cases to scrape:', len(cases))
        curs.close()
        cnx.close()
    

"""
class TestScraper(unittest.TestCase):
    def test_scrape(self):
        test_case = '28-CA-212340'
        expected = {
            'case_number': test_case, 
            'fetch_error': None,
        }
        got = scraper.fetch_case_page(test_case)
        self.assertEqual(got, expected)

    def test_bad_case_number(self):
        test_case = 'asd'
        expected = {
            'case_number': test_case, 
            'fetch_error': True,
            'write_error': True,
        }
        got = scraper.fetch_case_page(test_case)
        self.assertEqual(got, expected)
    
    def test_already_scraped(self):
            test_case = {'case_number': 'test_page',
                         'output_path': ''}
            expected = True
            got = scraper.case_pages_to_fetch(test_case)
            self.assertEqual(got, expected)
    
    def test_not_yet_scraped(self):
            test_case = {'case_number': 'abcd',
                         'output_path': ''}
            expected = False
            got = scraper.check_if_page_already_scraped(test_case)
            self.assertEqual(got, expected)
"""         



"""
class TestWriter(unittest.TestCase):
    def test_write(self):
        test_case = '28-CA-212340'
        expected = {
            'case_number': test_case, 
            'fetch_error': None,
            'write_error': None,
        }
        got = scraper.fetch_case_page(test_case)
        self.assertEqual(got, expected)
"""

if __name__ == '__main__':
    unittest.main()
