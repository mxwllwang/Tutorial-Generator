import os

from flask import Flask

# Factory function for creating an app (it returns app)
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True) # current Python module name, and config files relative to instance folder
    app.config.from_mapping(
        SECRET_KEY='dev', # override with random value when deploying
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite') # path of SQLite database file
    )

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
    def hello():
        return 'Tutorial Generator'

    # import database?
    from . import db
    db.init_app(app)

    # import my main.py file (explicit relative path)
    # from . import main
    from . import main
    app.register_blueprint(main.bp)

    return app
