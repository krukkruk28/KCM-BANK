import flask
import json
import os
import sqlite3
from db import get_connection, hash_password

app = flask.Flask(__name__)
# app.secret_key = os.getenv("SECRET_KEY")

# Load user data
def load_users():
    with open('usersdb.json', 'r') as f:
        return json.load(f)

# Save user data
def save_users(users):
    with open('usersdb.json', 'w') as f:
        json.dump(users, f, indent=4)

# Get user by username
def get_user_by_username(username):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

@app.route('/')
def home():
    if 'username' in flask.session:
        return flask.redirect('/dashboard')
    return flask.redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form.get('username', '')
        password = flask.request.form.get('password', '')

        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                flask.session['username'] = username
                return flask.redirect('/dashboard')

        error = 'Invalid username or password'
        return flask.render_template('login.html', error=error, username=username)

    return flask.render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in flask.session:
        return flask.redirect('/login')

    username = flask.session['username']
    user = get_user_by_username(username)
    balance = user['balance'] if user else 0

    return flask.render_template('login_interface.html', username=username, balance=balance)

@app.route('/transaction', methods=['POST'])
def transaction():
    if 'username' not in flask.session:
        return flask.redirect('/login')

    username = flask.session['username']
    try:
        amount = float(flask.request.form['amount'])
    except ValueError:
        flask.flash('Invalid amount entered')
        return flask.redirect('/dashboard')

    user = get_user_by_username(username)
    current_balance = user['balance'] if user else 0

    if amount < 0 and abs(amount) > current_balance:
        flask.flash('Insufficient funds')
        return flask.redirect('/dashboard')

    # Update balance and save to JSON
    users = load_users()
    for user in users:
        if user['username'] == username:
            user['balance'] = current_balance + amount
            break
    save_users(users)

    if amount > 0:
        flask.flash(f'Successfully deposited ${amount:.2f}')
    else:
        flask.flash(f'Successfully withdrew ${abs(amount):.2f}')

    return flask.redirect('/dashboard')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    status = None

    if flask.request.method == "POST":
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')

        users = load_users()

        # Check if user already exists
        if any(user['username'] == username for user in users):
            status = 'exists'
        else:
            # Add new user
            users.append({
                "username": username,
                "password": password,
                "balance": 0
            })
            save_users(users)
            status = 'success'

            # Optional: auto login after signup
            flask.session['username'] = username

    return flask.render_template('signup.html', status=status)

@app.route('/logout')
def logout():
    flask.session.pop('username', None)
    return flask.redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)


