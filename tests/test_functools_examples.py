#!/usr/bin/env python3
"""Unit tests for functools_examples.py"""
import unittest
from unittest.mock import patch
from io import StringIO
import time

from functools_examples import (
    fibonacci, multiply, log_message, process_data,
    DataProcessor, Student, rate_limit
)


class TestFibonacci(unittest.TestCase):
    """Test cases for fibonacci function with @lru_cache"""

    def test_fibonacci_base_cases(self):
        """Test fibonacci base cases"""
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)

    def test_fibonacci_recursive_cases(self):
        """Test fibonacci recursive calculations"""
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(3), 2)
        self.assertEqual(fibonacci(4), 3)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(10), 55)

    def test_fibonacci_larger_value(self):
        """Test fibonacci with larger value"""
        self.assertEqual(fibonacci(20), 6765)

    def test_fibonacci_cache_info(self):
        """Test that fibonacci uses cache"""
        # Clear cache
        fibonacci.cache_clear()
        
        # First call
        fibonacci(10)
        info = fibonacci.cache_info()
        self.assertGreater(info.hits + info.misses, 0)
        
        # Second call should have more cache hits
        fibonacci(10)
        info2 = fibonacci.cache_info()
        self.assertGreater(info2.hits, info.hits)


class TestMultiplyAndPartial(unittest.TestCase):
    """Test cases for multiply function and partial usage"""

    def test_multiply_basic(self):
        """Test basic multiply function"""
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(4, 5), 20)

    def test_multiply_with_z_parameter(self):
        """Test multiply with z parameter"""
        self.assertEqual(multiply(2, 3, z=2), 12)
        self.assertEqual(multiply(1, 5, z=10), 50)

    def test_multiply_default_z(self):
        """Test multiply uses default z=1"""
        self.assertEqual(multiply(3, 4), 12)


class TestLogMessage(unittest.TestCase):
    """Test cases for log_message function"""

    def test_log_message_basic(self):
        """Test basic log_message functionality"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            log_message("INFO", "Test message")
            output = fake_out.getvalue()
            self.assertIn("INFO", output)
            self.assertIn("Test message", output)

    def test_log_message_with_timestamp(self):
        """Test log_message with custom timestamp"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            log_message("ERROR", "Error occurred", timestamp="12:34:56")
            output = fake_out.getvalue()
            self.assertIn("[12:34:56]", output)
            self.assertIn("ERROR", output)
            self.assertIn("Error occurred", output)

    def test_log_message_different_levels(self):
        """Test log_message with different log levels"""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        for level in levels:
            with patch('sys.stdout', new=StringIO()) as fake_out:
                log_message(level, "Test")
                output = fake_out.getvalue()
                self.assertIn(level, output)


class TestProcessData(unittest.TestCase):
    """Test cases for process_data with @singledispatch"""

    def test_process_data_string(self):
        """Test process_data with string input"""
        result = process_data("hello")
        self.assertIn("Processing string", result)
        self.assertIn("hello", result)
        self.assertIn("length: 5", result)

    def test_process_data_list(self):
        """Test process_data with list input"""
        result = process_data([1, 2, 3])
        self.assertIn("Processing list", result)
        self.assertIn("3 items", result)

    def test_process_data_dict(self):
        """Test process_data with dict input"""
        result = process_data({"a": 1, "b": 2})
        self.assertIn("Processing dict", result)
        self.assertIn("['a', 'b']", result)

    def test_process_data_unknown_type(self):
        """Test process_data with unknown type (uses default)"""
        result = process_data(42)
        self.assertIn("Processing unknown type", result)
        self.assertIn("int", result)

    def test_process_data_empty_list(self):
        """Test process_data with empty list"""
        result = process_data([])
        self.assertIn("0 items", result)

    def test_process_data_empty_dict(self):
        """Test process_data with empty dict"""
        result = process_data({})
        self.assertIn("Processing dict", result)


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class with @cached_property"""

    def test_dataprocessor_initialization(self):
        """Test DataProcessor initialization"""
        processor = DataProcessor([1, 2, 3])
        self.assertEqual(processor.data, [1, 2, 3])

    def test_expensive_calculation(self):
        """Test expensive_calculation cached property"""
        processor = DataProcessor([1, 2, 3, 4, 5])
        result = processor.expensive_calculation
        # Sum of squares: 1 + 4 + 9 + 16 + 25 = 55
        self.assertEqual(result, 55)

    def test_expensive_calculation_is_cached(self):
        """Test that expensive_calculation is only computed once"""
        processor = DataProcessor([1, 2, 3])
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result1 = processor.expensive_calculation
            output1 = fake_out.getvalue()
            self.assertIn("Computing expensive calculation", output1)
        
        # Second access should use cache
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result2 = processor.expensive_calculation
            output2 = fake_out.getvalue()
            self.assertNotIn("Computing expensive calculation", output2)
        
        self.assertEqual(result1, result2)

    def test_regular_property(self):
        """Test regular_property is computed each time"""
        processor = DataProcessor([1, 2, 3, 4])
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result1 = processor.regular_property
            output1 = fake_out.getvalue()
            self.assertIn("Computing regular property", output1)
            self.assertEqual(result1, 4)
        
        # Second access should compute again
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result2 = processor.regular_property
            output2 = fake_out.getvalue()
            self.assertIn("Computing regular property", output2)
            self.assertEqual(result2, 4)


class TestStudent(unittest.TestCase):
    """Test cases for Student class with @total_ordering"""

    def test_student_initialization(self):
        """Test Student initialization"""
        student = Student("Alice", 85)
        self.assertEqual(student.name, "Alice")
        self.assertEqual(student.grade, 85)

    def test_student_equality(self):
        """Test Student equality comparison"""
        alice = Student("Alice", 85)
        bob = Student("Bob", 85)
        charlie = Student("Charlie", 90)
        
        self.assertEqual(alice, bob)
        self.assertNotEqual(alice, charlie)

    def test_student_less_than(self):
        """Test Student less than comparison"""
        alice = Student("Alice", 85)
        bob = Student("Bob", 92)
        
        self.assertTrue(alice < bob)
        self.assertFalse(bob < alice)

    def test_student_greater_than(self):
        """Test Student greater than comparison (auto-generated)"""
        alice = Student("Alice", 85)
        bob = Student("Bob", 92)
        
        self.assertTrue(bob > alice)
        self.assertFalse(alice > bob)

    def test_student_less_than_or_equal(self):
        """Test Student less than or equal comparison (auto-generated)"""
        alice = Student("Alice", 85)
        bob = Student("Bob", 92)
        charlie = Student("Charlie", 85)
        
        self.assertTrue(alice <= bob)
        self.assertTrue(alice <= charlie)
        self.assertFalse(bob <= alice)

    def test_student_greater_than_or_equal(self):
        """Test Student greater than or equal comparison (auto-generated)"""
        alice = Student("Alice", 85)
        bob = Student("Bob", 92)
        charlie = Student("Charlie", 85)
        
        self.assertTrue(bob >= alice)
        self.assertTrue(alice >= charlie)
        self.assertFalse(alice >= bob)

    def test_student_sorting(self):
        """Test sorting list of Students"""
        alice = Student("Alice", 85)
        bob = Student("Bob", 92)
        charlie = Student("Charlie", 78)
        
        students = [bob, alice, charlie]
        sorted_students = sorted(students)
        
        self.assertEqual(sorted_students[0].grade, 78)
        self.assertEqual(sorted_students[1].grade, 85)
        self.assertEqual(sorted_students[2].grade, 92)

    def test_student_repr(self):
        """Test Student string representation"""
        alice = Student("Alice", 85)
        self.assertEqual(repr(alice), "Student('Alice', 85)")


class TestRateLimitDecorator(unittest.TestCase):
    """Test cases for rate_limit decorator"""

    def test_rate_limit_preserves_function_name(self):
        """Test that rate_limit preserves function name"""
        @rate_limit(calls_per_second=10)
        def test_func():
            """Test docstring"""
            pass
        
        self.assertEqual(test_func.__name__, 'test_func')

    def test_rate_limit_allows_single_call(self):
        """Test rate_limit allows single call immediately"""
        @rate_limit(calls_per_second=10)
        def test_func():
            return "success"
        
        with patch('sys.stdout', new=StringIO()):
            start = time.time()
            result = test_func()
            elapsed = time.time() - start
            
            self.assertEqual(result, "success")
            # Should not delay first call significantly
            self.assertLess(elapsed, 0.2)

    def test_rate_limit_return_value(self):
        """Test that rate_limit preserves return value"""
        @rate_limit(calls_per_second=10)
        def return_func(value):
            return value * 2
        
        with patch('sys.stdout', new=StringIO()):
            result = return_func(5)
            self.assertEqual(result, 10)

    def test_rate_limit_with_arguments(self):
        """Test rate_limit on function with arguments"""
        @rate_limit(calls_per_second=10)
        def add_func(x, y):
            return x + y
        
        with patch('sys.stdout', new=StringIO()):
            result = add_func(3, 4)
            self.assertEqual(result, 7)


if __name__ == '__main__':
    unittest.main()
