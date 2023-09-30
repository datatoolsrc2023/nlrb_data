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
    This function takes an HTML string
    from the `raw_text` column in the `pages` database table,
    finds the participants HTML table from that string,
    collects the rows (i.e., a raw string for each participant) from the table,
    and finally returns a list of participant HTML strings.
    Each participant string will be parsed for relevant metadata
    in html_parse_participants() function.
    """
    try:
        soup = bs(html_str, "lxml")
        participants_table = soup.find(
            "table",
            attrs={
                "class": (
                    "Participants views-table case-decisions-table"
                    " views-view-table usa-table-borderless cols-3"
                    " responsive-enabled"
                )
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


def html_parse_single_participant(raw_participant: str) -> dict:
    """
    Given an input HTML string, attempt to parse the following 4 pieces of metadata:
    {
        "p_kind": ,
        "p_role": ,
        "p_name": ,
        "p_org": ,
    }
    """
    participantDict = {}
    raw_participant = raw_participant.find(name="td")
    brCount = str(raw_participant).count("<br/>")
    participantDict["p_kind"] = clean_html(str(raw_participant).split("</b>")[0])

    if brCount <= 2:
        participantDict["p_name"] = ""
        participantDict["p_org"] = ""
    # If there is only a name or only an organization associated with a participant,
    # it is impossible to reliably or consistently tell which it is.
    # This code distinguishes them if they're both present, but
    # it copies the same value for both dict keys if there's only one value present.
    # In other words, it responds to the ambiguity with redundancy.
    else:
        participantDict["p_name"] = str(raw_participant).split("<br/>\n")[2].strip()
        participantDict["p_org"] = clean_html(
            str(raw_participant).rsplit(sep="<br/>")[-2]
        )
    if brCount == 1:
        participantDict["p_role"] = ""
    else:
        participantDict["p_role"] = clean_html(str(raw_participant).split("/>")[1][:-3])

    return participantDict


def html_parser(html_str: str) -> list[dict]:
    """
    Runs the html_parse_metadata() function over list of raw participants
    from the `html_raw_participants()` function, called on a single case.
    Returns a list of dicts with relevant metadata.
    """
    raw_participant_list = html_raw_participants(html_str=html_str)

    return [
        html_parse_single_participant(raw_participant)
        for raw_participant in raw_participant_list
    ]


def pd_parser(html_raw: str) -> list[dict]:
    """
    Leverages pandas's read_html() to find the participant table,
    which provides three columns:
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


def parse_participants(html_raw=str) -> list[dict]:
    """ 
    Run the pd_parser() and html_parser() to get a list of dicts,
    one dict per participant in a given case.

    This list will be inserted into the participants table of the db
    with the process_participants() function.
    """

    # first, try to run both the pd and html parsing functions from above
    try:
        pd_participants_dict = pd_parser(html_raw=html_raw)
        html_participants_dict = html_parser(html_str=html_raw)

    except Exception as e:
        print(f"Failed to parse participant: {e}")
        raise e

    # then merge the results of the pd and html parsing,
    # output a list of dicts of the participant metadata
    out_dict_list = []
    for i in range(len(html_participants_dict)):
        temp_dict = pd_participants_dict[i] | html_participants_dict[i]
        out_dict_list.append(temp_dict)
    return out_dict_list


def process_participants(connection: sql.db_cnx(), case_row):
    """
    Connect to the nlrb database, insert participants.
    """
    curs = connection.cursor()

    if db_config.db_type == "sqlite":
        p_query = """INSERT INTO participants
                    (
                        case_id, 
                        case_number, 
                        p_name, 
                        p_kind, 
                        p_role, 
                        p_org, 
                        p_address, 
                        p_phone, 
                        raw_participant
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
    elif db_config.db_type == "postgresql":
        p_query = """INSERT INTO participants
                    (
                        case_id,
                        case_number,
                        p_name,
                        p_kind,
                        p_role,
                        p_org,
                        p_address,
                        p_phone,
                        raw_participant
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
    try:
        for r in parse_participants(html_raw=case_row["raw_text"]):
            curs.execute(
                p_query,
                (
                    case_row["case_id"],
                    case_row["case_number"],
                    r["p_name"],
                    r["p_kind"],
                    r["p_role"],
                    r["p_org"],
                    r["p_address"],
                    r["p_phone"],
                    r["raw_participant"],
                ),
            )

    # Since this task runs after the error_log table
    # has been set up and populated with allegations errors,
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
        print(
            f"Error parsing participants from case: \
            {case_row['case_id']}, {case_row['case_number']}."
        )
        curs.execute(error_query, (True, case_row["case_id"]))
        raise e

    finally:
        curs.close()
        connection.commit()
