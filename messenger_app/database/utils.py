# SQLlite imports
import sqlite3

# Click Imports
import click

# Flask Imports
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    Get Database Connection
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Close Database Connection
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def initialize_db():
    """
    Initialize The Database -- Uses Schema to Load Into Database
    """
    db = get_db()
    with current_app.open_resource('database\schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def initialize_db_command():
    """
    Delete all Data and Create New Tables.
    """
    initialize_db()
    click.echo('Donzo....DATABASE READY!')


def initialize_app(app):
    """
    Initialize Flask App -- Registers The Two Functions In The Instance
    """
    # Close Database Connection After Response
    app.teardown_appcontext(close_db)
    # Add 'init-db' To Flask Commands
    app.cli.add_command(initialize_db_command)