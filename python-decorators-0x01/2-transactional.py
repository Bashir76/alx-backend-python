Objective: create a decorator that manages database transactions by automatically committing or rolling back changes

Instructions:

Complete the script below by writing a decorator transactional(func) that ensures a function running a database operation is wrapped inside a transaction.If the function raises an error, rollback; otherwise commit the transaction.

Copy the with_db_connection created in the previous task into the script
