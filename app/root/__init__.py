import os
from flask import Blueprint

root_bp = Blueprint('root', os.getenv('APP_NAME', 'MEMBER-API'))

from app.root import routes
