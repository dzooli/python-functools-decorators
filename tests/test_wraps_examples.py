#!/usr/bin/env python3
"""Unit tests for wraps_examples.py"""
import unittest
from unittest.mock import patch
from io import StringIO
import time

from wraps_examples import (
    bad_decorator, good_decorator, bad_example, good_example,
    original_function, retry_decorator, debug_decorator
)


class TestBadDecorator(unittest.TestCase):
    """Test cases for bad_decorator (without @wraps)"""

    def test_bad_decorator_loses_function_name(self):
        """Test that bad_decorator loses original function name"""
        @bad_decorator
        def test_function():
            """Original docstring"""
            pass
        
        # Without @wraps, the function name is lost
        self.assertEqual(test_function.__name__, 'wrapper')

    def test_bad_decorator_loses_docstring(self):
        """Test that bad_decorator loses original docstring"""
        @bad_decorator
        def test_function():
            """Original docstring"""
            pass
        
        # Without @wraps, the docstring is lost
        self.assertNotEqual(test_function.__doc__, "Original docstring")
        self.assertEqual(test_function.__doc__, "This is the wrapper's docstring")

    def test_bad_decorator_functionality(self):
        """Test that bad_decorator still works functionally"""
        @bad_decorator
        def test_function():
            return "test_value"
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = test_function()
            self.assertEqual(result, "test_value")
            output = fake_out.getvalue()
            self.assertIn("Before function call", output)
            self.assertIn("After function call", output)


class TestGoodDecorator(unittest.TestCase):
    """Test cases for good_decorator (with @wraps)"""

    def test_good_decorator_preserves_function_name(self):
        """Test that good_decorator preserves original function name"""
        @good_decorator
        def test_function():
            """Original docstring"""
            pass
        
        self.assertEqual(test_function.__name__, 'test_function')

    def test_good_decorator_preserves_docstring(self):
        """Test that good_decorator preserves original docstring"""
        @good_decorator
        def test_function():
            """Original docstring"""
            pass
        
        self.assertEqual(test_function.__doc__, "Original docstring")

    def test_good_decorator_functionality(self):
        """Test that good_decorator works functionally"""
        @good_decorator
        def test_function():
            return "test_value"
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = test_function()
            self.assertEqual(result, "test_value")
            output = fake_out.getvalue()
            self.assertIn("Before function call", output)
            self.assertIn("After function call", output)


class TestBadExample(unittest.TestCase):
    """Test cases for bad_example function"""

    def test_bad_example_name(self):
        """Test bad_example has wrapper name"""
        self.assertEqual(bad_example.__name__, 'wrapper')

    def test_bad_example_docstring(self):
        """Test bad_example has wrapper docstring"""
        self.assertEqual(bad_example.__doc__, "This is the wrapper's docstring")

    def test_bad_example_return_value(self):
        """Test bad_example return value"""
        with patch('sys.stdout', new=StringIO()):
            result = bad_example()
            self.assertEqual(result, "Hello from bad_example!")


class TestGoodExample(unittest.TestCase):
    """Test cases for good_example function"""

    def test_good_example_name(self):
        """Test good_example preserves original name"""
        self.assertEqual(good_example.__name__, 'good_example')

    def test_good_example_docstring(self):
        """Test good_example preserves original docstring"""
        self.assertEqual(good_example.__doc__, 
                        "This function demonstrates the solution with @wraps")

    def test_good_example_return_value(self):
        """Test good_example return value"""
        with patch('sys.stdout', new=StringIO()):
            result = good_example()
            self.assertEqual(result, "Hello from good_example!")


class TestOriginalFunction(unittest.TestCase):
    """Test cases for original_function"""

    def test_original_function_name(self):
        """Test original_function name"""
        self.assertEqual(original_function.__name__, 'original_function')

    def test_original_function_docstring(self):
        """Test original_function docstring"""
        self.assertEqual(original_function.__doc__, 
                        "This is the original function's docstring")

    def test_original_function_return_value(self):
        """Test original_function return value"""
        result = original_function()
        self.assertEqual(result, "Hello from original!")


class TestRetryDecorator(unittest.TestCase):
    """Test cases for retry_decorator"""

    def test_retry_decorator_preserves_function_name(self):
        """Test that retry_decorator preserves function name"""
        @retry_decorator(max_attempts=2)
        def test_func():
            """Test docstring"""
            pass
        
        self.assertEqual(test_func.__name__, 'test_func')

    def test_retry_decorator_preserves_docstring(self):
        """Test that retry_decorator preserves docstring"""
        @retry_decorator(max_attempts=2)
        def test_func():
            """Test docstring"""
            pass
        
        self.assertEqual(test_func.__doc__, "Test docstring")

    def test_retry_decorator_success_on_first_attempt(self):
        """Test retry_decorator when function succeeds immediately"""
        @retry_decorator(max_attempts=3)
        def success_func():
            return "success"
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = success_func()
            self.assertEqual(result, "success")
            output = fake_out.getvalue()
            self.assertIn("Attempt 1 of 3", output)

    def test_retry_decorator_eventually_succeeds(self):
        """Test retry_decorator with eventual success"""
        call_count = [0]
        
        @retry_decorator(max_attempts=3, delay=0.01)
        def eventual_success():
            call_count[0] += 1
            if call_count[0] < 2:
                raise ValueError("Failing")
            return "success"
        
        with patch('sys.stdout', new=StringIO()):
            result = eventual_success()
            self.assertEqual(result, "success")
            self.assertEqual(call_count[0], 2)

    def test_retry_decorator_all_attempts_fail(self):
        """Test retry_decorator when all attempts fail"""
        @retry_decorator(max_attempts=2, delay=0.01)
        def always_fails():
            raise ValueError("Always fails")
        
        with patch('sys.stdout', new=StringIO()):
            with self.assertRaises(ValueError):
                always_fails()


class TestDebugDecorator(unittest.TestCase):
    """Test cases for debug_decorator"""

    def test_debug_decorator_preserves_function_name(self):
        """Test that debug_decorator preserves function name"""
        @debug_decorator
        def test_func():
            """Test docstring"""
            pass
        
        self.assertEqual(test_func.__name__, 'test_func')

    def test_debug_decorator_preserves_docstring(self):
        """Test that debug_decorator preserves docstring"""
        @debug_decorator
        def test_func():
            """Test docstring"""
            pass
        
        self.assertEqual(test_func.__doc__, "Test docstring")

    def test_debug_decorator_logs_function_call(self):
        """Test that debug_decorator logs function calls"""
        @debug_decorator
        def add(x, y):
            return x + y
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = add(3, 5)
            self.assertEqual(result, 8)
            output = fake_out.getvalue()
            self.assertIn("Calling add", output)
            self.assertIn("args=(3, 5)", output)
            self.assertIn("returned: 8", output)

    def test_debug_decorator_with_kwargs(self):
        """Test debug_decorator with keyword arguments"""
        @debug_decorator
        def func_with_kwargs(name, value=10):
            return f"{name}:{value}"
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = func_with_kwargs("test", value=20)
            self.assertEqual(result, "test:20")
            output = fake_out.getvalue()
            self.assertIn("Calling func_with_kwargs", output)
            self.assertIn("kwargs={'value': 20}", output)


if __name__ == '__main__':
    unittest.main()
