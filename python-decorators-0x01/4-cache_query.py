import functools

# Simple in-memory cache (dictionary)
_query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(sql_query, *args, **kwargs):
        # If query already in cache, return cached result
        if sql_query in _query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {sql_query}")
            return _query_cache[sql_query]
        
        # Otherwise, execute the query
        print(f"[CACHE MISS] Executing query: {sql_query}")
        result = func(sql_query, *args, **kwargs)

        # Store result in cache
        _query_cache[sql_query] = result
        return result
    return wrapper

# Example usage
@cache_query
def execute_query(sql_query):
    # Simulated DB call
    print(f"Query executed on DB: {sql_query}")
    return f"Results for: {sql_query}"

# Test
if __name__ == "__main__":
    print(execute_query("SELECT * FROM users;"))   # Executes DB call
    print(execute_query("SELECT * FROM users;"))   # Cached result
    print(execute_query("SELECT * FROM products;")) # Executes DB call
