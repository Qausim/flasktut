from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3


app = Flask(__name__)

# Create secret key for cookies
app.secret_key = 'my nigga'
# Link db name to app
app.database = 'sample.db'


# Define functions to for db connection
def connect_db():
    return sqlite3.connect(app.database)

def run_query(query_str, on_complete):
    g.db = connect_db()
    cursor = g.db.execute(query_str)
    result = on_complete(cursor.fetchall())
    g.db.close()
    return result


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print('logged_in' in session)
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# default method is get
@app.route('/')
@login_required
def home():
    posts = run_query(
        'SELECT * FROM posts',
        lambda cursor: [dict(title=row[0], desc=row[1]) for row in cursor]
    )
    return render_template('index.html', posts=posts)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credential please try again'
        else:
            session['logged_in'] = True
            flash('You just logged in!')
            # redirect passing name of function to redirect to url_for
            return redirect(url_for('home'))

    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in')
    flash('You just logged out!')
    return redirect(url_for('welcome'))


if __name__ == '__main__':
    app.run(debug=True)
