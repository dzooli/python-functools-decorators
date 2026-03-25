# Unit Tests for Python Decorator Examples

This directory contains comprehensive unit tests for all Python files in the project.

## Test Files

### test_decotest.py
Tests for `decotest.py`:
- `TestParamDecorator`: Tests the parametrized decorator functionality
- `TestMyFunction`: Tests the decorated `my_function`
- Coverage: decorator metadata preservation, custom parameters, function arguments, kwargs

### test_main.py
Tests for `main.py`:
- `TestHelloerDecorator`: Tests the `helloer` parametrized decorator
- `TestSimpleHelloerDecorator`: Tests the simple decorator without parameters
- `TestAdvancedHelloerDecorator`: Tests the advanced decorator with multiple parameters
- `TestMainFunction`, `TestSimpleMainFunction`, `TestAdvancedFunction`: Tests decorated functions
- Coverage: output validation, return values, argument passing, emoji handling, repeat functionality

### test_wraps_examples.py
Tests for `wraps_examples.py`:
- `TestBadDecorator`: Tests decorator without @wraps (demonstrates metadata loss)
- `TestGoodDecorator`: Tests decorator with @wraps (demonstrates metadata preservation)
- `TestRetryDecorator`: Tests the retry functionality decorator
- `TestDebugDecorator`: Tests the debug logging decorator
- Coverage: function name/docstring preservation, retry logic, debug output, exception handling

### test_functools_examples.py
Tests for `functools_examples.py`:
- `TestFibonacci`: Tests @lru_cache functionality and caching behavior
- `TestMultiplyAndPartial`: Tests partial function application
- `TestLogMessage`: Tests log message formatting
- `TestProcessData`: Tests @singledispatch for type-based function overloading
- `TestDataProcessor`: Tests @cached_property functionality
- `TestStudent`: Tests @total_ordering for automatic comparison methods
- `TestRateLimitDecorator`: Tests the rate limiting decorator
- Coverage: caching, partial application, single dispatch, cached properties, comparison operations

## Running Tests

### Run all tests
```bash
python -m unittest discover tests -v
```

### Run specific test file
```bash
python -m unittest tests.test_decotest -v
python -m unittest tests.test_main -v
python -m unittest tests.test_wraps_examples -v
python -m unittest tests.test_functools_examples -v
```

### Run specific test class
```bash
python -m unittest tests.test_decotest.TestParamDecorator -v
```

### Run specific test method
```bash
python -m unittest tests.test_decotest.TestParamDecorator.test_decorator_preserves_function_name -v
```

### With pytest (if installed)
```bash
pytest tests/ -v
pytest tests/test_decotest.py -v
```

## Test Statistics

- **Total Tests**: 82
- **Test Files**: 4
- **Test Classes**: 21
- **Coverage Areas**:
  - Decorator functionality and behavior
  - Metadata preservation with @wraps
  - Parametrized decorators
  - functools utilities (lru_cache, partial, singledispatch, cached_property, total_ordering)
  - Edge cases and error handling
  - Return value preservation
  - Argument passing (args and kwargs)

## Test Design Principles

1. **Isolation**: Each test is independent and can run in any order
2. **Mocking**: Uses `unittest.mock.patch` to capture stdout for output verification
3. **Comprehensive**: Tests both happy paths and edge cases
4. **Descriptive**: Test names clearly describe what is being tested
5. **Documentation**: Each test has a docstring explaining its purpose

## Key Testing Patterns Used

### Output Capture
```python
with patch('sys.stdout', new=StringIO()) as fake_out:
    my_function()
    output = fake_out.getvalue()
    self.assertIn("expected text", output)
```

### Metadata Verification
```python
self.assertEqual(decorated_func.__name__, 'original_name')
self.assertEqual(decorated_func.__doc__, 'original docstring')
```

### Exception Testing
```python
with self.assertRaises(ValueError):
    function_that_should_raise()
```

### Cache Testing
```python
fibonacci.cache_clear()
result = fibonacci(10)
info = fibonacci.cache_info()
self.assertGreater(info.hits, 0)
```

## Dependencies

- Python 3.x standard library
- unittest (built-in)
- unittest.mock (built-in)
- io.StringIO (built-in)

No external dependencies required!
