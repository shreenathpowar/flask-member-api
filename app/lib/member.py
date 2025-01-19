from app.lib.db import MemberDB
from werkzeug.security import check_password_hash

class Member(MemberDB):
    def __init__(self, dbfile, sql_file):
        super().__init__(dbfile, sql_file)
