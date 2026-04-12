import flask
from datetime import datetime

from db import (
    add_user,
    verify_password,
    update_balance,
    init_db,
    get_user_by_username,
    get_connection
)

from Dashboard import dashboard_bp  

app = flask.Flask(__name__)
app.secret_key = "super_secret_key_123"

# -------------------------------
# INIT
# -------------------------------
init_db()

# ✅ REGISTER BLUEPRINT
app.register_blueprint(dashboard_bp)


# -------------------------------
# HOME
# -------------------------------
@app.route('/')
def home():
    if 'username' in flask.session:
        return flask.redirect('/dashboard')
    return flask.redirect('/login')


# -------------------------------
# LOGIN
# -------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form.get('username', '')
        password = flask.request.form.get('password', '')

        user = get_user_by_username(username)

        if user and verify_password(password, user["password"]):
            flask.session['username'] = username
            flask.session['login_time'] = datetime.utcnow().isoformat()
            return flask.redirect('/dashboard')

        error = 'Invalid username or password'
        return flask.render_template('login.html', error=error, username=username)

    return flask.render_template('login.html')


# -------------------------------
# SIGNUP
# -------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    status = None

    if flask.request.method == "POST":
        first_name = flask.request.form.get('firstname')
        last_name = flask.request.form.get('lastname')
        email = flask.request.form.get('email')
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')

        if not all([first_name, last_name, email, username, password]):
            status = "missing"
            return flask.render_template('signup.html', status=status)

        success = add_user(first_name, last_name, email, username, password)

        if success:
            flask.session['username'] = username
            return flask.redirect('/dashboard')
        else:
            status = "exists"

    return flask.render_template('signup.html', status=status)


# -------------------------------
# TRANSACTION
# -------------------------------
@app.route('/transaction', methods=['POST'])
def transaction():
    if 'username' not in flask.session:
        return flask.redirect('/login')

    try:
        amount = float(flask.request.form['amount'])
    except ValueError:
        flask.flash('Invalid amount')
        return flask.redirect('/dashboard')

    result = update_balance(flask.session['username'], amount)

    if result == "insufficient":
        flask.flash("Insufficient funds")
    elif result is None:
        flask.flash("User not found")
    else:
        flask.flash(f"Transaction successful. New balance: {result:.2f}")

    return flask.redirect('/dashboard')


# -------------------------------
# LOGOUT
# -------------------------------
@app.route('/logout')
def logout():
    username = flask.session.get('username')
    login_time = flask.session.get('login_time')

    if username and login_time:
        user = get_user_by_username(username)

        if user:
            logout_time = datetime.utcnow()
            try:
                login_dt = datetime.fromisoformat(login_time)
            except Exception:
                login_dt = logout_time

            duration = int((logout_time - login_dt).total_seconds())

            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO user_sessions (user_id, login_time, logout_time, duration_seconds)
                    VALUES (?, ?, ?, ?)
                """, (
                    user["id"],
                    login_time,
                    logout_time.isoformat(),
                    duration
                ))
                conn.commit()

    flask.session.clear()
    return flask.redirect('/login')

# -------------------------------
# RUN
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)