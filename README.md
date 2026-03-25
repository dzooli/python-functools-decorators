# 🎨 Decor - Python Decorators & Functools Examples

A comprehensive collection of Python decorator patterns and `functools` utilities with practical examples and 99% test coverage.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-82%20passed-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen.svg)](htmlcov/index.html)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [Usage Examples](#-usage-examples)
- [Testing](#-testing)
- [Code Examples](#-code-examples)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Decorator Patterns
- ✅ Simple decorators with `@wraps`
- ✅ Parametrized decorators with closures
- ✅ Multiple decorator composition
- ✅ Decorators with custom parameters (prefix, repeat, emoji)

### Functools Utilities
- 🚀 **@lru_cache** - Memoization for performance optimization
- 🔧 **partial** - Pre-fill function arguments
- 🎯 **@singledispatch** - Type-based function overloading
- 💰 **reduce** - Cumulative operations
- 💾 **@cached_property** - Cache expensive property calculations
- ⚖️ **@total_ordering** - Auto-generate comparison methods
- ⏱️ **Rate limiting** - Custom decorator implementation

### Advanced Examples
- 🔄 Retry decorator with configurable attempts
- 🐛 Debug decorator with function call logging
- 📊 Metadata preservation demonstrations
- 🎭 Real-world practical patterns

---

## 🚀 Installation

### Prerequisites
- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Using uv (Recommended)

```powershell
# Clone the repository
git clone https://github.com/dzooli/python-functools-decorators.git
cd decor

# Sync dependencies (creates .venv automatically)
uv sync --extra dev
```

### Using pip

```powershell
# Clone the repository
git clone https://github.com/dzooli/python-functools-decorators.git
cd decor

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac

# Install dependencies
pip install -e .[dev]
```

---

## 📁 Project Structure

```
decor/
├── decotest.py              # Parametrized decorator examples
├── main.py                  # Simple, advanced decorator patterns
├── wraps_examples.py        # @wraps importance demonstrations
├── functools_examples.py    # Comprehensive functools utilities
├── tests/
│   ├── test_decotest.py            # Tests for parametrized decorators
│   ├── test_main.py                # Tests for main decorator examples
│   ├── test_wraps_examples.py      # Tests for @wraps demonstrations
│   └── test_functools_examples.py  # Tests for functools utilities
├── view-coverage.ps1        # Script to run tests and view coverage
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

---

## 💡 Usage Examples

### Run Individual Files

```powershell
# Simple decorator examples
uv run python main.py

# Functools utilities showcase
uv run python functools_examples.py

# @wraps importance demonstration
uv run python wraps_examples.py

# Parametrized decorator example
uv run python decotest.py
```

### Interactive Exploration

```powershell
# Start Python REPL with project modules
uv run python

>>> from main import helloer, simple_helloer
>>> from functools_examples import fibonacci, process_data
>>> 
>>> # Try the decorators
>>> @helloer("MyDecorator")
... def greet(name):
...     print(f"Hello, {name}!")
... 
>>> greet("World")
```

---

## 🧪 Testing

### Run All Tests

```powershell
# Using uv (recommended)
uv run pytest

# Or activate venv first
.venv\Scripts\Activate.ps1
pytest
```

### Run Tests with Coverage Report

```powershell
# Run tests and open HTML coverage report
.\view-coverage.ps1

# Or manually
uv run pytest
Start-Process htmlcov\index.html
```

### Run Specific Test Files

```powershell
uv run pytest tests/test_main.py -v
uv run pytest tests/test_functools_examples.py -v
```

### Test Statistics

- **Total Tests**: 82
- **Coverage**: 99% (252/255 statements)
- **Test Files**: 4
- **Test Classes**: 21

| File | Statements | Coverage |
|------|------------|----------|
| `decotest.py` | 12 | 100% |
| `functools_examples.py` | 120 | 100% |
| `main.py` | 39 | 100% |
| `wraps_examples.py` | 84 | 96% |

---

## 📚 Code Examples

### Simple Decorator with @wraps

```python
from functools import wraps

def simple_decorator(func):
    @wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@simple_decorator
def greet(name):
    """Greet someone by name"""
    return f"Hello, {name}!"

print(greet("World"))
# Output:
# Before function call
# Hello, World!
# After function call
```

### Parametrized Decorator

```python
from functools import wraps

def repeat(times=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                print(f"Call #{i+1}")
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def say_hello():
    print("Hello!")

say_hello()
```

### Functools - @lru_cache for Memoization

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# First call computes
print(fibonacci(30))  # Fast!

# Second call uses cache
print(fibonacci(30))  # Instant!
```

### Functools - @singledispatch for Type Overloading

```python
from functools import singledispatch

@singledispatch
def process_data(data):
    return f"Unknown type: {type(data).__name__}"

@process_data.register(str)
def _(data: str):
    return f"Processing string: '{data}' (length: {len(data)})"

@process_data.register(list)
def _(data: list):
    return f"Processing list with {len(data)} items"

print(process_data("hello"))        # Processing string
print(process_data([1, 2, 3]))      # Processing list
print(process_data(42))             # Unknown type
```

---

## 🎯 Key Learnings

### Why Use @wraps?

**Without @wraps** ❌
```python
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_func():
    """My docstring"""
    pass

print(my_func.__name__)  # 'wrapper' (WRONG!)
print(my_func.__doc__)   # None (LOST!)
```

**With @wraps** ✅
```python
from functools import wraps

def good_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def my_func():
    """My docstring"""
    pass

print(my_func.__name__)  # 'my_func' (Correct!)
print(my_func.__doc__)   # 'My docstring' (Preserved!)
```

---

## 🛠️ Development

### Code Formatting

```powershell
# Format code with Black
uv run black .

# Check formatting
uv run black --check .
```

### Configuration

- **Python Version**: 3.13+
- **Formatter**: Black (line length: 120)
- **Testing**: pytest with pytest-cov
- **Coverage Target**: 95%+

---

## 📖 Learning Resources

- [PEP 318 - Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- [functools - Python Documentation](https://docs.python.org/3/library/functools.html)
- [Real Python - Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```powershell
   git checkout -b feature/amazing-decorator
   ```
3. **Make your changes and add tests**
4. **Ensure tests pass**
   ```powershell
   uv run pytest
   ```
5. **Format your code**
   ```powershell
   uv run black .
   ```
6. **Commit and push**
   ```powershell
   git commit -m "Add amazing decorator pattern"
   git push origin feature/amazing-decorator
   ```
7. **Open a Pull Request**

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**dzooli**

- GitHub: [@dzooli](https://github.com/dzooli)
- Project Link: [https://github.com/dzooli/python-functools-decorators](https://github.com/dzooli/python-functools-decorators)

---

## 🌟 Show Your Support

Give a ⭐️ if this project helped you understand Python decorators better!

---

**Happy Decorating! 🎨✨**
