from functools import wraps


def helloer(prefix: str):
    def decorator(func):
        @wraps(func)  # Preserves original function metadata
        def wrapper(*fnargs, **fnkwargs):
            print("Hello, World!", f"Welcome by {prefix}", end="\n\n")
            result = func(*fnargs, **fnkwargs)
            print("\nGoodbye, World!")
            return result

        return wrapper

    return decorator


def simple_helloer(func):
    @wraps(func)  # Always use @wraps!
    def wrapper(*args, **kwargs):
        print("Hello, World!")
        result = func(*args, **kwargs)
        print("Goodbye, World!")
        return result

    return wrapper


@helloer("Helloer Decorator")
def main(name: str = "User"):
    print(f"Hello from main, {name}!")


@simple_helloer
def simple_main(name: str = "Simple User"):
    print(f"Hello from simple_main, {name}!")


# Example showing multiple parameters captured by closure
def advanced_helloer(prefix: str, repeat: int = 1, emoji: str = "🎉"):
    def decorator(func):
        @wraps(func)  # Don't forget @wraps in parametrized decorators!
        def wrapper(*fnargs, **fnkwargs):
            for i in range(repeat):
                print(f"{emoji} Hello! {prefix} (call #{i+1}) {emoji}")

            result = func(*fnargs, **fnkwargs)

            print(f"Goodbye from {prefix}! {emoji}")
            return result

        return wrapper

    return decorator


@advanced_helloer("Advanced Decorator", repeat=2, emoji="🚀")
def advanced_function(name: str):
    print(f"Advanced function called with: {name}")


if __name__ == "__main__":
    print("Using @ syntax:")
    main()

    print("\nUsing simple decorator:")
    simple_main()

    print("\nUsing advanced decorator with multiple parameters:")
    advanced_function("Test User")
