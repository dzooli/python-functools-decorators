from functools import wraps


def param_decorator(param):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            print(f"Func called. Decor param is: {param}")

        return wrapper

    return decorator


@param_decorator("TestParam")
def my_function():
    print("Inside my_function")


if __name__ == "__main__":
    my_function()
    # end def
