#!/usr/bin/env python3

from common import db_config, sql


if __name__ == '__main__':
    """Ensure pages table is created."""

    statements = sql.get_query_lines_from_file(f'{db_config.db_type}/pages.sql')
    pages_query = 'SELECT COUNT(*) c from pages;'
    
    try:
        with sql.db_cnx() as cnx:
            c = cnx.cursor()
            c.execute(pages_query)
            table_count = c.fetchall()[0]
        print(f'{db_config.pages} table already created and populated with {table_count[0]} cases')
        c.close()
        cnx.close()

    except Exception as e:
        print(f'Could not count pages: {e}')
        try:
            with sql.db_cnx() as cnx:
                c = cnx.cursor()
                print(f'Attempting to create {db_config.pages} table...')
                for statement in statements:
                    c.execute(statement)
        except Exception as e:
            raise Exception(f'Failed to create table {db_config.pages}') from e
        else: # no exception
            print(f'Created {db_config.pages} table')
        finally:
            c.close()
            cnx.close()
                
