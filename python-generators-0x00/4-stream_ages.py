import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",         # <-- change if different
        password="password", # <-- change if different
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    for (age,) in cursor:   # loop 1
        yield age
    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Calculate the average age using the generator without loading all rows into memory.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():  # loop 2
        total_age += age
        count += 1

    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age}")


if __name__ == "__main__":
    calculate_average_age()

