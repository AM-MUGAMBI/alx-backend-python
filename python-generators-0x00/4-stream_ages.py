import sqlite3
from typing import Generator

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
    
    # Insert sample data with various ages
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
        (16, 'Paul', 45, 'paul@email.com'),
        (17, 'Quinn', 21, 'quinn@email.com'),
        (18, 'Rachel', 34, 'rachel@email.com'),
        (19, 'Sam', 26, 'sam@email.com'),
        (20, 'Tina', 32, 'tina@email.com'),
    ]
    
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', sample_users)
    conn.commit()
    return conn

def stream_user_ages() -> Generator[int, None, None]:
    """
    Generator that yields user ages one by one from the database
    This allows processing large datasets without loading everything into memory
    
    Yields:
        Individual user ages as integers
    """
    conn = setup_demo_database()  # In real implementation, use existing connection
    cursor = conn.cursor()
    
    # Fetch ages one at a time using a cursor
    cursor.execute("SELECT age FROM users")
    
    # Loop 1: Fetch and yield ages one by one
    while True:
        row = cursor.fetchone()
        if row is None:  # No more data
            break
        yield row[0]  # Yield the age
    
    conn.close()

def calculate_average_age() -> float:
    """
    Calculate the average age using the generator without loading all data into memory
    Uses running sum and count to compute average efficiently
    
    Returns:
        Average age as a float
    """
    total_age = 0
    count = 0
    
    # Loop 2: Process each age from the generator
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0.0
    
    return total_age / count

def demonstrate_memory_efficiency():
    """Show how the generator processes data efficiently"""
    print("=== Memory-Efficient Age Calculation Demo ===\n")
    print("🔄 Streaming user ages one by one...")
    print("💾 Only one age is in memory at any given time\n")
    
    # Show individual ages being processed (for demonstration)
    print("Processing ages:")
    age_count = 0
    running_sum = 0
    
    for age in stream_user_ages():
        age_count += 1
        running_sum += age
        current_avg = running_sum / age_count
        print(f"  Age {age_count}: {age} (running average: {current_avg:.2f})")
        
        # Only show first 10 for brevity
        if age_count >= 10:
            print("  ... (continuing with remaining ages)")
            break
    
    print()

def main():
    """Main function to demonstrate the average age calculation"""
    # First show the streaming process
    demonstrate_memory_efficiency()
    
    # Calculate and display the final average
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")
    
    # Show memory efficiency benefits
    print(f"\n💡 Memory Efficiency Benefits:")
    print("✅ Only one age value in memory at any time")
    print("✅ Can process millions of records with constant memory usage")
    print("✅ No need to load entire dataset before calculation")

if __name__ == "__main__":
    main()
