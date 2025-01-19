from flask import current_app as app

class Logger:
    def __init__(self):
        self.log = app.logger
