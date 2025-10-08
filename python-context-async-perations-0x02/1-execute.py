import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results  # Returned to the `as` variable in the `with` statement

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Usage Example:
if __name__ == "__main__":
    # Setup DB and test data
    with sqlite3.connect('example.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        ''')
        cur.executemany('''
            INSERT OR IGNORE INTO users (id, name, age) VALUES (?, ?, ?)
        ''', [
            (1, 'Alice', 30),
            (2, 'Bob', 20),
            (3, 'Charlie', 35)
        ])
        conn.commit()

    # Use the context manager to execute a SELECT query with parameters
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery('example.db', query, params) as results:
        for row in results:
            print(row)

