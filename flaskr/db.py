import sqlite3

import click
from flask import current_app, g
# g is a special object that is unique for each request.
# It is used to store data that might be accessed by multiple functions during the request.
# The connection is stored and reused instead of creating a new connection
# if get_db is called a second time in the same request.
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.connect() establishes a connection to the file pointed at by the DATABASE configuration key.
        # This file doesn't have to exist yet, and won’t until you initialize the database later.
        g.db.row_factory = sqlite3.Row
        # sqlite3.Row tells the connection to return rows that behave like dicts.
        # This allows accessing the columns by name.

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        # close_db checks if a connection was created by checking if g.db was set.
        # If the connection exists, it is closed.
        # Further down you will tell your application about the close_db function in the application factory
        # so that it is called after each request.


# below (38-57) adds the Python functions that will run (the code in the schema.sql file) SQL commands to the db.py file
def init_db(): # this function is initilizing the database
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        # havig the app open the SQL script (f is the SQL script)
        db.executescript(f.read().decode('utf8')) # taking f, reading it, & then decoding from BITs 2 english characters
        # db is the database connection
        # when u r executing f u are executing teh SQL code
        # all of the schema.sql text is stored in f


@click.command('init-db') # turning the function into a click command
# click.command() defines a command line command called init-db that calls the init_db function
# and shows a success message to the user.
# You can read Command Line Interface to learn more about writing commands.
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.') # so that we now that the function worked (in the terminal)


# The close_db and init_db_command functions need to be registered with the application instance;
# otherwise, they won’t be used by the application.
# However, since you’re using a factory function, that instance isn’t available when writing the functions.
# Instead, write a function that takes an application and does the registration.
# lines 65-67 is that function
# flask does not have accses to these functions so you have to do this below
def init_app(app):
    app.teardown_appcontext(close_db)
    # app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
    app.cli.add_command(init_db_command)
    # app.cli.add_command() adds a new command that can be called with the flask command.
