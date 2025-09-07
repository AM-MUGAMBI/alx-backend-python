#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error
import csv
import uuid
import os
from typing import Optional, List, Dict, Any

def connect_db() -> Optional[mysql.connector.MySQLConnection]:
    """
    Connects to the MySQL database server.
    
    Returns:
        mysql.connector.MySQLConnection: Connection object if successful, None otherwise
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Change to your MySQL username
            password='password',  # Change to your MySQL password
            port=3306
        )
        
        if connection.is_connected():
            print("Successfully connected to MySQL server")
            return connection
            
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None

def create_database(connection: mysql.connector.MySQLConnection) -> bool:
    """
    Creates the database ALX_prodev if it does not exist.
    
    Args:
        connection: MySQL connection object
        
    Returns:
        bool: True if database created/exists, False otherwise
    """
    try:
        cursor = connection.cursor()
        
        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully or already exists")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"Error creating database: {e}")
        return False

def connect_to_prodev() -> Optional[mysql.connector.MySQLConnection]:
    """
    Connects to the ALX_prodev database in MySQL.
    
    Returns:
        mysql.connector.MySQLConnection: Connection object if successful, None otherwise
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Change to your MySQL username
            password='password',  # Change to your MySQL password
            database='ALX_prodev',
            port=3306
        )
        
        if connection.is_connected():
            print("Successfully connected to ALX_prodev database")
            return connection
            
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def create_table(connection: mysql.connector.MySQLConnection) -> bool:
    """
    Creates a table user_data if it does not exist with the required fields.
    
    Args:
        connection: MySQL connection object
        
    Returns:
        bool: True if table created/exists, False otherwise
    """
    try:
        cursor = connection.cursor()
        
        # Create table with required schema
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        
        cursor.execute(create_table_query)
        print("Table user_data created successfully or already exists")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"Error creating table: {e}")
        return False

def insert_data(connection: mysql.connector.MySQLConnection, data: List[Dict[str, Any]]) -> bool:
    """
    Inserts data in the database if it does not exist.
    
    Args:
        connection: MySQL connection object
        data: List of dictionaries containing user data
        
    Returns:
        bool: True if data inserted successfully, False otherwise
    """
    try:
        cursor = connection.cursor()
        
        # Insert query with ON DUPLICATE KEY UPDATE to avoid duplicates
        insert_query = """
        INSERT INTO user_data (user_id, name, email, age) 
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        name = VALUES(name),
        email = VALUES(email),
        age = VALUES(age)
        """
        
        # Prepare data for insertion
        insert_values = []
        for row in data:
            # Generate UUID if not provided or convert existing ID to UUID format
            if 'user_id' not in row or not row['user_id']:
                user_id = str(uuid.uuid4())
            else:
                # Ensure it's a valid UUID format
                try:
                    uuid.UUID(row['user_id'])
                    user_id = row['user_id']
                except ValueError:
                    user_id = str(uuid.uuid4())
            
            insert_values.append((
                user_id,
                row['name'],
                row['email'],
                float(row['age'])
            ))
        
        # Execute batch insert
        cursor.executemany(insert_query, insert_values)
        connection.commit()
        
        print(f"Successfully inserted/updated {cursor.rowcount} records")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
        return False

def read_csv_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads data from CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        List[Dict]: List of dictionaries containing CSV data
    """
    data = []
    
    try:
        if not os.path.exists(file_path):
            print(f"CSV file not found: {file_path}")
            return data
            
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Clean and validate data
                if row.get('name') and row.get('email') and row.get('age'):
                    try:
                        # Validate age is numeric
                        float(row['age'])
                        data.append(row)
                    except ValueError:
                        print(f"Skipping row with invalid age: {row}")
                else:
                    print(f"Skipping row with missing required fields: {row}")
        
        print(f"Successfully read {len(data)} records from CSV")
        return data
        
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return data

def main():
    """
    Main function to set up database and populate with data.
    """
    print("Starting database setup and data seeding...")
    
    # Step 1: Connect to MySQL server
    server_connection = connect_db()
    if not server_connection:
        print("Failed to connect to MySQL server. Exiting...")
        return
    
    # Step 2: Create database
    if not create_database(server_connection):
        print("Failed to create database. Exiting...")
        server_connection.close()
        return
    
    # Close server connection
    server_connection.close()
    
    # Step 3: Connect to ALX_prodev database
    db_connection = connect_to_prodev()
    if not db_connection:
        print("Failed to connect to ALX_prodev database. Exiting...")
        return
    
    # Step 4: Create table
    if not create_table(db_connection):
        print("Failed to create table. Exiting...")
        db_connection.close()
        return
    
    # Step 5: Read CSV data
    csv_file = 'user_data.csv'  # Make sure this file exists in the same directory
    csv_data = read_csv_data(csv_file)
    
    if not csv_data:
        print("No valid data found in CSV file. Exiting...")
        db_connection.close()
        return
    
    # Step 6: Insert data
    if insert_data(db_connection, csv_data):
        print("Database setup and data seeding completed successfully!")
    else:
        print("Failed to insert data.")
    
    # Step 7: Display summary
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        print(f"Total records in database: {count}")
        cursor.close()
    except Error as e:
        print(f"Error getting record count: {e}")
    
    # Close database connection
    db_connection.close()
    print("Database connection closed.")

if __name__ == "__main__":
    main()
