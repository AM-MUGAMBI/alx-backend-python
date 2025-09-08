#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator that streams rows from the user_data table one by one.
    Uses yield to return each row without loading all data into memory.
    
    Yields:
        tuple: Each row from user_data table as (user_id, name, email, age)
    """
    connection = None
    cursor = None
    
    try:
        # Connect to ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',  # Change to your MySQL password
            database='ALX_prodev',
            port=3306,
            ssl_disabled=True
        )
        
        if connection.is_connected():
            cursor = connection.cursor(buffered=False)  # Use unbuffered cursor for streaming
            
            # Execute query to fetch all user data
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            
            # Single loop to yield rows one by one
            for row in cursor:
                yield row
                
    except Error as e:
        print(f"Error connecting to database: {e}")
        return
        
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
