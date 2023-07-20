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
    Reads in an html string from the `raw_text` column in the `pages` table,
    finds the participants table, collects the rows in the table,
    and finally returns a list of participant strings that will be parsed in the next step.
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
        raw_participants = []
        raise e

    return raw_participants


# this needs refacotring, cleaning up!
def html_parse_participant(raw_participant_list: list) -> list:
    """
    Given a list of raw participants from the `html_raw_participants()` function,
    this function attempts to parse the following 4 pieces of metadata and put them in a dict:
    ["p_kind", "p_role", "p_name", "p_org"].

    Returns a list of dicts.
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
        print(f"Pandas table parse error: {e}")

    # If no participants table, return empty list for testing purposes
    return []


def parse_participant(html_raw=str) -> list[dict]:
    try:
        pd_raw_dicts = pd_raw_participants(html_raw=html_raw)
        raw_html_parse = html_raw_participants(html_str=html_raw)
        # print('len(raw_html_parse):', len(raw_html_parse))
        html_participants = html_parse_participant(raw_html_parse)
        # print('len(html_participants)', len(html_participants))

    except Exception as e:
        print(f"Failed to parse participant: {e}")
        print(html_raw)
        pass

    out_dict_list = []
    for i in range(len(html_participants)):
        temp_dict = pd_raw_dicts[i] | html_participants[i]
        out_dict_list.append(temp_dict)
    return out_dict_list


def process_participants(connection: sql.db_cnx(), case_row):
    curs = connection.cursor()
    raw = case_row["raw_text"]
    case_id = case_row["case_id"]
    case_number = case_row["case_number"]

    if db_config.db_type == "sqlite":
        query = """INSERT INTO participants
                    (case_id, p_name, p_kind, p_role, p_org, p_address, p_phone, raw_participant)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
    elif db_config.db_type == "postgresql":
        query = """INSERT INTO participants
                    (case_id, p_name, p_kind, p_role, p_org, p_address, p_phone, raw_participant)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
    try:
        for r in parse_participant(raw):
            curs.execute(
                query,
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

    except Exception as e:
        if db_config.db_type == "sqlite":
            error_query = """INSERT INTO error_log (case_id, participants_parse_error)
                    VALUES (?, ?)
                """
        elif db_config.db_type == "postgresql":
            error_query = """INSERT INTO error_log (case_id, participants_parse_error)
                    VALUES (%s, %s);
                """
        print(f"Error parsing participants from case: {case_id}, {case_number}.")
        curs.execute(error_query, (case_id, True))
        raise e

    finally:
        curs.close()
        connection.commit()


def add_participant_row(case_id: int, r: list):
    # insert relevant info to participants table in the db
    try:
        if db_config.db_type == "sqlite":
            query = """INSERT INTO participants
                        (case_id, p_name, p_kind, p_role, p_org, p_address, p_phone, raw_participant)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """
        elif db_config.db_type == "postgresql":
            query = """INSERT INTO participants
                        (case_id, p_name, p_kind, p_role, p_org, p_address, p_phone, raw_participant)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """

        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(
                query,
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

    except Exception as e:
        print(f"Error adding page to {db_config.participants} table: {e}")
        raise e

    finally:
        c.close()
        cnx.close()


def threaded_process_participants(case_row):
    raw = case_row["raw_text"]
    case_id = case_row["case_id"]
    case_number = case_row["case_number"]

    try:
        for r in parse_participant(raw):
            add_participant_row(case_id=case_id, r=r)

    except Exception as e:
        print(f"Unable to parse participants from case_id: {case_id}, case_number: {case_number}")
        raise e
