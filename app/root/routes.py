from app.root import root_bp
from flask import (
    redirect,
    url_for
)

@root_bp.route('/')
def root():
    return redirect(url_for('api.home'))
