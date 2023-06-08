from . import paths

# general db connection variables
# can be set to postgresql or sqlite3
db_type = 'sqlite'

# postgresql connection variables
host = 'localhost'
user = 'nlrb'
password = 'badpassword'
database = 'nlrb_data'
port = '5432'

# sqlite3 connection variables
sqlite_file = paths.data / 'sqlite_db' / 'nlrb_data.db'

# commonly used database tables
allegations = 'allegations'
cases_raw = 'cases_raw'
cases = 'cases'
error_log = 'error_log'
