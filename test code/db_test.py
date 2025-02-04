import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

def get_connection():
    try:
        # Get database connection details from environment variables
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        
        if connection.is_connected():
            print("Successfully connected to the database!")
            
            # Get and print database version
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION();")
            db_version = cursor.fetchone()
            print(f"MySQL database version: {db_version[0]}")
            
            cursor.close()
            return connection
    
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None
    
if __name__ == "__main__":
    # Try to establish connection
    connection = get_connection()
    
    # Close connection if it was successful
    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed.")
