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
            balance REAL DEFAULT 0
        )
        """)
        conn.commit()

# -------------------------------
# Add User
# -------------------------------
def add_user(first_name, last_name, email, username, password):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            hashed_password = hash_password(password)

            cursor.execute("""
            INSERT INTO users (first_name, last_name, email, username, password)
            VALUES (?, ?, ?, ?, ?)
            """, (first_name, last_name, email, username, hashed_password))

            conn.commit()
            print("User added successfully.")

    except sqlite3.IntegrityError as e:
        print("Error:", e)

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
            (first_name, last_name, email, username, password, balance)
            VALUES (?, ?, ?, ?, ?, ?)
            """, ("Admin", "User", "admin@example.com", "admin", hashed_password, 0))

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

def query_database():
    query = input("Enter SQL query: ")

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)

            # Handle SELECT vs others
            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                for row in rows:
                    print(dict(row))
            else:
                conn.commit()
                print("Query executed successfully.")

    except Exception as e:
        print("Error:", e)

# -------------------------------
# CLI
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database Management")

    parser.add_argument('--add-admin', action='store_true', help="Add default admin user")
    parser.add_argument('--delete-user', type=int, help="Delete user by ID")
    parser.add_argument('--query-users', action='store_true', help="Show all users")
    parser.add_argument('--query-database', action='store_true', help="Run custom SQL query")

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