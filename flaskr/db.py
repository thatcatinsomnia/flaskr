import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # g is a special object that is unique for each request.
    # return db connection if exist
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], # current_app is Flask application handling the request
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


# closed the connection if it exists
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# init db schema with schema.sql
def init_db():
    db = get_db()

    # open a file relative to the flaskr package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')   # defines a command line command called init-db
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.') # shows a success message to the user. 

# a function that takes an application and does the registration.
def init_app(app):
    # cleaning up after returning the response.
    app.teardown_appcontext(close_db) 

    # adds a new command that can be called with the flask command.
    app.cli.add_command(init_db_command) 