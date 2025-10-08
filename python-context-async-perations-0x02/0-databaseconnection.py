import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection  # This is passed to the `as` part of the `with` statement

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

# Usage Example:
with DatabaseConnection('example.db') as conn:
    cursor = conn.cursor()

    # (Optional) Create a sample table and insert dummy data (if not exists)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')")
    conn.commit()

    # Now perform the required SELECT query
    cursor.execute('SELECT * FROM users')
    results = cursor.fetchall()

    # Print results
    for row in results:
        print(row)

