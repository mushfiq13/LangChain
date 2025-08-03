# setup_test_db.py
import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Create sample tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        age INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product TEXT,
        amount DECIMAL,
        order_date DATE,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

# Insert sample data
cursor.execute("INSERT INTO users VALUES (1, 'John Doe', 'john@email.com', 30)")
cursor.execute("INSERT INTO users VALUES (2, 'Jane Smith', 'jane@email.com', 25)")
cursor.execute("INSERT INTO orders VALUES (1, 1, 'Laptop', 999.99, '2024-01-15')")
cursor.execute("INSERT INTO orders VALUES (2, 2, 'Phone', 599.99, '2024-01-16')")

conn.commit()
conn.close()
