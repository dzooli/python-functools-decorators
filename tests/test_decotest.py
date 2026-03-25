#!/usr/bin/env python3
"""Unit tests for decotest.py"""
import unittest
from unittest.mock import patch
from io import StringIO

from decotest import param_decorator, my_function


class TestParamDecorator(unittest.TestCase):
    """Test cases for param_decorator"""

    def test_decorator_preserves_function_name(self):
        """Test that decorator preserves function name with @wraps"""
        @param_decorator("TestParam")
        def test_func():
            pass
        
        self.assertEqual(test_func.__name__, 'test_func')

    def test_decorator_with_custom_parameter(self):
        """Test decorator with custom parameter"""
        @param_decorator("CustomParam")
        def custom_function():
            print("Inside custom_function")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            custom_function()
            output = fake_out.getvalue()
            self.assertIn("Inside custom_function", output)
            self.assertIn("Func called. Decor param is: CustomParam", output)

    def test_decorator_with_different_parameters(self):
        """Test decorator with different parameter values"""
        @param_decorator("Param1")
        def func1():
            return "func1"
        
        @param_decorator("Param2")
        def func2():
            return "func2"
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            func1()
            output1 = fake_out.getvalue()
            self.assertIn("Param1", output1)
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            func2()
            output2 = fake_out.getvalue()
            self.assertIn("Param2", output2)

    def test_decorator_with_function_arguments(self):
        """Test decorator on function with arguments"""
        @param_decorator("TestArg")
        def func_with_args(x, y):
            print(f"x={x}, y={y}")
            return x + y
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            func_with_args(5, 3)
            output = fake_out.getvalue()
            self.assertIn("x=5, y=3", output)
            self.assertIn("Func called. Decor param is: TestArg", output)

    def test_decorator_with_kwargs(self):
        """Test decorator on function with keyword arguments"""
        @param_decorator("KwargsTest")
        def func_with_kwargs(name="default", value=0):
            print(f"name={name}, value={value}")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            func_with_kwargs(name="test", value=42)
            output = fake_out.getvalue()
            self.assertIn("name=test, value=42", output)
            self.assertIn("Func called. Decor param is: KwargsTest", output)


class TestMyFunction(unittest.TestCase):
    """Test cases for my_function"""

    def test_my_function_output(self):
        """Test my_function produces correct output"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            my_function()
            output = fake_out.getvalue()
            self.assertIn("Inside my_function", output)
            self.assertIn("Func called. Decor param is: TestParam", output)

    def test_my_function_name_preserved(self):
        """Test that my_function name is preserved"""
        self.assertEqual(my_function.__name__, 'my_function')


if __name__ == '__main__':
    unittest.main()
