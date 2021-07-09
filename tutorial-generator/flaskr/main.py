import functools, sys

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('main', __name__, url_prefix='/main') # Declares blueprint

@bp.route('/get', methods=('GET', 'POST'))
def get():
    print('Hello World!', file=sys.stderr)
    if request.method == 'GET':
        print("GET Request", file=sys.stderr)
        error_message = "Jeff"
        # error_message = request.form['error'] # get from form (total message)
        print(error_message, file=sys.stderr)

        # parse error message to a recognizable format
        flash("JEFF")
        db = get_db()
        tutorial = db.execute(
            "SELECT * FROM tg WHERE error = '%s'" % error_message
        ).fetchone()

        error = None # default value of error        
        if tutorial is None:
            error = 'Error not recognized'

        if error is None:
            flash(tutorial, category='warning')
        else:
            flash(error, category='error')
        return redirect('base.html')
    else:
        return render_template('base.html')
            
