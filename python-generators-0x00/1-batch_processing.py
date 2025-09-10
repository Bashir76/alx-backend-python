import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows in batches from the user_data table.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",         # <-- update if different
        password="password", # <-- update if different
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    offset = 0
    while True:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s;", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows   # ✅ yield instead of return
        offset += batch_size

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes batches and yields users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1
        filtered = [user for user in batch if user["age"] > 25]  # loop 2 (list comp)
        if filtered:
            yield filtered   # ✅ yield, not return


if __name__ == "__main__":
    for processed_batch in batch_processing(3):  # loop 3
        print("Filtered batch:", processed_batch)
