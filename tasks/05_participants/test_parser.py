#!/usr/bin/env python3

import participants
from common import paths
import os
import random
from common import db_config, sql

import unittest



class TestParseParticipants(unittest.TestCase):
    """def test_participants_parse(self):
        n = random.choice(range(len(test_html_files)))
        print(f'testing {test_html_files[n]}')
        test_case = paths.pages / test_html_files[n]
        with open(test_case, 'r') as test_html:
            expected = str
            got = participants.parse_participants_str(test_html.read())
        self.assertEqual(got, expected)
    """
    def test_matching_cardinality_raw_participants(self):
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            random_row_query = """select raw_text from pages order by random() limit 1;"""
            c.execute(random_row_query)
            test_case = c.fetchone()[0]   
        c.close()
        cnx.close()

        pd_raw_participants = participants.pd_raw_participants(test_case)
        html_raw_participants = participants.html_raw_participants(test_case)         
        print(f"pd:{len(pd_raw_participants)}, html:{len(html_raw_participants)}")
        self.assertEqual(len(pd_raw_participants), len(html_raw_participants))


class TestParticipantHtmlParse(unittest.TestCase):
    def test_html_participants_parse(self):
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            random_row_query = """select case_number, raw_text from pages order by random() limit 1;"""
            c.execute(random_row_query)
            test_case = c.fetchone()
            print('test_case:', test_case[0])
        c.close()
        cnx.close()
        test_case = participants.html_raw_participants(test_case[1])
        #print(participants.html_raw_participants(test_case2))
        self.assertIsNotNone(participants.html_parse_participant(test_case))

    def test_html_parse_3_br(self):
        test_case = participants.html_raw_participants(test_case[1])
        #print(participants.html_raw_participants(test_case2))
        self.assertIsNotNone(participants.html_parse_participant(test_case))
"""
    def test_valid_four_point_code(self):
        test_case = "8(b)(1)(A) Duty of Fair Representation, incl'g Superseniority, denial of access"
        expected = allegations.Row(
                code="8(b)(1)(A)",
                desc="Duty of Fair Representation, incl'g Superseniority, denial of access",
                parse_error=False,
                raw=test_case
                )
        got = allegations.parse_line(test_case)
        self.assertEqual(got, expected)

    def test_invalid_code_fails(self):
        test_case = "8(8)(1)(A) Duty of Fair Representation, incl'g Superseniority, denial of access"
        expected = allegations.Row(
                code=None,
                desc=None,
                parse_error=True,
                raw=test_case
                )
        got = allegations.parse_line(test_case)
        self.assertEqual(got, expected)

    def test_code_index_multiple_digits(self):
        test_case = '8(b)(11)(A) Something I made up'
        expected = allegations.Row(
                code='8(b)(11)(A)',
                desc='Something I made up',
                parse_error=False,
                raw=test_case
                )
        got = allegations.parse_line(test_case)
        self.assertEqual(got, expected)
"""
"""
class TestParseAllegations(unittest.TestCase):
    def test_multiple_valid_allegations(self):
        test_case = "8(a)(3) Discharge (Including Layoff and Refusal to Hire (not salting))
        8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
        8(a)(1) Coercive Statements (Threats, Promises of Benefits, etc.)
        "
        got = list(allegations.parse_lines(test_case))
        self.assertEqual(len(got), 3)
        self.assertTrue(all(not r.parse_error for r in got))

    def test_trailing_whitespace(self):
        test_case = "8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
        "
        got = list(allegations.parse_lines(test_case))
        self.assertEqual(len(got), 1)
        self.assertFalse(got[0].parse_error)

    def test_ignore_empty_lines(self):
        test_case = "8(a)(1) Coercive Rules

        8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
        "
        got = list(allegations.parse_lines(test_case))
        self.assertEqual(len(got), 2)
        self.assertTrue(all(not r.parse_error for r in got))

    def test_mix_of_success_and_error(self):
        test_case = "8(2)(1) Coercive Rules
        8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
        "
        got = list(allegations.parse_lines(test_case))
        self.assertEqual(len(got), 2)
        self.assertTrue(got[0].parse_error)
        self.assertFalse(got[1].parse_error)
"""

if __name__ == '__main__':
    unittest.main()
