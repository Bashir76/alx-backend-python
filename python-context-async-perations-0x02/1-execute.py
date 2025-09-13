import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=(), db_name="users.db"):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


# ✅ Usage
if __name__ == "__main__":
    with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
        print("Users older than 25:", results)

