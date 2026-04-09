import sqlite3
import argparse
import bcrypt

DB_NAME = "app.db"

# -------------------------------
# Connection
# -------------------------------
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------------
# Password Hashing
# -------------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    import bcrypt
    return bcrypt.checkpw(password.encode(), hashed.encode())

# -------------------------------
# Initialize DB
# -------------------------------
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            full_name TEXT GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            balance REAL DEFAULT 0
        )
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

        cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if not user:
            return None

        current_balance = user["balance"]
        new_balance = current_balance + amount

        # prevent overdraft
        if new_balance < 0:
            return "insufficient"

        cursor.execute("""
            UPDATE users SET balance = ? WHERE username = ?
        """, (new_balance, username))

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
# Query Users
# -------------------------------
def query_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        if not users:
            print("No users found.")
            return

        for user in users:
            print(dict(user))

# -------------------------------
# Query Users - For admin
# -------------------------------

def query_database():
    query = input("Enter SQL query: ").strip()

    # 🔐 Restrict to SELECT only (safer)
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
# Delete Database - For admin
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

    if args.query_users:
        query_users()

    if args.query_database:
        query_database()

    if args.delete_database:
        delete_database()