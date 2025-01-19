from app.lib.db import MembershipDB
from werkzeug.security import check_password_hash

class Membership(MembershipDB):
    def __init__(self, dbfile, sql_file):
        super().__init__(dbfile, sql_file)
