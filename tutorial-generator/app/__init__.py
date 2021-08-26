import os
from flask import Flask, redirect, render_template, send_from_directory, flash

# Factory function for creating an app (it returns app)
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True) # current Python module name, and config files relative to instance folder
    app.config.from_mapping(
        SECRET_KEY='dev', # override with random value when deploying
        # SECRET_KEY='I\x8e\xe8H\x12\xf6\xe6Y\xcdc\xde\xaf{\x15\x08>',
        # SECRET_KEY='QdJIebhULdyw5PSZGjGoaA',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'), # path of SQLite database file
        UPLOAD_FOLDER='../working-folders' # TODO: Db may not work yet. Will have to rerun flask init-db later
    )

    ##ckeditor.init_app(app)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        # test_config is default none unless a parameter is passed in
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # now default page should say hello
    @app.route('/')
    def index():
        return redirect('/main')

    @app.route('/main')
    def home():
        return redirect('/main/file')

    # import database?
    from . import db
    db.init_app(app)

    # import my main.py file (explicit relative path)
    # from . import main
    from . import main
    app.register_blueprint(main.bp)

    @app.route('/uploads/<location>/<name>')
    def download_file(location, name):
        try:
            print(os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], location, name)))
            return send_from_directory(
                os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], location)), name, as_attachment=True
            )
        except:
            print("Failed send_from_directory, redirecting")
            flash("Download failed")
            return redirect('/main/file')            
        return render_template('file.html')

    app.add_url_rule(
        "/uploads/<location>/<name>", endpoint="download_file", build_only=True
    )

    return app
