import functools, sys

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('main', __name__, url_prefix='/main') # Declares blueprint

@bp.route('/id', methods=('GET', 'POST'))
def id():
    if request.method == 'POST':
        error_message = "Temporary Error Message"
        error_message = request.form['error'] # get from form (total message)
        print("POST REQUEST: {error}".format(error = error_message))

        # parse error message to a recognizable format
        db = get_db()
        selected_row = db.execute('SELECT * FROM tg WHERE error=?', (error_message,)).fetchone()

        tutorial = "Default Tutorial"
        error = None # default value of error        
        if selected_row is None:
            error = 'Input not recognized'
        else:
            tutorial = selected_row['tutorial']
            print(tutorial)

        if error is None:
            flash(tutorial, category='warning')
        else:
            flash(error, category='error')
        
    return render_template('id.html')

@bp.route('/file', methods=('GET', 'POST'))
def file():
    if request.method == 'POST':
        error_message = "Temporary Error Message"
        error_message = request.form['error'] # get from form (total message)
        print("POST REQUEST: {error}".format(error = error_message))

        # parse error message to a recognizable format
        db = get_db()
        selected_row = db.execute('SELECT * FROM tg WHERE error=?', (error_message,)).fetchone()

        tutorial = "Default Tutorial"
        error = None # default value of error        
        if selected_row is None:
            error = 'Input not recognized'
        else:
            tutorial = selected_row['tutorial']
            print(tutorial)

        if error is None:
            flash(tutorial, category='warning')
        else:
            flash(error, category='error')
        
    return render_template('file.html')
            
