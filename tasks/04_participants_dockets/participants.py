from collections import namedtuple
import re
from common import paths
from os import listdir
import pandas as pd
import datetime
import time


def parse_participants_str(html_str: str) -> list:
    initial_split = html_str.split('<h2>Participants</h2>')[1].split('</table>')[0].split('<tbody>')[1].split('<b> ')[1:]
    participants = []
    for raw_participant in initial_split:
        brCount = raw_participant.split('<td>')[0].count('br')

        participantDict = {'type': raw_participant.split('<')[0]}

        if brCount <= 2:
            participantDict['name'] = ''
            participantDict['organization'] = ''
        else:
            participantDict['name'] = raw_participant.split('<br/>\n')[1].strip()
            participantDict['organization'] = raw_participant.split('</td>')[0].rstrip().split('\n')[-1].strip().replace(
                '<br/>',
                '')
        participantDict['role'] = '' if brCount == 1 else raw_participant.split('/>')[1][:-3]
        participants.append(participantDict)
        
    return participants


# def find_docket_link(html_str:str) -> str:
  


def read_tables(html_file_location: str) -> str:
    with open(html_file_location, 'r', encoding='utf-8') as html_file:
            # pd.read_html grabs html tables!
            tables = pd.read_html(html_file_location)
            docket_df = tables[0].dropna(how='all')
            participants_df = tables[1].dropna(how='all')
    

    
    return (docket_df, participants_df)


     

current_pages = listdir(paths.pages)
testing_page_path, testing_case_number = current_pages[4], current_pages[4].split('.html')[0]

for page in current_pages[:5]:
    docket, participants = read_tables(html_file_location = str(paths.pages / testing_page_path))

    docket['Date'] = pd.to_datetime(docket['Date'], format='%m/%d/%Y')
    docket['Date'] = [datetime.datetime.strftime(x, format='%Y-%m-%d') for x in docket['Date']]
    docket['case_number'] = testing_case_number
    print(docket.head())
    


#print(participants.columns)
#print(participants.shape)
"""
participants_ = participants.Participant.tolist()
i=1
for participant in participants_:
     print(i, participant)
     i+=1


def task(html_page: str) -> tuple:
    d_df, p_df = read_tables(html_page)
"""
    
    