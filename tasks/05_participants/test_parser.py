import participants
from common import sql

import unittest


# Collect some rows from the pages table for testing.
# Examples chosen to cover some common parsing patterns to check.
test_rows_query = """
SELECT case_id, case_number, raw_text 
FROM pages
WHERE case_number 
IN (
    '31-CA-028366', 
    '11-CA-066432', 
    '22-CB-251531', 
    '28-CA-078475', 
    '01-CA-045448',
    '20-CA-123557', 
    '03-CB-009071'
    );
"""

# If the `pages` table doesn't contain these cases,
# randomly select up to 5 rows that have participants.
random_test_rows_query = """
SELECT case_id, case_number, raw_text
FROM pages
WHERE raw_text NOT LIKE '%Participants data is not available%'
AND random() < .1
LIMIT 5;
"""


class TestParseParticipants(unittest.TestCase):
    """
    Collect test cases from the pages table.
    """

    @classmethod
    def setUpClass(cls) -> None:
        with sql.db_cnx() as cls.cnx:
            # First, try to collect default test cases.
            print("Selecting test cases...")
            cls.c = cls.cnx.cursor()
            cls.c.execute(test_rows_query)
            cls.test_cases = cls.c.fetchall()

        # If there aren't enough specified test cases present in the pages table,
        # choose random non-empty rows from the pages table.
        if len(cls.test_cases) < 3:
            cls.c.execute(random_test_rows_query)
            cls.test_cases = cls.c.fetchall()

        print(
            "Test cases (case_id, case_number):\n",
            [(x[0], x[1]) for x in cls.test_cases],
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Close the class's cursor and connection.
        """
        cls.c.close()
        cls.cnx.close()

    def test_pd_raw_participants(self):
        """
        First make sure the pd parser finds the appropriate table.
        If this fails, the test case has no participants.
        """
        for test_text in self.test_cases:
            with self.subTest(test_text=test_text[2]):
                self.assertIsNotNone(participants.pd_parser(test_text[2]))

    def test_matching_cardinality_raw_participants(self):
        """
        Ensure consistency between the two functions for parsing the participants.
        (one uses pandas' read_html(), one parses the raw html using bs4)
        """
        for test_text in self.test_cases:
            with self.subTest(test_text=test_text[2]):
                pd_raw_participants = participants.pd_parser(test_text[2])
                html_raw_participants = participants.html_raw_participants(test_text[2])
                # Uncomment below to see the number of participants
                # found by the pd and html based parsers.
                """
                print(
                   f"lengths of pd:{len(pd_raw_participants)},\
                  html:{len(html_raw_participants)}"
                )
                """
                self.assertEqual(len(pd_raw_participants), len(html_raw_participants))

    def test_parser(self):
        for test_text in self.test_cases:
            with self.subTest(test_text=test_text[2]):
                self.assertIsNotNone(test_text)


if __name__ == "__main__":
    unittest.main()
