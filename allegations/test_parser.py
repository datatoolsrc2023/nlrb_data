#!/usr/bin/env python3

import allegations

import re
#import unittest
#TODO Consider converting to use unittest
# For now, I appreciate having the large test harness

def test_regex():
    regex_tests = [
            {
                'description': 'Valid 3-term allegation',
                'case': '8(a)(3) Discharge (Including Layoff and Refusal to Hire (not salting))',
                'expected': ('8(a)(3)', 'Discharge (Including Layoff and Refusal to Hire (not salting))')
            },
            {
                'description': 'Valid 4-term allegation',
                'case': "8(b)(1)(A) Duty of Fair Representation, incl'g Superseniority, denial of access",
                'expected': ("8(b)(1)(A)", "Duty of Fair Representation, incl'g Superseniority, denial of access")
            },
            {
                'description': 'Invalid allegation (numeric second term)',
                'case': "8(8)(1)(A) Duty of Fair Representation, incl'g Superseniority, denial of access",
                'expected': None
            },
            {
                'description': 'Valid hypothetical third term greater than 9',
                'case': '8(b)(11)(A) Something I made up',
                'expected': ('8(b)(11)(A)', 'Something I made up')
            }
            ]
    for t in regex_tests:
        print('Testing:', t['description'])
        got = allegations.pat.match(t['case'])
        expected = t['expected']
        if expected is None and got is not None:
            print(f'Expected None, got {got.group(1)} and {group(2)}')
            return False
        if expected is not None and got is None:
            print(f'Expected {expected[0]}, {expected[1]}, got None')
            return False
        if expected is None and got is None:
            continue

        gots = got.group(1), got.group(2)
        if gots != expected:
            print(f'Expected\n{expected}\nGot\n{gots}')
            return False

    # Tests passed
    return True

def test_parse_allegations():
    tests = [
            {
                'description': 'Multiple valid allegations',
                'case': """8(a)(3) Discharge (Including Layoff and Refusal to Hire (not salting))
                8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
                8(a)(1) Coercive Statements (Threats, Promises of Benefits, etc.)
                """,
                'expected': [
                    ('8(a)(3)', 'Discharge (Including Layoff and Refusal to Hire (not salting))', None),
                    ('8(a)(1)', 'Concerted Activities (Retaliation, Discharge, Discipline)', None),
                    ('8(a)(1)', 'Coercive Statements (Threats, Promises of Benefits, etc.)', None)
                    ]
            },
            {
                'description': 'Test single line and trailing whitespace',
                'case': """8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
                """,
                'expected': [
                    ('8(a)(1)', 'Concerted Activities (Retaliation, Discharge, Discipline)', None)
                    ]
            },
            {
                'description': 'Empty lines are ignored',
                'case': """8(a)(1) Coercive Rules

                8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
                """,
                'expected': [
                    ('8(a)(1)', 'Coercive Rules', None),
                    ('8(a)(1)', 'Concerted Activities (Retaliation, Discharge, Discipline)', None)
                    ]
            },
            {
                'description': 'Mismatch fails gracefully',
                'case': """8(2)(1) Coercive Rules
                8(a)(1) Concerted Activities (Retaliation, Discharge, Discipline)
                """,
                'expected': [
                    (None, None, '8(2)(1) Coercive Rules'),
                    ('8(a)(1)', 'Concerted Activities (Retaliation, Discharge, Discipline)', None)
                    ]
            }
        ]

    for t in tests:
        print('Testing:', t['description'])
        got = allegations.parse_allegations(t['case'])
        expected = t['expected']
        if got != expected:
            print(f'Expected\n{expected}\nGot\n{got}')
            return False

    # Tests passed
    return True


if __name__ == '__main__':
    if not test_regex() or not test_parse_allegations():
        import sys
        sys.exit(1)
