import sqlite3
from typing import Generator, List, Dict, Any, Tuple

# Database setup for demonstration
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
    
    # Insert sample data with more users for better pagination demo
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
        (11, 'Kate', 27, 'kate@email.com'),
        (12, 'Liam', 30, 'liam@email.com'),
        (13, 'Mia', 25, 'mia@email.com'),
        (14, 'Noah', 38, 'noah@email.com'),
        (15, 'Olivia', 23, 'olivia@email.com'),
    ]
    
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', sample_users)
    conn.commit()
    return conn

def paginate_users(page_size: int, offset: int) -> Tuple[List[Dict[str, Any]], bool]:
    """
    Fetch a single page of users from the database
    
    Args:
        page_size: Number of users to fetch per page
        offset: Starting position for the page
        
    Returns:
        Tuple containing:
        - List of user dictionaries for the page
        - Boolean indicating if there are more pages
    """
    conn = setup_demo_database()  # In real implementation, use existing connection
    cursor = conn.cursor()
    
    # Fetch one extra record to check if there are more pages
    cursor.execute(
        "SELECT id, name, age, email FROM users LIMIT ? OFFSET ?", 
        (page_size + 1, offset)
    )
    
    rows = cursor.fetchall()
    
    # Check if there are more pages
    has_more = len(rows) > page_size
    
    # Only return the requested page size
    if has_more:
        rows = rows[:page_size]
    
    # Convert rows to dictionaries
    users = []
    for row in rows:
        user_dict = {
            'id': row[0],
            'name': row[1], 
            'age': row[2],
            'email': row[3]
        }
        users.append(user_dict)
    
    conn.close()
    return users, has_more

def lazy_paginate(page_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Generator that lazily loads pages of users from the database
    Only fetches the next page when needed, starting at offset 0
    
    Args:
        page_size: Number of users to fetch per page
        
    Yields:
        List of user dictionaries for each page
    """
    offset = 0
    
    # Single loop: Continue fetching pages until no more data
    while True:
        # Fetch the current page
        page_data, has_more = paginate_users(page_size, offset)
        
        # If no data returned, we're done
        if not page_data:
            break
            
        # Yield the current page
        yield page_data
        
        # If no more pages, stop
        if not has_more:
            break
            
        # Move to the next page
        offset += page_size

# Example usage and demonstration
def main():
    """Demonstrate the lazy pagination functionality"""
    print("=== Lazy Pagination Demo ===\n")
    
    page_size = 4
    print(f"Fetching users with page size: {page_size}")
    print("Pages are loaded lazily - only when requested\n")
    
    page_count = 0
    total_users = 0
    
    # Demonstrate lazy loading - each page is only fetched when the loop advances
    for page in lazy_paginate(page_size):
        page_count += 1
        print(f"📄 Page {page_count} (fetched lazily):")
        
        for user in page:
            print(f"  - ID: {user['id']}, Name: {user['name']}, Age: {user['age']}")
            total_users += 1
        
        print(f"  Users on this page: {len(page)}")
        print()
        
        # Simulate some processing time to show lazy loading
        import time
        time.sleep(0.1)
    
    print(f"📊 Summary:")
    print(f"Total pages fetched: {page_count}")
    print(f"Total users processed: {total_users}")

def demonstrate_lazy_behavior():
    """Show that pages are only fetched when needed"""
    print("\n=== Demonstrating Lazy Behavior ===")
    print("Creating generator (no database calls yet)...")
    
    paginator = lazy_paginate(3)
    print("✅ Generator created - no data fetched yet!")
    
    print("\nFetching first page...")
    first_page = next(paginator)
    print(f"✅ First page fetched: {len(first_page)} users")
    
    print("\nFetching second page...")
    second_page = next(paginator)
    print(f"✅ Second page fetched: {len(second_page)} users")
    
    print("\n💡 Each page is only fetched when next() is called!")

if __name__ == "__main__":
    main()
    demonstrate_lazy_behavior()
