import sqlite3
from typing import Generator, List, Dict, Any

# Simulated database setup for demonstration
def setup_demo_database():
    """Create a demo database with sample user data"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT
        )
    ''')
    
    # Insert sample data
    sample_users = [
        (1, 'Alice', 28, 'alice@email.com'),
        (2, 'Bob', 22, 'bob@email.com'),
        (3, 'Charlie', 35, 'charlie@email.com'),
        (4, 'Diana', 19, 'diana@email.com'),
        (5, 'Eve', 42, 'eve@email.com'),
        (6, 'Frank', 26, 'frank@email.com'),
        (7, 'Grace', 31, 'grace@email.com'),
        (8, 'Henry', 24, 'henry@email.com'),
        (9, 'Iris', 29, 'iris@email.com'),
        (10, 'Jack', 33, 'jack@email.com'),
    ]
    
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', sample_users)
    conn.commit()
    return conn

def stream_users_in_batches(batch_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Generator that fetches users from database in batches
    
    Args:
        batch_size: Number of records to fetch in each batch
        
    Yields:
        List of user dictionaries for each batch
    """
    conn = setup_demo_database()  # In real implementation, use existing connection
    cursor = conn.cursor()
    
    offset = 0
    
    # Loop 1: Fetch batches from database
    while True:
        cursor.execute(
            "SELECT id, name, age, email FROM users LIMIT ? OFFSET ?", 
            (batch_size, offset)
        )
        
        rows = cursor.fetchall()
        
        if not rows:  # No more data
            break
            
        # Convert rows to dictionaries
        batch = []
        # Loop 2: Convert each row to dictionary
        for row in rows:
            user_dict = {
                'id': row[0],
                'name': row[1], 
                'age': row[2],
                'email': row[3]
            }
            batch.append(user_dict)
        
        yield batch
        offset += batch_size
    
    conn.close()

def batch_processing(batch_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Process each batch to filter users over the age of 25
    
    Args:
        batch_size: Number of records to process in each batch
        
    Yields:
        List of filtered users (age > 25) for each batch
    """
    # Loop 3: Process each batch from the stream
    for batch in stream_users_in_batches(batch_size):
        # Filter users over 25 using list comprehension (no additional loop needed)
        filtered_users = [user for user in batch if user['age'] > 25]
        
        if filtered_users:  # Only yield non-empty batches
            yield filtered_users

# Example usage and demonstration
def main():
    """Demonstrate the batch processing functionality"""
    print("=== Batch Processing Demo ===\n")
    
    batch_size = 3
    print(f"Processing users in batches of {batch_size}")
    print("Filtering users over age 25\n")
    
    batch_count = 0
    total_filtered = 0
    
    for filtered_batch in batch_processing(batch_size):
        batch_count += 1
        print(f"Batch {batch_count}:")
        
        for user in filtered_batch:
            print(f"  - {user['name']}, Age: {user['age']}, Email: {user['email']}")
            total_filtered += 1
        
        print()
    
    print(f"Total users over 25: {total_filtered}")
    print(f"Total batches processed: {batch_count}")

if __name__ == "__main__":
    main()
