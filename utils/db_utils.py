import sqlite3

def create_connection():
    return sqlite3.connect('db/bot_users.db')

def create_group_settings_connection():
    return sqlite3.connect('db/group_settings.db')

def create_users_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_group_settings_table():
    conn = create_group_settings_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            group_id INTEGER PRIMARY KEY,
            rules TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_user(user_id, full_name, username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, full_name, username) VALUES (?, ?, ?)
    ''', (user_id, full_name, username))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def store_group_settings(group_id, rules):
    conn = create_group_settings_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO settings (group_id, rules) VALUES (?, ?)
    ''', (group_id, rules))
    conn.commit()
    conn.close()

def get_group_settings(group_id):
    conn = create_group_settings_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM settings WHERE group_id = ?', (group_id,))
    settings = cursor.fetchone()
    conn.close()
    return settings
