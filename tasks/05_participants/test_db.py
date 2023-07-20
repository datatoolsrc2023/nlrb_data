#!/usr/bin/env python3

from common import db_config, sql


if __name__ == "__main__":
    """Confirm database meets expectations."""

    pages_query = "SELECT COUNT(*) c from pages"
    participants_query = "SELECT COUNT(*) c from participants"
    
    print("Attempting to count pages and check that participants table is empty...")
    try:
        with sql.db_cnx() as cnx:
            c_pages = cnx.cursor()
            c_participants = cnx.cursor()
            c_pages.execute(pages_query)
            c_participants.execute(participants_query)
    except Exception as e:
        print("Failed to count from tables")
        raise e
    else:
        pages_count = c_pages.fetchone()[0]
        if pages_count == 0:
            raise Exception(
                f"Expected {db_config.pages} table to be populated, found 0 records"
            )
        participants_count = c_participants.fetchone()[0]
        if participants_count != 0:
            raise Exception(f"Expected 0 participants, found {participants_count}.")
        print(
            f"{db_config.pages} and {db_config.participants} "
            "table count expectations met"
        )
    finally:
        c_pages.close()
        c_participants.close()
        cnx.close()
