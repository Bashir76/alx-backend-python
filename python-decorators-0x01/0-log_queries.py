import functools

def log_queries(func):
    """
    Decorator that logs SQL queries executed by the wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        if query:
            print(f"[LOG] Executing SQL query: {query}")
        return func(*args, **kwargs)
    return wrapper


# Example usage
@log_queries
def execute_query(query):
    # Simulate executing the query
    return f"Query executed: {query}"


if __name__ == "__main__":
    print(execute_query("SELECT * FROM user_data;"))
