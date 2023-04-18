import scraper

import unittest


class TestScraper(unittest.TestCase):
    def test_scrape(self):
        test_case = '28-CA-212340'
        expected = {
            'case_number': test_case, 
            'fetch_error': None,
            'write_error': None,
        }
        got = scraper.fetch_case_page(test_case)
        self.assertEqual(got, expected)


if __name__ == '__main__':
    unittest.main()
