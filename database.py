import sqlite3

# Connect to the SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect("bot_database.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS warnings (
    user_id INTEGER,
    chat_id INTEGER,
    warning_count INTEGER,
    PRIMARY KEY (user_id, chat_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    admin_id INTEGER PRIMARY KEY
)
""")

conn.commit()

# Function to add a warning to a user
def add_warning(user_id, chat_id):
    cursor.execute("SELECT warning_count FROM warnings WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
    result = cursor.fetchone()

    if result:
        warning_count = result[0] + 1
        cursor.execute("UPDATE warnings SET warning_count = ? WHERE user_id = ? AND chat_id = ?", (warning_count, user_id, chat_id))
    else:
        cursor.execute("INSERT INTO warnings (user_id, chat_id, warning_count) VALUES (?, ?, ?)", (user_id, chat_id, 1))
    
    conn.commit()

# Function to get the number of warnings for a user
def get_warnings(user_id, chat_id):
    cursor.execute("SELECT warning_count FROM warnings WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
    result = cursor.fetchone()
    return result[0] if result else 0

# Function to reset warnings after unban
def reset_warnings(user_id, chat_id):
    cursor.execute("DELETE FROM warnings WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
    conn.commit()

# Function to add an admin
def add_admin(admin_id):
    cursor.execute("INSERT OR IGNORE INTO admins (admin_id) VALUES (?)", (admin_id,))
    conn.commit()

# Function to remove an admin
def remove_admin(admin_id):
    cursor.execute("DELETE FROM admins WHERE admin_id = ?", (admin_id,))
    conn.commit()

# Function to check if a user is an admin
def is_admin(admin_id):
    cursor.execute("SELECT admin_id FROM admins WHERE admin_id = ?", (admin_id,))
    return cursor.fetchone() is not None

# Function to list all admins
def list_admins():
    cursor.execute("SELECT admin_id FROM admins")
    return [row[0] for row in cursor.fetchall()]
