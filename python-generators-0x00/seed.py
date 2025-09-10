import mysql.connector
import csv
import uuid

# ---------- PROTOTYPES ----------

def connect_db():
    """Connects to the MySQL database server (without selecting DB)."""
    return mysql.connector.connect(
        host="localhost",
        user="root",       # update with your MySQL username
        password="password" # update with your MySQL password
    )

def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    return mysql.connector.connect(
        host="localhost",
        user="root",       # update with your MySQL username
        password="password", # update with your MySQL password
        database="ALX_prodev"
    )

def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            age DECIMAL NOT NULL,
            INDEX idx_user_id (user_id)
        );
    """)
    cursor.close()

def insert_data(connection, data):
    """Inserts data in the database if it does not exist."""
    cursor = connection.cursor()
    for row in data:
        user_id = str(uuid.uuid4())
        name, email, age = row
        try:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
            """, (user_id, name, email, age))
        except Exception as e:
            print(f"Error inserting row {row}: {e}")
    connection.commit()
    cursor.close()


# ---------- MAIN SCRIPT ----------

if __name__ == "__main__":
    # Step 1: Connect to MySQL server
    conn = connect_db()
    create_database(conn)
    conn.close()

    # Step 2: Connect to ALX_prodev DB
    conn_prodev = connect_to_prodev()

    # Step 3: Create table if not exists
    create_table(conn_prodev)

    # Step 4: Load data from CSV and insert
    with open("user_data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        insert_data(conn_prodev, list(reader))

    conn_prodev.close()
    print("Database seeded successfully!")

