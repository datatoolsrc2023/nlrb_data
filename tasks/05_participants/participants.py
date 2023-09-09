from common import db_config
import pandas as pd
from bs4 import BeautifulSoup as bs
from common import sql


def clean_html(html_str: str) -> str:
    """
    A simple helper function for cleaning html artifacts from html strings.
    There might be a more idiomatic way for doing this.
    """
    for x in [
        "<td>",
        "\n",
        "<b>",
        "\n",
    ]:
        html_str = html_str.replace(x, "")

    return html_str.strip().rstrip()


def html_raw_participants(html_str: str) -> list:
    """
    This function takes an HTML string from the `raw_text` column in the `pages` database table,
    finds the participants HTML table in the string, 
    collects the rows (i.e., a raw string for each participant) from the table,
    and finally returns a list of participant HTML strings.
    Each participant string will be parsed for relevant metadata in html_parse_participants() function.
    """
    try:
        soup = bs(html_str, "lxml")
        participants_table = soup.find(
            "table",
            attrs={
                "class": "Participants views-table case-decisions-table views-view-table usa-table-borderless cols-3 responsive-enabled"
            },
        )
        participants = participants_table.find_all("tr")
        
        # participants are separated by blank lines, so use %2 to find every other line
        raw_participants = [
            participant for i, participant in enumerate(participants) if i % 2 == 1
        ]

    except Exception as e:
        print("Exception in html parse:")
        raise e

    return raw_participants



def html_parse_participant(raw_participant_list: list) -> list[dict]:
    # this could use refactoring
    """
    Given a list of raw participants from the `html_raw_participants()` function,
    this function attempts to parse the following 4 pieces of metadata and put them in a dict:
    ["p_kind", "p_role", "p_name", "p_org"].

    Returns a list of dicts with the format:
    {
        "p_kind": , 
        "p_role": , 
        "p_name": , 
        "p_org": ,
    }.
    """
    participants = []
    for raw_participant in raw_participant_list:
        participantDict = {}
        raw_participant = raw_participant.find(name="td")
        brCount = str(raw_participant).count("<br/>")
        participantDict["p_kind"] = clean_html(str(raw_participant).split("</b>")[0])

        if brCount <= 2:
            participantDict["p_name"] = ""
            participantDict["p_org"] = ""
        else:
            participantDict["p_name"] = str(raw_participant).split("<br/>\n")[2].strip()
            participantDict["p_org"] = clean_html(
                str(raw_participant).rsplit(sep="<br/>")[-2]
            )
        if brCount == 1:
            participantDict["p_role"] = ""
        else:
            participantDict["p_role"] = clean_html(
                str(raw_participant).split("/>")[1][:-3]
            )
        participants.append(participantDict)
    return participants


def pd_raw_participants(html_raw: str) -> list[dict]:
    """
    Leverages pandas's read_html() to find the participant table, which provides three columns:
    ["raw_participant", "p_address", "p_phone"].
    """
    try:
        tables = pd.read_html(html_raw)
        for df in tables:
            if "Participant" in df.columns:
                df = df.dropna(how="all")
                df.columns = ["raw_participant", "p_address", "p_phone"]

                return df.to_dict(orient="records")

    except Exception as e:
        print("Pandas table parse error:")
        raise e


def parse_participant(html_raw=str) -> list[dict]:
    """
    runs the parsing functions in order
    """

    # first, try to run both the pd and html parsing functions from above
    try:
        pd_raw_dicts = pd_raw_participants(html_raw=html_raw)
        raw_html_parse = html_raw_participants(html_str=html_raw)
        html_participants = html_parse_participant(raw_participant_list=raw_html_parse)

    except Exception as e:
        print(f"Failed to parse participant: {e}")
        raise e
    
    # then merge the results of the pd and html parsing, 
    # output a list of dicts of the participant metadata
    out_dict_list = []
    for i in range(len(html_participants)):
        temp_dict = pd_raw_dicts[i] | html_participants[i]
        out_dict_list.append(temp_dict)
    return out_dict_list


def process_participants(connection: sql.db_cnx(), case_row):
    """
    Connect to the nlrb database, insert a row 
    """
    curs = connection.cursor()
    
    case_id = case_row["case_id"]
    case_number = case_row["case_number"]

    if db_config.db_type == "sqlite":
        p_query = """INSERT INTO participants
                    (case_id, p_name, p_kind, p_role, p_org, p_address, p_phone, raw_participant)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
    elif db_config.db_type == "postgresql":
        p_query = """INSERT INTO participants
                    (case_id, p_name, p_kind, p_role, p_org, p_address, p_phone, raw_participant)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
    try:
        for r in parse_participant(html_raw=case_row["raw_text"]):
            curs.execute(
                p_query,
                (
                    case_id,
                    r["p_name"],
                    r["p_kind"],
                    r["p_role"],
                    r["p_org"],
                    r["p_address"],
                    r["p_phone"],
                    r["raw_participant"],
                ),
            )

    # since this task runs after the error_log table has been set up and populated with allegations errors,
    # the query here updates extant rows based on case_ids rather than insert new rows.
    except Exception as e:
        if db_config.db_type == "sqlite":
             error_query = """
            UPDATE error_log 
            SET participants_parse_error = ?
            WHERE case_id = ?;
                """
        elif db_config.db_type == "postgresql":
            error_query = """
            UPDATE error_log 
            SET participants_parse_error = %s
            WHERE case_id = %s;
                """
        print(f"Error parsing participants from case: {case_id}, {case_number}.")
        curs.execute(error_query, (True, case_id))
        raise e

    finally:
        curs.close()
        connection.commit()
