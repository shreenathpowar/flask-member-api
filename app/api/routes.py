from app.api import api_bp, api_version
from functools import wraps
from flask import (
    request,
    jsonify,
    current_app as app
)
from werkzeug.security import generate_password_hash
from app.lib.admin import Admin

################## decorators #################
def protect(f):
    '''
    decorator to protect admin routes
    '''
    @wraps(f)
    def decorator(*args, **kwargs):
        username = request.authorization.get('username')
        password = request.authorization.get('password')
        dbfile = app.config['SQLITE_DATABASE_URI']
        admin = Admin(dbfile, app.config['ADMINS_SQL_FILE'])
        if admin.validate_password(username, password):
            dbaccess = ({ 'admin': admin })
            kwargs.update({'dbaccess': dbaccess})
            return f(*args, **kwargs)
        return jsonify({ 'message': 'Unuthorized' }), 403
    return decorator

def get_db_access(db=[]):
    '''
    decorator to get db access in route functions
    '''
    def db_access(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            dbaccess = kwargs.get('dbaccess', {})
            dbfile = app.config['SQLITE_DATABASE_URI']
            for _db in db:
                # protected decorator already created admin given protect decorator is second in chain
                # always keep protect second in chain for: only get db access or proceed if admin is athonticated
                if _db == 'admin' and not dbaccess.get(_db, None):
                    dbaccess.update({ _db: Admin(dbfile, app.config['ADMINS_SQL_FILE']) })
            kwargs.update({'dbaccess': dbaccess})
            return f(*args, **kwargs)
        return decorator
    return db_access
############# end decorators ##############


################## routes #################
@api_bp.route('/')
def home():
    return jsonify(api_version), 200


@api_bp.route('/admin', methods=['POST'])
@protect
@get_db_access(db=['admin'])
def create_admin(dbaccess=None):
    app.logger.debug(f'create admin request')
    if not dbaccess and dbaccess.get('admin', None):
        app.logger.error(f'Internal Server Error')
        response = api_version.copy()
        response.update({'message': 'Internal Server Error'})
        return jsonify(response), 500

    r = request.get_json()
    username = r.get('username', None)
    emailid = r.get('emailid', None)
    password = r.get('password', None)

    if username is None or emailid is None or password is None:
        response = api_version.copy()
        response.update({'message': 'Bad Request'})
        return jsonify(response), 403

    if dbaccess['admin'].exists(username=username) or dbaccess['admin'].exists(emailid=emailid):
        response = api_version.copy()
        response.update({'message': 'Admin Already Exists with Same Username or Email ID'})
        return jsonify(response), 406

    hpassword = generate_password_hash(password)
    id = dbaccess['admin'].add(username, emailid, hpassword)

    if id is None:
        app.logger.error(f'Internal Server Error')
        response = api_version.copy()
        response.update({'message': 'Internal Server Error'})
        return jsonify(response), 500

    result = dbaccess['admin'].get_info_by_id(id)
    response = api_version.copy()
    result.pop('id')
    response.update({str(id): result})
    return jsonify(response), 200

@api_bp.route('/admin/<int:id>', methods=['GET'])
@protect
@get_db_access(db=['admin'])
def get_admin(id, dbaccess=None):
    app.logger.debug(f'get admin request, ID:{id}')
    if not dbaccess and dbaccess.get('admin', None):
        app.logger.error(f'Internal Server Error')
        response = api_version.copy()
        response.update({'message': 'Internal Server Error'})
        return jsonify(response), 500

    try: id = int(id)
    except ValueError:
        response = api_version.copy()
        response.update({'message': 'Bad Request'})
        return jsonify(response), 403

    result = dbaccess['admin'].get_info_by_id(id)
    response = api_version.copy()
    result.pop('id')
    response.update({str(id): result})
    return jsonify(response), 200
