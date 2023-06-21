#!/usr/bin/env python3

import participants
from common import paths
import os
import random
from common import db_config, sql

import unittest



class TestParseParticipants(unittest.TestCase):
    def test_matching_cardinality_raw_participants(self):
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            random_row_query = """select case_id, case_number, raw_text from pages order by random() limit 1;"""
            c.execute(random_row_query)
            test_case = c.fetchone()[2]   
        c.close()
        cnx.close()

        pd_raw_participants = participants.pd_raw_participants(test_case)
        html_raw_participants = participants.html_raw_participants(test_case)         
        print(f"lengths of pd:{len(pd_raw_participants)}, html:{len(html_raw_participants)}")
        self.assertEqual(len(pd_raw_participants), len(html_raw_participants))


class TestParticipantHtmlParse(unittest.TestCase):
    def test_html_participants_parse(self):
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            random_row_query = """select case_number, raw_text from pages order by random() limit 1;"""
            c.execute(random_row_query)
            test_case = c.fetchone()
        c.close()
        cnx.close()
        test_case = participants.html_raw_participants(test_case[1])
        #print(participants.html_raw_participants(test_case2))
        self.assertIsNotNone(participants.html_parse_participant(test_case))
    """
    def test_html_parse_3_br(self):
        test_case = participants.html_raw_participants(test_case[1])
        #print(participants.html_raw_participants(test_case2))
        self.assertIsNotNone(participants.html_parse_participant(test_case))
    """

class TestParticipantPdParse(unittest.TestCase):
    def test_pd_participants_columns(self):
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            random_row_query = """select case_number, case_id, raw_text from pages order by random() limit 1;"""
            c.execute(random_row_query)
            test_case = c.fetchone()
        c.close()
        cnx.close()
        result = participants.pd_raw_participants(test_case[2])
        print('pd_test_case:', test_case[0])
        #print(result)
        
        self.assertIsNotNone(result)

class TestParticipantParse(unittest.TestCase):
    def test_parser(self):
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            random_row_query = """select case_id, case_number, raw_text from pages order by random() limit 1;"""
            c.execute(random_row_query)
            test_case = c.fetchone()
        c.close()
        cnx.close()
        result = participants.parse_participant(test_case[2])
        print('parse_test_case:', test_case[0])
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
            

        c.close()
        cnx.close()
    """


if __name__ == '__main__':
    unittest.main()
