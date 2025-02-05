from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Load environment variables
load_dotenv()

class DatabaseConnection:
    _instance = None
    _connection = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DatabaseConnection()
        return cls._instance

    def connect(self):
        if not self._connection or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST'),
                    database=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD')
                )
                if self._connection.is_connected():
                    print("Successfully connected to the database!")
                    
                    # Get and print database version
                    cursor = self._connection.cursor()
                    cursor.execute("SELECT VERSION()")
                    db_version = cursor.fetchone()
                    print(f"MySQL database version: {db_version[0]}")
                    
                    # Get and print list of tables
                    cursor.execute("SHOW TABLES;")
                    tables = cursor.fetchall()
                    
                    print("\nList of tables in the database:")
                    print("--------------------------------")
                    for (table_name,) in tables:
                        print(f"- {table_name}")
                    
                    cursor.close()
            except Error as e:
                print(f"Error connecting to database: {e}")
                raise e
        return self._connection

    def get_connection(self):
        return self.connect()

    def close(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Database connection closed.")
            self._connection = None

# Global function to get database connection
def get_db_connection():
    return DatabaseConnection.get_instance().get_connection()

# Global function to close database connection
def close_db_connection():
    DatabaseConnection.get_instance().close()

# Invoice-related database operations
def get_employees():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT employee_id, CONCAT(first_name, ' ', last_name) as full_name 
            FROM employees 
            WHERE status = 'active'
            ORDER BY first_name, last_name
        """)
        employees = cursor.fetchall()
        cursor.close()
        return employees
    except Error as e:
        print(f"Error fetching employees: {e}")
        return []

def get_invoices():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                i.invoice_id,
                CONCAT(e.first_name, ' ', e.last_name) as employee_name,
                e.email as employee_email,
                i.invoice_number,
                i.amount,
                s.bonus,
                i.issue_date,
                i.status
            FROM invoices i
            JOIN employees e ON i.employee_id = e.employee_id
            LEFT JOIN salaries s ON i.employee_id = s.employee_id 
                AND MONTH(i.issue_date) = MONTH(s.payment_date)
                AND YEAR(i.issue_date) = YEAR(s.payment_date)
            ORDER BY i.issue_date DESC
        """)
        invoices = cursor.fetchall()
        cursor.close()
        return invoices
    except Error as e:
        print(f"Error fetching invoices: {e}")
        return []

def create_invoice(employee_id, amount, issue_date, due_date):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Generate invoice number (INV-YYYYMM-XXX)
        cursor.execute("""
            SELECT COUNT(*) + 1 as next_num 
            FROM invoices 
            WHERE YEAR(issue_date) = YEAR(%s) AND MONTH(issue_date) = MONTH(%s)
        """, (issue_date, issue_date))
        next_num = cursor.fetchone()[0]
        invoice_number = f"INV-{issue_date.strftime('%Y%m')}-{str(next_num).zfill(3)}"
        
        print(f"Creating invoice: {invoice_number} for employee {employee_id}")  # Debug print
        
        # Insert new invoice
        cursor.execute("""
            INSERT INTO invoices 
            (employee_id, invoice_number, amount, issue_date, due_date, status) 
            VALUES (%s, %s, %s, %s, %s, 'draft')
        """, (employee_id, invoice_number, amount, issue_date, due_date))
        
        invoice_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        print(f"Created invoice with ID: {invoice_id}")  # Debug print
        return invoice_id
    except Error as e:
        print(f"Error creating invoice: {e}")
        return None

def update_invoice_status(invoice_id, status):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE invoices 
            SET status = %s 
            WHERE invoice_id = %s
        """, (status, invoice_id))
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        print(f"Error updating invoice status: {e}")
        return False

def get_employee_salary(employee_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT base_salary, bonus 
            FROM salaries 
            WHERE employee_id = %s 
            ORDER BY payment_date DESC 
            LIMIT 1
        """, (employee_id,))
        salary = cursor.fetchone()
        cursor.close()
        print(f"Found salary for employee {employee_id}: {salary}")  # Debug print
        return salary
    except Error as e:
        print(f"Error fetching employee salary: {e}")
        return None
