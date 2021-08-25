import functools, sys, os
from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename
from app.db import get_db
from compilers.compiler_error import CompilerError
from compilers import javacompiler
import uuid

app = Flask(__name__)
bp = Blueprint('main', __name__, url_prefix='/main') # Declares blueprint

app.config['UPLOAD_FOLDER'] = '../working-folders'

def establish_user():
    if 'user' not in session:   
        user = str(uuid.uuid4()) # Save temporary session anonymous user identifier w/o flask-login
        session['user'] = user
        print("Created User", session['user'])
    else:
        print("User already exists", session['user'])
    # app.config['UPLOAD_FOLDER'] = os.path.join('app/uploads', session['user'])

## By ID
@bp.route('/id', methods=('GET', 'POST'))
def id():
    
    db = get_db() # Get dropdown list for error selection
    database_errors = db.execute('SELECT id, error FROM java_errors').fetchall() # TODO
    
    if request.method == 'POST':
        establish_user()
        error_message = "Temporary Error Message"
        error_message = request.form['error'] # get from form (total message)
        print("POST REQUEST /id: Error is {error}".format(error = error_message))

        # parse error message to a recognizable format
        db = get_db()
        selected_row = db.execute('SELECT * FROM java_errors WHERE id=?', (error_message,)).fetchone()

        tutorial = "Default Tutorial"
        error = None # default value of error        
        if selected_row is None:
            error = 'Input not recognized'
        else:
            tutorial = selected_row['tutorial']
            error_msg = selected_row['error']
            print("Tutorial:", tutorial)
            print("Error:", error_msg)

        if error is None:
            flash("Error: " + error_msg)
            flash("Tutorial: " + tutorial)
        else:
            flash(error, category='error')
        
    return render_template('id.html', errors=database_errors)

def allowed_file(filename, extension):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == extension

## By File
@bp.route('/file', methods=('GET', 'POST'))
def file():
    submitted = False
    errors = None # compilerError
    tutorials = None
    filename = ""
    if request.method == 'POST':
        establish_user()
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
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], session['user']) # Location that file will be saved at

            try:
                os.mkdir(upload_path) # Create working folder if does not exist
            except OSError as error:
                print(upload_path, "already exists")
            
            print('Upload Folder:', os.path.abspath(upload_path))
            file.save(os.path.join(upload_path, filename))
            print("Saved file successfully")
            
            ## DOWNLOAD FILE
            if request.form.get('download'):            
                return redirect(url_for('download_file', location=session['user'], name=filename)) # downloads the file
            ## GENERATE TUTORIAL
            elif request.form.get('generate'):
                tutorials = {} # Initialize empty dictionary
                submitted = True # Change submission status, enabling error and tutorial to be displayed
                errors = javacompiler.java_compile(filename, upload_path) # Inform Jinja of all the errors

                # parse error message to a recognizable format
                db = get_db()
                for error in errors:
                    tutorial = "No tutorial found"
                    selected_row = db.execute('SELECT * FROM java_errors WHERE id=?', (error.get_id(),)).fetchone()
                    if selected_row is not None:
                        tutorial = selected_row['tutorial']
                        print("Tutorial -", tutorial)
                        print("Error -", error.get_error())
                    tutorials[error] = tutorial
            else:
                flash('An error occured')
        else:
            flash('Incorrect file extension')
            return redirect(request.url)

        # db stuff
        
    return render_template('file.html', filename=filename, submitted=submitted, errors=errors, tutorials=tutorials)

## Add Tutorials
@bp.route('/add', methods=('GET', 'POST'))
def add():

    db = get_db() # Get dropdown list for error selection
    database_errors = db.execute('SELECT id, error FROM java_errors').fetchall() # TODO
    
    selected_language = ''
    error_id = int(-1) # java
    error_msg = ''
    if request.method == 'POST':
        establish_user()
        selected_language = request.form['lang']
        
        if request.form.get('select'): # Select Language
            if selected_language == 'java':
                print("Selected Java")
            else:
                flash("Language unsupported")
                
        elif request.form.get('next'): # After language has been selected
            if selected_language == 'java': # Case java
                error_id = int(request.form['errorID'])
                print(error_id)
                ##
                db = get_db()
                selected_row = db.execute('SELECT * FROM java_errors WHERE id=?', (error_id,)).fetchone()

                tutorial = "Default Tutorial"
                error = None # default value of error        
                if selected_row is None:
                    error = 'Input not recognized'
                else:
                    tutorial = selected_row['tutorial']
                    error_msg = selected_row['error']
                    print("Tutorial:", tutorial)
                    print("Error:", error_msg)

                if error is not None:
                    flash(error, category='error')
                
                
            # elif other cases here
            else: # This should not happen
                flash("Language Unsupported")

        elif request.form.get('add'):
            tutorial_msg = request.form['tutorial']
            if tutorial_msg is not None:            
                error_id = int(request.form['errorID'])
                db = get_db()
                db.execute('UPDATE java_errors SET tutorial =? WHERE id=?', (tutorial_msg, error_id,))
                print("Update:", tutorial_msg, "", error_id)
                db.commit()
                flash("Tutorial Saved")
        else:
            flash("An error occurred")
        
    return render_template('add.html', language=selected_language, error=error_id, message=error_msg, errors=database_errors)
            
