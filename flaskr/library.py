from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('library', __name__)


@bp.route('/')
def index():
    db = get_db()
    # i dont think this above line is needed

    # userUsername = session.get('user_username')

    userUsername = 'reece'

    booksV = db.execute(
        'SELECT *'
        'FROM books'
        'ORDER BY title DESC'
    ).fetchall()
    
    return str(booksV[0])
    #return render_template('book/library.html', books = booksV)
# books in line above is the line 11 in library.html

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        username = request.form['username']
        title = request.form['title']
        error = None

        db = get_db()
        if not title:
            error = 'Title is required.'


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO books (username, title) VALUES (?, ?)',
                (username, title)
            )
            db.commit()
            return redirect(url_for('library.index'))
        # u only get redirected to index if you "POST" (click)

    return render_template('book/newBook.html')

# the /create URL is the newBook html file
