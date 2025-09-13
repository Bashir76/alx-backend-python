import functools
import time
import random  # only used in example

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a function if it raises an exception.
    Retries up to `retries` times with a `delay` (in seconds) between attempts.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"[Retry {attempt}/{retries}] Error: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            # if all retries fail, raise the last exception
            raise last_exception
        return wrapper
    return decorator


# Example usage
@retry_on_failure(retries=3, delay=1)
def unstable_query():
    """
    Example function that randomly fails to simulate transient DB errors.
    Replace with real DB operation in production.
    """
    if random.choice([True, False]):  # randomly succeed or fail
        raise Exception("Transient DB error")
    return "Query succeeded!"


if __name__ == "__main__":
    try:
        print(unstable_query())
    except Exception as e:
        print(f"Final failure after retries: {e}")
