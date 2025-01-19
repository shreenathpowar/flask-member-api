from app.lib.db import AdminDB
from werkzeug.security import check_password_hash

class Admin(AdminDB):
    def __init__(self, dbfile, sql_file):
        super().__init__(dbfile, sql_file)

    def get_admins(self) -> list[int]:
        return []

    def get_info_by_id(self, id):
        self.log.debug(f'Get Admin data by id')
        info = self.get_admin_data(id=id)
        info.pop('password')
        return info

    def get_info_by_username(self, username):
        self.log.debug(f'Get Admin data by username')
        info = self.get_admin_data(username=username)
        info.pop('password')
        return info

    def validate_password(self, username, password):
        self.log.debug(f'Validate Admin')
        try:
            data = self.get_admin_data(username=username)
            dbpassword = data['password']
            valid = check_password_hash(dbpassword, password)
            return valid
        except Exception as error:
            self.log.error(f'Failed `Admin` `validate_password` function')
            self.log.error(f'Error: {error}, Username: {username}')
            return None
