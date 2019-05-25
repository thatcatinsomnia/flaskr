import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# creates a Blueprint named 'auth'
# url_prefix will be prepended to all the URLs associated with the blueprint.
bp = Blueprint('auth', __name__, url_prefix='/auth')

# associates the URL /register with the register view function
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        db = get_db()
        error = None

        # username and password are not empty.
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif repassword != password:
            error = 'The Password and confirm password is different'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)   # check if username exist or not
        ).fetchone() is not None:
            error = f'User {username} is already exist'

        # pass the validation
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))    # password should be hash
            )
            db.commit()
            return redirect(url_for('auth.login'))  # redirect to login page after register

        # validation fails show error to the user
        # flash() stores messages that can be retrieved when rendering the template.
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # get user from db
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        ).fetchone()
        print(f'user = {user}')
        # check username and password
        if user is None:
            error = 'Username is not exist.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        # store session if validation succeed
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# runs before the view function, no matter what URL is requested. 
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    # get user data from db if session['user_id'] is exist
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# clear session when logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# decoration for check if user login or not
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

