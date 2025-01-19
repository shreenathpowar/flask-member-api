import os
import logging
import datetime
from logging import FileHandler, StreamHandler
from flask.logging import default_handler
from flask import Flask
from config import Config

def create_app(flask_config=Config):
    app = Flask(os.getenv('APP_NAME', 'MEMBER-API'))
    app.config.from_object(flask_config)

    from flask_cors import CORS
    CORS(app=app, resources=['/api/*'], origins='*')

    app.logger.removeHandler(default_handler)

    stream_handler = StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    stream_handler.setLevel(app.config['LOGGING_LEVEL'])
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(app.config['LOGGING_LEVEL'])

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        timestamp = datetime.datetime.now().strftime(f'%Y%m%d-%H%M%S')
        file_handler = FileHandler(f'logs/{timestamp}-{os.getenv("APP_NAME", "MEMBER-API")}.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s in %(module)s:%(lineno)d, [%(threadName)s]: %(message)s'))
        file_handler.setLevel(app.config['LOGGING_LEVEL'])
        app.logger.addHandler(file_handler)
        app.logger.setLevel(app.config['LOGGING_LEVEL'])

    app.logger.info('Member API startup')

    # register blueprints
    from app.root import root_bp
    app.register_blueprint(root_bp)

    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
