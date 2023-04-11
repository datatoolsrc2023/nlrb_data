"""
Connection is just a wrapper around pymysql.Connection
to provide preferable cursor defaults throughout the project.
"""

import pymysql

class Connection(pymysql.Connection):
    # We get __enter__() for free, just want it to call __init__
    def __init__(self, config, *args, **kwargs):
        super().__init__(host=config.host,
                       user=config.user,
                       password=config.password,
                       database=config.database,
                       *args, **kwargs)

    def cursor(self, cursor=None, **kwargs):
        """Ensure ANSI_QUOTES"""
        c = super().cursor(cursor=cursor, **kwargs)
        c.execute('SET SQL_MODE=ANSI_QUOTES')
        return c

    def dict_cursor(self, **kwargs):
        """Provide easier access to DictCursor"""
        return self.cursor(cursor=pymysql.cursors.DictCursor, **kwargs)
