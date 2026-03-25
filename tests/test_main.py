#!/usr/bin/env python3
"""Unit tests for main.py"""
import unittest
from unittest.mock import patch
from io import StringIO

from main import helloer, simple_helloer, advanced_helloer, main, simple_main, advanced_function


class TestHelloerDecorator(unittest.TestCase):
    """Test cases for helloer decorator"""

    def test_helloer_preserves_function_name(self):
        """Test that helloer preserves function name"""
        @helloer("Test")
        def test_func():
            pass
        
        self.assertEqual(test_func.__name__, 'test_func')

    def test_helloer_with_prefix(self):
        """Test helloer decorator with custom prefix"""
        @helloer("CustomPrefix")
        def custom_func():
            print("Function body")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            custom_func()
            output = fake_out.getvalue()
            self.assertIn("Hello, World!", output)
            self.assertIn("Welcome by CustomPrefix", output)
            self.assertIn("Function body", output)
            self.assertIn("Goodbye, World!", output)

    def test_helloer_return_value(self):
        """Test that helloer preserves return value"""
        @helloer("Test")
        def return_func():
            return "test_value"
        
        with patch('sys.stdout', new=StringIO()):
            result = return_func()
            self.assertEqual(result, "test_value")

    def test_helloer_with_arguments(self):
        """Test helloer on function with arguments"""
        @helloer("ArgTest")
        def func_with_args(x, y):
            print(f"Sum: {x + y}")
            return x + y
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = func_with_args(3, 4)
            self.assertEqual(result, 7)
            output = fake_out.getvalue()
            self.assertIn("Sum: 7", output)


class TestSimpleHelloerDecorator(unittest.TestCase):
    """Test cases for simple_helloer decorator"""

    def test_simple_helloer_preserves_function_name(self):
        """Test that simple_helloer preserves function name"""
        @simple_helloer
        def test_func():
            pass
        
        self.assertEqual(test_func.__name__, 'test_func')

    def test_simple_helloer_output(self):
        """Test simple_helloer decorator output"""
        @simple_helloer
        def simple_func():
            print("Inside function")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            simple_func()
            output = fake_out.getvalue()
            self.assertIn("Hello, World!", output)
            self.assertIn("Inside function", output)
            self.assertIn("Goodbye, World!", output)

    def test_simple_helloer_return_value(self):
        """Test that simple_helloer preserves return value"""
        @simple_helloer
        def return_func():
            return 42
        
        with patch('sys.stdout', new=StringIO()):
            result = return_func()
            self.assertEqual(result, 42)


class TestAdvancedHelloerDecorator(unittest.TestCase):
    """Test cases for advanced_helloer decorator"""

    def test_advanced_helloer_preserves_function_name(self):
        """Test that advanced_helloer preserves function name"""
        @advanced_helloer("Test")
        def test_func():
            pass
        
        self.assertEqual(test_func.__name__, 'test_func')

    def test_advanced_helloer_with_repeat(self):
        """Test advanced_helloer with repeat parameter"""
        @advanced_helloer("TestPrefix", repeat=3)
        def test_func():
            print("Function body")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            test_func()
            output = fake_out.getvalue()
            # Should have 3 hello messages
            self.assertEqual(output.count("call #1"), 1)
            self.assertEqual(output.count("call #2"), 1)
            self.assertEqual(output.count("call #3"), 1)
            self.assertIn("Function body", output)

    def test_advanced_helloer_with_emoji(self):
        """Test advanced_helloer with custom emoji"""
        @advanced_helloer("EmojiTest", repeat=1, emoji="✨")
        def test_func():
            print("Function body")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            test_func()
            output = fake_out.getvalue()
            self.assertIn("✨", output)
            self.assertIn("EmojiTest", output)

    def test_advanced_helloer_return_value(self):
        """Test that advanced_helloer preserves return value"""
        @advanced_helloer("Test", repeat=2)
        def return_func():
            return "return_value"
        
        with patch('sys.stdout', new=StringIO()):
            result = return_func()
            self.assertEqual(result, "return_value")


class TestMainFunction(unittest.TestCase):
    """Test cases for main function"""

    def test_main_default_name(self):
        """Test main function with default name"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
            self.assertIn("Hello from main, User!", output)
            self.assertIn("Welcome by Helloer Decorator", output)

    def test_main_custom_name(self):
        """Test main function with custom name"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main("Alice")
            output = fake_out.getvalue()
            self.assertIn("Hello from main, Alice!", output)

    def test_main_function_name_preserved(self):
        """Test that main function name is preserved"""
        self.assertEqual(main.__name__, 'main')


class TestSimpleMainFunction(unittest.TestCase):
    """Test cases for simple_main function"""

    def test_simple_main_default_name(self):
        """Test simple_main function with default name"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            simple_main()
            output = fake_out.getvalue()
            self.assertIn("Hello from simple_main, Simple User!", output)

    def test_simple_main_custom_name(self):
        """Test simple_main function with custom name"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            simple_main("Bob")
            output = fake_out.getvalue()
            self.assertIn("Hello from simple_main, Bob!", output)

    def test_simple_main_function_name_preserved(self):
        """Test that simple_main function name is preserved"""
        self.assertEqual(simple_main.__name__, 'simple_main')


class TestAdvancedFunction(unittest.TestCase):
    """Test cases for advanced_function"""

    def test_advanced_function_output(self):
        """Test advanced_function output"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            advanced_function("TestUser")
            output = fake_out.getvalue()
            self.assertIn("Advanced function called with: TestUser", output)
            self.assertIn("Advanced Decorator", output)
            self.assertIn("🚀", output)
            # Should have 2 hello calls
            self.assertEqual(output.count("call #1"), 1)
            self.assertEqual(output.count("call #2"), 1)

    def test_advanced_function_name_preserved(self):
        """Test that advanced_function name is preserved"""
        self.assertEqual(advanced_function.__name__, 'advanced_function')


if __name__ == '__main__':
    unittest.main()
