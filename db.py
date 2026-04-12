import sqlite3
import argparse
import bcrypt
from datetime import datetime

DB_NAME = "app.db"

# -------------------------------
# Connection
# -------------------------------
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# -------------------------------
# Password Hashing
# -------------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# -------------------------------
# Initialize DB
# -------------------------------
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT UNIQUE,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT CHECK(role IN ('admin','user')) DEFAULT 'user',
            balance REAL DEFAULT 0
        )
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            login_time TEXT,
            logout_time TEXT,
            duration_seconds INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            duration_seconds INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL,
            type TEXT CHECK(type IN ('deposit','withdraw')),
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)
        """)

        conn.commit()

# -------------------------------
# Add User
# -------------------------------
def add_user(first_name, last_name, email, username, password, role='user', balance=0):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            hashed_password = hash_password(password)

            cursor.execute("""
            INSERT INTO users (first_name, last_name, email, username, password, role, balance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, email, username, hashed_password, role, balance))

            conn.commit()

            user_id = cursor.lastrowid
            print("User added successfully.")

            return user_id

    except sqlite3.IntegrityError as e:
        print("Error:", e)
        return None

# -------------------------------
# Update Balance
# -------------------------------

def update_balance(username, amount):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id, balance FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if not user:
            return None

        current_balance = user["balance"]
        new_balance = current_balance + amount

        if new_balance < 0:
            return "insufficient"

        # update balance
        cursor.execute("""
            UPDATE users SET balance = ? WHERE id = ?
        """, (new_balance, user["id"]))

        cursor.execute("""
            INSERT INTO transactions (user_id, amount, type, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            user["id"],
            amount,
            "deposit" if amount > 0 else "withdraw",
            datetime.utcnow().isoformat()
        ))

        conn.commit()

        return new_balance

# -------------------------------
# Get user by username
# -------------------------------

def get_user_by_username(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

# -------------------------------
# Add Default Admin
# -------------------------------
def add_admin_user():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            hashed_password = hash_password("admin123")

            cursor.execute("""
            INSERT OR IGNORE INTO users 
            (first_name, last_name, email, username, password, role, balance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ("Admin", "User", "admin@example.com", "admin", hashed_password, "admin", 0))

            conn.commit()
            print("Admin user added (or already exists).")

    except sqlite3.Error as e:
        print("Error:", e)

# -------------------------------
# Log Action
# -------------------------------
def log_action(user_id, action, duration=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_actions (user_id, action, timestamp, duration_seconds)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            action,
            datetime.utcnow().isoformat(),
            duration
        ))
        conn.commit()

# -------------------------------
# Delete User
# -------------------------------
def delete_user(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        if cursor.rowcount:
            print(f"User {user_id} deleted.")
        else:
            print("User not found.")


# -------------------------------
# Query User ID
# -------------------------------
def get_user_id(username):
    user = get_user_by_username(username)
    return user["id"] if user else None

# -------------------------------
# Query Users - For admin
# -------------------------------

def query_database():
    query = input("Enter SQL query: ").strip()

    if not query.lower().startswith("select"):
        print("Only SELECT queries are allowed.")
        return

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)

            rows = cursor.fetchall()

            if not rows:
                print("No results.")
                return

            for row in rows:
                print(dict(row))

    except Exception as e:
        print("Error:", e)

# -------------------------------
# Delete Database - For admin (Not advisable in production)
# -------------------------------

def delete_database():
    import os

    confirm = input("⚠️ Are you sure you want to delete the database? (yes/no): ")

    if confirm.lower() != "yes":
        print("Cancelled.")
        return

    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("Database deleted.")
    else:
        print("Database not found.")

# -------------------------------
# CLI
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database Management")

    parser.add_argument('--add-admin', action='store_true', help="Add default admin user")
    parser.add_argument('--delete-user', type=int, help="Delete user by ID")
    parser.add_argument('--query-users', action='store_true', help="Show all users")
    parser.add_argument('--query-database', action='store_true', help="Run custom SQL query")
    parser.add_argument('--delete-database', action='store_true', help="Delete the entire database")

    args = parser.parse_args()

    init_db()
    print("Database initialized.")

    if args.add_admin:
        add_admin_user()

    if args.delete_user:
        delete_user(args.delete_user)

    if args.query_database:
        query_database()

    if args.delete_database:
        delete_database()