import mysql.connector
import functools

def with_db_connection(func):
    """
    Decorator that opens a database connection,
    passes it to the function, and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",         # change if different
            password="password", # change if different
            database="ALX_prodev"
        )
        try:
            result = func(connection, *args, **kwargs)
        finally:
            connection.close()
        return result
    return wrapper


# Example usage
@with_db_connection
def get_users(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    rows = cursor.fetchall()
    cursor.close()
    return rows


if __name__ == "__main__":
    users = get_users()
    for user in users:
        print(user)
