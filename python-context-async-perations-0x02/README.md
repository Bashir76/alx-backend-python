# Database Context Managers & Async Queries

This project demonstrates how to work with databases in Python using **class-based context managers** and **async I/O with `aiosqlite`**.

---

## **1. DatabaseConnection Context Manager**

### Objective  
Create a class-based context manager to handle opening and closing database connections automatically.

### Implementation  
- The `DatabaseConnection` class uses `__enter__` and `__exit__` to manage SQLite connections.  
- Example usage:  

```python
with DatabaseConnection("users.db") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
