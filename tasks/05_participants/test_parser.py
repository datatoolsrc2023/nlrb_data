#!/usr/bin/env python3

import participants
from common import sql

import unittest

random_row_query = """
select c.id as case_id, c.case_number, p.raw_text 
from cases c 
left join pages p on c.id = p.case_id
where c.participants_raw IS NOT NULL
order by random() limit 1;
"""

with sql.db_cnx() as cnx:
    c = cnx.cursor()
    c.execute(random_row_query)
    test_row = c.fetchone()
    print("Test case:", test_row[0], test_row[1])


class TestParseParticipants(unittest.TestCase):
    def test_matching_cardinality_raw_participants(self):
        """
        Ensure the two functions for parsing the participants
        (one uses pandas' read_html(), one parses the raw html using bs4)
        """
        pd_raw_participants = participants.pd_raw_participants(test_row[2])
        html_raw_participants = participants.html_raw_participants(test_row[2])
        print(
            f"lengths of pd:{len(pd_raw_participants)}, html:{len(html_raw_participants)}"
        )
        self.assertEqual(len(pd_raw_participants), len(html_raw_participants))


class TestParticipantHtmlParse(unittest.TestCase):
    def test_html_participants_parse(self):
        test_case = participants.html_raw_participants(test_row[2])
        self.assertIsNotNone(participants.html_parse_participant(test_case))

    """
    def test_html_parse_3_br(self):
        test_case = participants.html_raw_participants(test_case[1])
        #print(participants.html_raw_participants(test_case2))
        self.assertIsNotNone(participants.html_parse_participant(test_case))
    """


class TestParticipantPdParse(unittest.TestCase):
    def test_pd_participants_columns(self):
        result = participants.pd_raw_participants(test_row[2])
        # print(result)

        self.assertIsNotNone(result)


class TestParticipantParse(unittest.TestCase):
    def test_parser(self):
        result = participants.parse_participant(test_row[2])
        # print(result)

        self.assertIsNotNone(result)

    """
    def test_process(self):
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            random_row_query = "select case_id, case_number, raw_text from pages order by random() limit 1;"
            c.execute(random_row_query)
            test_case = c.fetchone()
            print('process:', test_case['case_number'])
            participants.process_participants(cursor=c, case_row=test_case)
            u

        c.close()
        cnx.close()
    """


if __name__ == "__main__":
    unittest.main()
    c.close()
    cnx.close()
