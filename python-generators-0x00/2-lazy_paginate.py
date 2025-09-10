import mysql.connector

def paginate_users(page_size, offset):
    """Fetch a page of users from the database based on page size and offset."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",       # update with your MySQL username
        password="password", # update with your MySQL password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s;", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """Generator that lazily fetches pages of users from the database."""
    offset = 0
    while True:   # only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# Example usage
if __name__ == "__main__":
    for page in lazy_paginate(2):  # This will lazily fetch 2 users per page
        print("Page:", page)

