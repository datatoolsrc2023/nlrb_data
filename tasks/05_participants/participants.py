from collections import namedtuple
from common import paths
from os import listdir
import pandas as pd
import datetime
from bs4 import BeautifulSoup as bs


def read_in_pages_table(cursor) -> str:
     """
     reads in the pages table, returns a list of
     """

def html_raw_participants(html_str: str) -> list:
    try:
        soup = bs(html_str, 'lxml')
        participants_table = soup.find('table', attrs={'class': "Participants views-table case-decisions-table views-view-table usa-table-borderless cols-3 responsive-enabled"})
        participants = participants_table.find_all('tr')
        raw_participants = [participant for i, participant in enumerate(participants) if i%2==1]
        
    except Exception as e:
        print('Exception in html parse:')
        raw_participants = []
        raise e
        
    # print(raw_participants)
    return raw_participants

def clean_html(html_str: str) -> str:
    for x in ["<td>","\n","<b>","\n",]:
        html_str = html_str.replace(x, '')
    return html_str.strip().rstrip()

def html_parse_participant(raw_participant_list: list) -> list:
     participants = []
     for raw_participant in raw_participant_list:
        participantDict = {}
        raw_participant = raw_participant.find(name="td")
        print(f'raw_participant:{raw_participant}')
        brCount = str(raw_participant).count('<br/>')
        print('brcount:', brCount)
        participantDict['kind'] = clean_html(str(raw_participant).split('</b>')[0])
        

        if brCount <= 2:
            participantDict['name'] = ''
            participantDict['organization'] = ''
        else:
            participantDict['name'] = str(raw_participant).split('<br/>\n')[2].strip()
            participantDict['organization'] = str(raw_participant).split('</td>')[0].rstrip().split('\n')[-1].strip().replace(
                '<br/>',
                '')
        if brCount == 1:
            participantDict['role'] = ''  
        else:
            participantDict['role'] = clean_html(str(raw_participant).split('/>')[1][:-3])
             
        print(participantDict)
        participants.append(participantDict)
        return participants
    


# def find_docket_link(html_str:str) -> str:
  
def pd_raw_participants(html_file_location: str) -> list:
    try:
        tables = pd.read_html(html_file_location)
        for df in tables:
            if 'Participant' in df.columns:
                return df.dropna(how='all') 
        
    
    except Exception as e:
        print(f'Pandas table parse error: {e}')
    
    # If no participants table, return empty list for testing purposes
    return []
    
    

def read_tables(html_file_location: str) -> tuple:
    tables = pd.read_html(html_file_location)
    print(len(tables))
    docket_df = tables[0].dropna(how='all')
    participants_df = tables[1].dropna(how='all')
    with open(html_file_location, 'r', encoding='utf-8') as html_file:
        text = html_file.read()
        participants_df['parsed'] = parse_participants_str(text)
        
    return (docket_df, participants_df)


"""

current_pages = listdir(paths.pages)
testing_page_path, testing_case_number = current_pages[4], current_pages[4].split('.html')[0]

for page in current_pages[:5]:
    docket, participants = read_tables(html_file_location = str(paths.pages / page))

    docket['Date'] = pd.to_datetime(docket['Date'], format='%m/%d/%Y')
    docket['Date'] = [datetime.datetime.strftime(x, format='%Y-%m-%d') for x in docket['Date']]
    docket['case_number'] = testing_case_number
    print(docket.head())
    print(participants.parsed)
""" 


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

    