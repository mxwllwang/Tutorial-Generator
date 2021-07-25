import functools, sys, os
from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename
from flaskr.db import get_db
from compilers.compiler_error import CompilerError
from compilers import javacompiler

# from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'flaskr/uploads'

bp = Blueprint('main', __name__, url_prefix='/main') # Declares blueprint

@bp.route('/id', methods=('GET', 'POST'))
def id():
    if request.method == 'POST':
        error_message = "Temporary Error Message"
        error_message = request.form['error'] # get from form (total message)
        print("POST REQUEST /id: Error is {error}".format(error = error_message))

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

def allowed_file(filename, extension):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == extension

@bp.route('/file', methods=('GET', 'POST'))
def file():
    submitted = False
    errors = None # compilerError
    if request.method == 'POST':

        # parse file extension type
        allowed_extension = ''
        selected_language = request.form['lang']
        if selected_language == 'java':
            allowed_extension = 'java'
        elif selected_language == 'python':
            allowed_extension = 'py'
        elif selected_language == 'c++':
            allowed_extension = 'cpp'
        elif selected_language == 'text':
            allowed_extension = 'txt'
        else:
            flash("Language selection is unavailable")
        
        print("POST REQUEST /file: Allowed extension is {lang}".format(lang = allowed_extension))

        # upload file
        # check if the post request has the file part (is this necessary?)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if the user doesn't select a file, submit empty file without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename, allowed_extension):
            filename = secure_filename(file.filename)
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("Saved file successfully")
            if request.form.get('download'):            
                return redirect(url_for('download_file', name=filename)) # downloads the file
            elif request.form.get('generate'):
                submitted = True # Change submission status, enabling error and tutorial to be displayed
                print(file.filename)
                errors = javacompiler.java_compile(file.filename) # Inform Jinja of all the errors
            else:
                flash('An error occured')
        else:
            flash('Incorrect file extension')
            return redirect(request.url)

        #db = get_db()
        #selected_row = db.execute('SELECT * FROM tg WHERE error=?', (error_message,)).fetchone()

        #tutorial = "Default Tutorial"
        #error = None # default value of error        
        #if selected_row is None:
        #    error = 'Input not recognized'
        #else:
        #    tutorial = selected_row['tutorial']
        #    print(tutorial)
        
    return render_template('file.html', submitted=submitted, errors=errors)

@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        print ("add")
        
    return render_template('add.html')
            
