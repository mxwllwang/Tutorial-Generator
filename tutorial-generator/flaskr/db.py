import sqlite3

import click
from flask import current_app, g # special object g stores request data
    # current_app refers to the Flask app handling the request
from flask.cli import with_appcontext

def get_db(): # will be called when application has been created
    if 'db' not in g:
        g.db = sqlite3.connect( # connects to file pointed to by Database configuration key
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8')) # Reading my schema.sql file


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app): # Registers functions with the application instance
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
