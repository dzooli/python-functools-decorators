#!/usr/bin/env python3
"""
Demonstrating when and why to use @wraps decorator
"""
from functools import wraps


# Example 1: Problem without @wraps
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        """This is the wrapper's docstring"""
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result

    return wrapper


def good_decorator(func):
    @wraps(func)  # This preserves the original function's metadata!
    def wrapper(*args, **kwargs):
        """This is the wrapper's docstring"""
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result

    return wrapper


# Test functions
@bad_decorator
def bad_example():
    """This function demonstrates the problem without @wraps"""
    return "Hello from bad_example!"


@good_decorator
def good_example():
    """This function demonstrates the solution with @wraps"""
    return "Hello from good_example!"


def original_function():
    """This is the original function's docstring"""
    return "Hello from original!"


print("=== Without @wraps (BAD) ===")
print(f"Function name: {bad_example.__name__}")
print(f"Function docstring: {bad_example.__doc__}")
print(f"Function module: {bad_example.__module__}")

print("\n=== With @wraps (GOOD) ===")
print(f"Function name: {good_example.__name__}")
print(f"Function docstring: {good_example.__doc__}")
print(f"Function module: {good_example.__module__}")

print("\n=== Original (for comparison) ===")
print(f"Function name: {original_function.__name__}")
print(f"Function docstring: {original_function.__doc__}")
print(f"Function module: {original_function.__module__}")


# Example 2: Parametrized decorator with @wraps
def retry_decorator(max_attempts=3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)  # Always use @wraps in your decorators!
        def wrapper(*args, **kwargs):
            import time

            for attempt in range(max_attempts):
                try:
                    print(f"Attempt {attempt + 1} of {max_attempts}")
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    if attempt == max_attempts - 1:  # Last attempt
                        print(f"All {max_attempts} attempts failed!")
                        raise e
                    else:
                        print(f"Attempt {attempt + 1} failed: {e}")
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)

        return wrapper

    return decorator


@retry_decorator(max_attempts=2, delay=0.5)
def unreliable_function(should_fail=True):
    """A function that might fail"""
    if should_fail:
        raise ValueError("Something went wrong!")
    return "Success!"


print("\n=== Parametrized Decorator with @wraps ===")
print(f"Function name: {unreliable_function.__name__}")
print(f"Function docstring: {unreliable_function.__doc__}")


# Example 3: When @wraps is CRITICAL
def debug_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result

    return wrapper


@debug_decorator
def calculate_area(length, width):
    """Calculate the area of a rectangle"""
    return length * width


# Without @wraps, this would print "wrapper" instead of "calculate_area"
print("\n=== Debug Example ===")
print(f"About to call: {calculate_area.__name__}")
result = calculate_area(5, 3)


# Example 4: Real-world use cases
print("\n=== When to Use @wraps ===")
print("1. Writing any decorator (simple or parametrized)")
print("2. When debugging - preserves original function names")
print("3. When using introspection tools")
print("4. When writing libraries that others will use")
print("5. When generating documentation")
print("6. When using tools that rely on function metadata")


if __name__ == "__main__":
    print("\n=== Summary ===")
    print("Always use @wraps(func) in your decorator's wrapper function!")
    print("It preserves the original function's important metadata.")
