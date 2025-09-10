import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that fetches rows in batches from the user_data table."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",       # update with your MySQL username
        password="password", # update with your MySQL password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Processes each batch to filter users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):   # loop 1
        filtered = [user for user in batch if user["age"] > 25]  # loop 2 (list comprehension counts as a loop)
        yield filtered


# Example usage
if __name__ == "__main__":
    for batch in batch_processing(3):   # loop 3
        print("Processed batch:", batch)

