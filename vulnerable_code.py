import sqlite3
import os

# 1. Hardcoded Credentials in plain text
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123!"
API_KEY = "12345-ABCDE-67890-FGHIJ"

def authenticate_user(username, password):
    """Authenticates a user against the database."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 2. SQL Injection Vulnerability (string concatenation)
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    cursor.execute(query)
    user = cursor.fetchone()
    
    conn.close()
    return user is not None

def read_user_document(filename):
    """Reads a document provided by the user."""
    # 3. Path Traversal Vulnerability (no sanitization of filename)
    base_dir = "/var/app/documents/"
    filepath = base_dir + filename
    
    with open(filepath, 'r') as file:
        return file.read()

def calculate_average_order_value(total_revenue, order_count):
    """Calculates the average order value for metrics."""
    # 4. Divide-by-zero Possibility (no check if order_count is 0)
    return total_revenue / order_count

def process_payment(user_data):
    """Processes payment for a given user."""
    # 5. Missing Null / Type check
    # If user_data is None, or 'credit_card' is missing/None, this crashes with an AttributeError
    card_number = user_data.get('credit_card').replace(' ', '')
    
    # 6. Logging sensitive information
    print(f"Processing payment for card: {card_number}")
    
    return True
