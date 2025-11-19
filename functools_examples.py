#!/usr/bin/env python3
"""
Practical functools utilities beyond @wraps
"""
from functools import (
    wraps,
    partial,
    lru_cache,
    singledispatch,
    reduce,
    cached_property,
    total_ordering,
)
import time


# 1. @lru_cache - Memoization (caching function results)
print("=== 1. @lru_cache - Memoization ===")


@lru_cache(maxsize=128)  # Cache up to 128 results
def fibonacci(n):
    """Fibonacci with caching - much faster for repeated calls"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Without cache, fib(30) would be very slow
start = time.time()
result = fibonacci(30)
print(f"fibonacci(30) = {result} (took {time.time() - start:.4f}s)")

# Second call is instant due to cache
start = time.time()
result = fibonacci(30)
print(f"fibonacci(30) again = {result} (took {time.time() - start:.4f}s)")

# Check cache info
print(f"Cache info: {fibonacci.cache_info()}")


# 2. partial - Create functions with some arguments pre-filled
print("\n=== 2. partial - Pre-fill function arguments ===")


def multiply(x, y, z=1):
    return x * y * z


# Create specialized versions
double = partial(multiply, 2)  # x is always 2
triple_with_bonus = partial(multiply, 3, z=10)

print(f"double(5) = {double(5)}")  # multiply(2, 5)
print(f"triple_with_bonus(4) = {triple_with_bonus(4)}")  # multiply(3, 4, z=10)


# Great for callbacks and event handlers
def log_message(level, message, timestamp=None):
    ts = timestamp or time.strftime("%H:%M:%S")
    print(f"[{ts}] {level}: {message}")


# Create specialized loggers
info = partial(log_message, "INFO")
error = partial(log_message, "ERROR")

info("Application started")
error("Something went wrong!")


# 3. @singledispatch - Function overloading based on type
print("\n=== 3. @singledispatch - Type-based function overloading ===")


@singledispatch
def process_data(data):
    """Default implementation"""
    return f"Processing unknown type: {type(data).__name__}"


@process_data.register(str)
def _(data: str):
    return f"Processing string: '{data}' (length: {len(data)})"


@process_data.register(list)
def _(data: list):
    return f"Processing list with {len(data)} items: {data}"


@process_data.register(dict)
def _(data: dict):
    return f"Processing dict with keys: {list(data.keys())}"


# Same function name, different behavior based on type
print(process_data("hello"))
print(process_data([1, 2, 3]))
print(process_data({"a": 1, "b": 2}))
print(process_data(42))  # Uses default implementation


# 4. reduce - Apply function cumulatively to items
print("\n=== 4. reduce - Cumulative operations ===")

numbers = [1, 2, 3, 4, 5]

# Sum all numbers
total = reduce(lambda x, y: x + y, numbers)
print(f"Sum: {total}")

# Find maximum
maximum = reduce(lambda x, y: x if x > y else y, numbers)
print(f"Max: {maximum}")

# Flatten nested lists
nested = [[1, 2], [3, 4], [5, 6]]
flattened = reduce(lambda x, y: x + y, nested)
print(f"Flattened: {flattened}")


# 5. @cached_property - Property that's computed once and cached
print("\n=== 5. @cached_property - Expensive property caching ===")


class DataProcessor:
    def __init__(self, data):
        self.data = data

    @cached_property
    def expensive_calculation(self):
        """This will only be computed once"""
        print("Computing expensive calculation...")
        time.sleep(0.1)  # Simulate expensive operation
        return sum(x * x for x in self.data)

    @property
    def regular_property(self):
        """This is computed every time"""
        print("Computing regular property...")
        return len(self.data)


processor = DataProcessor([1, 2, 3, 4, 5])

print("First access to cached_property:")
print(f"Result: {processor.expensive_calculation}")

print("Second access to cached_property (cached):")
print(f"Result: {processor.expensive_calculation}")

print("Regular property (computed each time):")
print(f"Result: {processor.regular_property}")
print(f"Result: {processor.regular_property}")


# 6. @total_ordering - Auto-generate comparison methods
print("\n=== 6. @total_ordering - Automatic comparison methods ===")


@total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __eq__(self, other):
        return self.grade == other.grade

    def __lt__(self, other):
        return self.grade < other.grade

    def __repr__(self):
        return f"Student('{self.name}', {self.grade})"


# Only defined __eq__ and __lt__, but get all comparison operators for free!
alice = Student("Alice", 85)
bob = Student("Bob", 92)
charlie = Student("Charlie", 85)

print(f"alice < bob: {alice < bob}")
print(f"alice <= charlie: {alice <= charlie}")
print(f"alice == charlie: {alice == charlie}")
print(f"bob > alice: {bob > alice}")
print(f"bob >= charlie: {bob >= charlie}")

students = [bob, alice, charlie]
print(f"Sorted students: {sorted(students)}")


# 7. Practical decorator using functools
print("\n=== 7. Practical example: Rate limiting decorator ===")


def rate_limit(calls_per_second=1):
    """Limit function calls per second"""

    def decorator(func):
        last_called = [0.0]  # Use list for mutable reference

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            time_since_last = now - last_called[0]
            min_interval = 1.0 / calls_per_second

            if time_since_last < min_interval:
                sleep_time = min_interval - time_since_last
                print(f"Rate limiting: sleeping for {sleep_time:.2f}s")
                time.sleep(sleep_time)

            last_called[0] = time.time()
            return func(*args, **kwargs)

        return wrapper

    return decorator


@rate_limit(calls_per_second=2)  # Max 2 calls per second
def api_call(endpoint):
    """Simulate an API call"""
    return f"Called {endpoint} at {time.strftime('%H:%M:%S')}"


print("Making rapid API calls (rate limited):")
for i in range(3):
    result = api_call(f"/endpoint{i}")
    print(result)


if __name__ == "__main__":
    print("\n=== Summary: Most Useful functools Tools ===")
    print("1. @wraps - Always use in decorators")
    print("2. @lru_cache - Cache expensive function results")
    print("3. partial - Create specialized function versions")
    print("4. @singledispatch - Type-based function overloading")
    print("5. reduce - Cumulative operations on iterables")
    print("6. @cached_property - Cache expensive property calculations")
    print("7. @total_ordering - Auto-generate comparison methods")
