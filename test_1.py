#!/usr/bin/env python3
"""
Unit tests for the TODO CLI Application
"""

import unittest
import os
import json
from main import TodoManager


class TestTodoManager(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.test_file = 'test_todos.json'
        self.manager = TodoManager(data_file=self.test_file)

    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_todo(self):
        """Test adding a new todo"""
        self.manager.add_todo("Test task")
        self.assertEqual(len(self.manager.todos), 1)
        self.assertEqual(self.manager.todos[0]['task'], "Test task")
        self.assertFalse(self.manager.todos[0]['completed'])

    def test_complete_todo(self):
        """Test completing a todo"""
        self.manager.add_todo("Test task")
        self.manager.complete_todo(1)
        self.assertTrue(self.manager.todos[0]['completed'])

    def test_delete_todo(self):
        """Test deleting a todo"""
        self.manager.add_todo("Test task")
        self.manager.delete_todo(1)
        self.assertEqual(len(self.manager.todos), 0)

    def test_load_save_todos(self):
        """Test loading and saving todos"""
        self.manager.add_todo("Test task")

        # Create a new manager instance to test loading
        new_manager = TodoManager(data_file=self.test_file)
        self.assertEqual(len(new_manager.todos), 1)
        self.assertEqual(new_manager.todos[0]['task'], "Test task")


if __name__ == '__main__':
    unittest.main()
