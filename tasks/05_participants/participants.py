from common import db_config
import pandas as pd
from bs4 import BeautifulSoup as bs


def html_raw_participants(html_str: str) -> list:
    try:
        soup = bs(html_str, "lxml")
        participants_table = soup.find(
            "table",
            attrs={
                "class": "Participants views-table case-decisions-table views-view-table usa-table-borderless cols-3 responsive-enabled"
            },
        )
        participants = participants_table.find_all("tr")
        raw_participants = [
            participant for i, participant in enumerate(participants) if i % 2 == 1
        ]

    except Exception as e:
        print("Exception in html parse:")
        raw_participants = []
        raise e

    return raw_participants


def clean_html(html_str: str) -> str:
    for x in [
        "<td>",
        "\n",
        "<b>",
        "\n",
    ]:
        html_str = html_str.replace(x, "")
    return html_str.strip().rstrip()


def html_parse_participant(raw_participant_list: list) -> list:
    participants = []
    for raw_participant in raw_participant_list:
        participantDict = {}
        raw_participant = raw_participant.find(name="td")
        # print(f'raw_participant:{raw_participant}')
        brCount = str(raw_participant).count("<br/>")
        # print('brcount:', brCount)
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

        # print(participantDict)
        participants.append(participantDict)
    return participants


def pd_raw_participants(html_raw: str) -> list[dict]:
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
        # print('temp_dict', temp_dict)
        out_dict_list.append(temp_dict)
    # print('how many in out dict:', len(out_dict_list))
    return out_dict_list


def process_participants(cursor, case_row):
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
            # print('r HERE:', r)
            cursor.execute(
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
        print(f"Unable to parse participants from {case_id}, {case_number}")
        raise e
    finally:
        cursor.close()
