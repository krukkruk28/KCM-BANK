import flask

from db import (
    get_user_by_username,
    create_user,
    verify_password,
    update_balance,
    init_db
)

app = flask.Flask(__name__)
# app.secret_key = os.getenv("SECRET_KEY")
app.secret_key = 123456789  # Change this to a secure secret key. It's only for educational purposes, use os.getenvfor production use.

# -------------------------------
# Init DB
# -------------------------------
init_db()

# -------------------------------
# Routes
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
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')

        user = get_user_by_username(username)

        if user and verify_password(password, user["password"]):
            flask.session['username'] = username
            return flask.redirect('/dashboard')

        return flask.render_template('login.html', error="Invalid credentials")

    return flask.render_template('login.html')


# -------------------------------
# SIGNUP
# -------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    status = None

    if flask.request.method == 'POST':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')

        success = create_user(
            "User", "Default",
            f"{username}@mail.com",
            username,
            password
        )

        if success:
            flask.session['username'] = username
            return flask.redirect('/dashboard')
        else:
            status = "exists"

    return flask.render_template('signup.html', status=status)


# -------------------------------
# DASHBOARD
# -------------------------------
@app.route('/dashboard')
def dashboard():
    if 'username' not in flask.session:
        return flask.redirect('/login')

    user = get_user_by_username(flask.session['username'])

    return flask.render_template(
        'login_interface.html',
        username=user["username"],
        balance=user["balance"]
    )


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
        flask.flash("Invalid amount")
        return flask.redirect('/dashboard')

    result = update_balance(flask.session['username'], amount)

    if result == "insufficient":
        flask.flash("Insufficient funds")
    elif result is None:
        flask.flash("User not found")
    else:
        flask.flash(f"New balance: {result:.2f}")

    return flask.redirect('/dashboard')


# -------------------------------
# LOGOUT
# -------------------------------
@app.route('/logout')
def logout():
    flask.session.pop('username', None)
    return flask.redirect('/login')


# -------------------------------
# RUN
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)