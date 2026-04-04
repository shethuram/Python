import sqlite3

# connect to DB (creates file if not exists)
conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room TEXT,
    username TEXT,
    message TEXT
)
""")

conn.commit()


def save_message(room, username, message):
    cursor.execute(
        "INSERT INTO messages (room, username, message) VALUES (?, ?, ?)",
        (room, username, message)
    )
    conn.commit()


def get_messages(room):
    cursor.execute(
        "SELECT username, message FROM messages WHERE room = ?",
        (room,)
    )
    return cursor.fetchall()


def search_messages(room, keyword):
    cursor.execute(
        "SELECT username, message FROM messages WHERE room=? AND message LIKE ?",
        (room, f"%{keyword}%")
    )
    return cursor.fetchall()