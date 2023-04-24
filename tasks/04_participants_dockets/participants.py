from collections import namedtuple
import re
from common import paths
from os import listdir
import pandas as pd


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
def read_tables(html_file_location: str) -> str:
    with open(html_file_location, 'r', encoding='utf-8') as html_file:
            # pd.read_html grabs html tables!
            tables = pd.read_html(html_file_location)
            docket_df = tables[0].dropna(how='all')
            participants_df = tables[1].dropna(how='all')
    

    
    return (docket_df, participants_df)


current_pages = listdir(paths.pages)
print(current_pages[4])
docket, participants = read_tables(html_file_location = str(paths.pages / current_pages[4]))

print(docket.columns)



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
    
    