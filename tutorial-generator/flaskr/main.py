import functools, sys

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('main', __name__, url_prefix='/main') # Declares blueprint

@bp.route('/base', methods=('GET', 'POST'))
def get():
    print('Hello World!', file=sys.stderr)
    if request.method == 'GET':
        error_message = "Temporary Error Message"
        error_message = request.args['error'] # get from form (total message)
        print("GET REQUEST: {error}".format(error = error_message))

        # parse error message to a recognizable format
        db = get_db()
        selected_row = db.execute('SELECT * FROM tg WHERE error=?', (error_message,)).fetchone()

        tutorial = "Null Tutorial"
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
        
    return render_template('base.html')
            
