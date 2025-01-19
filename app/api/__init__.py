import os
from flask import Blueprint

api_version = {
    'api_version': 1,
    'name': 'Member API'
}

api_bp = Blueprint('api', os.getenv('APP_NAME', 'MEMBER-API'))

from app.api import routes
