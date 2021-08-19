import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
# @bp.route associates the URL /register with the register view function.
# When Flask receives a request to /auth/register, it will call the register view & use the return value as the response
def register():
    if request.method == 'POST':
        # If the user submitted the form, request.method will be 'POST'.
        # In this case, start validating the input.
        username = request.form['username']
        password = request.form['password']
        # request.form is a special type of dict mapping submitted form keys and values.
        # The user will input their username and password.
        db = get_db()
        # this essitaly opens teh database
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # 26-29 Validate that username and password are not empty.
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."
            # saying you've already regersted go login

        # Validate that username is not already registered by querying the database
        # and checking if a result is returned
        # db.execute takes a SQL query with ? placeholders for any user input
        # and a tuple of values to replace the placeholders with
        # The database library will take care of escaping the values so U R not vulnerable to a SQL injection attack

        # fetchone() returns one row from the query. If the query returned no results, it returns None.
            # DOES THIS MEAN THAT IT RETURNS NONE WHEN THERE IS NO PASSWORD FOR THAT USERNAME
            # AKA NO ACCOUNT ALREADY?
        # Later, fetchall() is used, which returns a list of all results.

        if error is None: # is there is no error (??)
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            # Instead, generate_password_hash() is used to securely hash the password, and that hash is stored.
            # Since this query modifies data, db.commit() needs to be called afterwards to save the changes.
            return redirect(url_for('auth.login'))
        # url_for() generates the URL for the login view based on its name.
        # redirect() generates a redirect response to the generated URL.

        flash(error)  # If validation fails, the error is shown to the user.
        # flash() stores messages that can be retrieved when rendering the template.

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            # session['user_username'] = user['username']
            # global userUsername = user['username']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')
# There are a few differences from the register view:
    # The user is queried first and stored in a variable for later use.

    # check_password_hash() hashes the submitted password in the same way as the stored hash and securely compares them.
    # If they match, the password is valid.

    # session is a dict that stores data across requests.
    # When validation succeeds, the user’s id is stored in a new session.
    # The data is stored in a cookie that is sent to the browser,
    # and the browser then sends it back with subsequent requests
    # Flask securely signs the data so that it can’t be tampered with.

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
# bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested
# load_logged_in_user checks if a user id is stored in the session and gets that user’s data from the database,
# storing it on g.user, which lasts for the length of the request.
# If there is no user id, or if the id doesn’t exist, g.user will be None.


# To log out, you need to remove the user id from the session.
# Then load_logged_in_user won’t load a user on subsequent requests.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# Creating, editing, and deleting blog posts will require a user to be logged in.
# A decorator can be used to check this for each view it’s applied to.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
