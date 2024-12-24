import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("db_billiard_app.db")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

# Create users table if it doesn't exist
cur.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            username TEXT UNIQUE,
            phone INT,
            gender TEXT)""")
conn.commit()

# Create tables table if it doesn't exist
cur.execute("""CREATE TABLE IF NOT EXISTS tables (id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INT UNIQUE,
            table_name TEXT,
            price INT)""")
conn.commit()

# Create bookings table if it doesn't exist
cur.execute("""CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            booking_time TIME,
            duration INT,
            table_number INT,
            table_name TEXT,
            price INT,
            payment_method TEXT,
            booking_date DATETIME,
            FOREIGN KEY (username) REFERENCES users (username) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (table_number) REFERENCES tables (table_number) ON UPDATE CASCADE ON DELETE CASCADE)""")
conn.commit()
