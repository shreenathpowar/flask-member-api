import sqlite3
import datetime
from flask import current_app as app
from app.lib.logger import Logger


def convert_to_dict(sqlrows: sqlite3.Row | list) -> dict | list:
    """
    convert sql output (sqlite3.Row(s)) into python dictionary

    Below line must be added to db connection object to use this function

    .. code-block:: python
        connection.row_factory = sqlite3.Row

    SQL rows can directly be converted into dict using dict_factory
    See :ref: `dict_factory`.

    :param sqlrows: output of cursor fetchall/fetchone/fetchmany
    """

    if sqlrows is None:
        return None

    if isinstance(sqlrows, sqlite3.Row):
        return {key: sqlrows[key] for key in sqlrows.keys()}

    results = []
    for row in sqlrows:
        results.append({key: row[key] for key in row.keys()})
    return results


def dict_factory(cursor, row) -> dict:
    """
    accepts the cursor and the original row as a tuple and will return the real result row

    See :ref: `https://docs.python.org/3.5/library/sqlite3.html#sqlite3.Connection.row_factory`.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    if not d:
        d = None
    return d


class connection(Logger):
    """
    Establish a connection with sqlite3 DB.

    Use `with` statement
    e.g.
    .. code-block:: python

        with connection(dbfile) as con:
            # your code

    :param dbfile: database file
    """

    def __init__(self, dbfile):
        super().__init__()
        self.connection = None
        self.dbfile = dbfile

    def __enter__(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.dbfile)
            self.connection.row_factory = dict_factory
        self.log.debug(f'Connected to Database')
        return self.connection

    def __exit__(self, etype, evalue, etraceback):
        if self.connection:
            self.log.debug(f'Connection to Database closed')
            self.connection.close()


class SQLDB(Logger):
    def __init__(self, dbfile):
        super().__init__()
        self.dbfile = dbfile
        self.connection = connection

    def table_exists(self, table):
        self.log.debug(f'Checking table exists')
        result = None
        with self.connection(self.dbfile) as con:
            cursor = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table, ))
            result = cursor.fetchone()

        return result is not None

    def create_table(self, schema_file):
        self.log.debug(f'Creating table from schema: {schema_file}')
        try:
            with open(schema_file, 'r') as sql_file:
                sql_script = sql_file.read()

            with self.connection(self.dbfile) as con:
                con.executescript(sql_script)
                con.commit()

            return True
        except Exception as e:
            self.log.error(f'Failed `SQLDB` `create_table` function, schema: {schema_file}')
            self.log.error(f'Error: {e}')
            return False


class AdminDB(SQLDB):
    def __init__(self, dbfile, sql_file):
        super().__init__(dbfile)
        self.table = 'admins'
        self.sql_file = sql_file

        if not self.table_exists(self.table):
            self.create_table(self.sql_file)

    def add(self, username, emailid, hpassword, active=1):
        self.log.debug(f'Adding admin into {self.table}')
        try:
            id = None
            timestamp = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            with self.connection(self.dbfile) as con:
                con.execute(f'INSERT INTO {self.table} (username, emailid, password, active, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)', 
                            (username, emailid, hpassword, active, timestamp, timestamp, ))
                con.commit()
                cursor = con.execute(f'SELECT id from {self.table} where username = ?', (username, ))
                id = int(cursor.fetchone()['id'])
            if id is None:
                raise Exception(f'Failed getting added admin id')
            return id
        except Exception as error:
            self.log.error('Failed `AdminDB` `add` function with below error -v')
            self.log.error(f'Error: {error}')
            return None

    def exists(self, id=None, username=None, emailid=None):
        self.log.debug(f'Checking if admin exists')
        result = None
        with self.connection(self.dbfile) as con:
            if id is None and username is None and emailid is None:
                self.log.error(f'Either id, username or email id is required to check admin existence')
                return False
            if id:
                cursor = con.execute(f'select id from {self.table} where id=?', (id, ))
            elif username:
                cursor = con.execute(f'select id from {self.table} where username=?', (username, ))
            elif emailid:
                cursor = con.execute(f'select id from {self.table} where emailid=?', (emailid, ))
            result = cursor.fetchone()
        return result is not None

    def remove(self, id):
        self.log.debug(f'Removing admin')
        try:
            with self.connection(self.dbfile) as con:
                con.execute(f'DELETE FROM {self.table} WHERE id = ?', (id, ))
                con.commit()
            return True
        except Exception as error:
            self.log.error(f'Failed `AdminDB` `remove` function')
            self.log.error(f'Error: {error} ID: `{id}`')
            return False

    def update(self, id, username=None, emailid=None, hpassword=None):
        self.log.debug(f'Updaing Admin')
        try:
            if username is None and emailid is None and hpassword is None:
                self.log.error(f'Either username, email or password is required to check admin existence')
                return False

            with self.connection(self.dbfile) as con:
                if username and emailid is None and hpassword is None:
                    con.execute(f'UPDATE {self.table} SET (username=?) WHERE id IS ?', (username, id, ))
                elif emailid and username is None and hpassword is None:
                    con.execute(f'UPDATE {self.table} SET (emailid=?) WHERE id IS ?', (emailid, id, ))
                elif hpassword and username is None and emailid is None:
                    con.execute(f'UPDATE {self.table} SET (password=?) WHERE id IS ?', (hpassword, id, ))
                elif username and emailid and hpassword is None:
                    con.execute(f'UPDATE {self.table} SET (username=?, emailid=?) WHERE id IS ?', (username, emailid, id, ))
                elif emailid and hpassword and username is None:
                    con.execute(f'UPDATE {self.table} SET (emailid=?, password=?) WHERE id IS ?', (emailid, hpassword, id, ))
                elif username and hpassword and emailid is None:
                    con.execute(f'UPDATE {self.table} SET (username=?, password=?) WHERE id IS ?', (username, hpassword, id, ))
                elif username and emailid and hpassword:
                    con.execute(f'UPDATE {self.table} SET (username=?, emailid=?, password=?) WHERE id IS ?', (username, emailid, hpassword, id, ))
                else:
                    self.log.debug(f'Something went wrong! `{username}` `{emailid}` `{hpassword}`')
                    return False
                con.commit()
            return True
        except Exception as error:
            self.log.error(f'Failed `AdminDB` `update` function')
            self.log.error(f'Error: {error}')
            return False

    def get_admin_data(self, id=None, username=None):
        self.log.debug(f'Getting admin data')
        try:
            result = None
            if id is None and username is None:
                raise Exception(f'Either id, username is required to check admin existence')

            with self.connection(self.dbfile) as con:
                if id:
                    cursor = con.execute(f'SELECT * from {self.table} where id = ?', (id, ))
                elif username:
                    cursor = con.execute(f'SELECT * from {self.table} where username = ?', (username, ))
                result = cursor.fetchone()
            return result
        except Exception as error:
            self.log.error(f'Failed `AdminDB` `get_info` function')
            self.log.error(f'Error: {error}, ID: {id}')
            return None
