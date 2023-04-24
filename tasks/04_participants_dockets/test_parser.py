#!/usr/bin/env python3

import participants

import re
import unittest

class TestParseParticipants(unittest.TestCase):
    def test_three_point_code(self):
        test_case = '8(a)(3) Discharge (Including Layoff and Refusal to Hire (not salting))'
        expected = allegations.Row(
                code='8(a)(3)',
                desc='Discharge (Including Layoff and Refusal to Hire (not salting))',
                parse_error=False,
                raw=test_case
                )
        got = allegations.parse_line(test_case)
        self.assertEqual(got, expected)

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


class TestParseAllegations(unittest.TestCase):
    def test_multiple_valid_allegations(self):
        test_case = """8(a)(3) Discharge (Including Layoff and Refusal to Hire (not salting))
        8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
        8(a)(1) Coercive Statements (Threats, Promises of Benefits, etc.)
        """
        got = list(allegations.parse_lines(test_case))
        self.assertEqual(len(got), 3)
        self.assertTrue(all(not r.parse_error for r in got))

    def test_trailing_whitespace(self):
        test_case = """8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
        """
        got = list(allegations.parse_lines(test_case))
        self.assertEqual(len(got), 1)
        self.assertFalse(got[0].parse_error)

    def test_ignore_empty_lines(self):
        test_case = """8(a)(1) Coercive Rules

        8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
        """
        got = list(allegations.parse_lines(test_case))
        self.assertEqual(len(got), 2)
        self.assertTrue(all(not r.parse_error for r in got))

    def test_mix_of_success_and_error(self):
        test_case = """8(2)(1) Coercive Rules
        8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
        """
        got = list(allegations.parse_lines(test_case))
        self.assertEqual(len(got), 2)
        self.assertTrue(got[0].parse_error)
        self.assertFalse(got[1].parse_error)


if __name__ == '__main__':
    unittest.main()
