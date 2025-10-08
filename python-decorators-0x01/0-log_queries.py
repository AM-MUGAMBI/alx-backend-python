import sqlite3
import functools

# ✅ Decorator to log SQL queries (without using datetime)
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get query from kwargs or args
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"[SQL LOG] Executing query: {query}")
        else:
            print("[SQL LOG] No SQL query found in arguments.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Run the function and log the query
users = fetch_all_users(query="SELECT * FROM users")

