#!/usr/bin/env/python3

from common import sql


def main():

    query = 'INSERT INTO error_log (case_id) SELECT id from cases'

    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(query)
            cnx.commit()
    except Exception as e:
        raise Exception('Unable to insert case ids into error_log table') from e
    else: # no exception
        print('Inserted case IDs from cases table into error_log table')
    finally:
        c.close()
        cnx.close()



if __name__ == '__main__':
    main()