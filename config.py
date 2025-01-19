import os
from logging import DEBUG as LDEBUG, INFO as LINFO
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    TESTING = False
    DEBUG = True if os.getenv('ENVIRONMENT', 'PROD') == 'DEV' else False
    LOGGING_LEVEL = LDEBUG if DEBUG else LINFO
    MEMBER_API_URL = os.getenv('MEMBER_API_URL_DEV') if os.getenv('ENVIRONMENT', 'PROD') == 'DEV' \
        else os.getenv('MEMBER_API_URL_PROD')
    SERVER_NAME = MEMBER_API_URL
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLITE_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        os.path.join(basedir, 'db', 'memberapi.db')
    ADMINS_SQL_FILE = os.environ.get('ADMIN_SQL_FILE') or \
        os.path.join(basedir, 'db', 'schemas', 'admins.sql')
    MEMBERS_SQL_FILE = os.environ.get('ADMIN_SQL_FILE') or \
        os.path.join(basedir, 'db', 'schemas', 'members.sql')
    MEMBERSHIPS_SQL_FILE = os.environ.get('ADMIN_SQL_FILE') or \
        os.path.join(basedir, 'db', 'schemas', 'admins.sql')
