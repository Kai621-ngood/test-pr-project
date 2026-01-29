#!/usr/bin/env python3
"""
Simple TODO CLI Application
A command-line tool to manage your daily tasks
"""

import json
import os
from datetime import datetime


class TodoManager:
    def __init__(self, data_file='todos.json'):
        self.data_file = data_file
        self.todos = self.load_todos()

    def load_todos(self):
        """Load todos from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load {self.data_file}: {e}")
                print("Starting with empty todo list")
                return []
        return []

    def save_todos(self):
        """Save todos to JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)

    def add_todo(self, task):
        """Add a new todo item"""
        # Generate ID based on max existing ID to avoid conflicts
        next_id = max([t['id'] for t in self.todos], default=0) + 1
        todo = {
            'id': next_id,
            'task': task,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.todos.append(todo)
        self.save_todos()
        print(f"✓ Added: {task}")

    def list_todos(self):
        """List all todo items"""
        if not self.todos:
            print("No tasks found. Add one with: python main.py add 'Your task'")
            return

        print("\nYour TODO List:")
        print("-" * 60)
        for todo in self.todos:
            status = "✓" if todo['completed'] else "○"
            print(f"{status} [{todo['id']}] {todo['task']}")
        print("-" * 60)

    def complete_todo(self, todo_id):
        """Mark a todo as completed"""
        for todo in self.todos:
            if todo['id'] == todo_id:
                todo['completed'] = True
                self.save_todos()
                print(f"✓ Completed: {todo['task']}")
                return
        print(f"Task with ID {todo_id} not found")

    def delete_todo(self, todo_id):
        """Delete a todo item"""
        for i, todo in enumerate(self.todos):
            if todo['id'] == todo_id:
                task = todo['task']
                self.todos.pop(i)
                self.save_todos()
                print(f"✓ Deleted: {task}")
                return
        print(f"Task with ID {todo_id} not found")


def print_help():
    """Print usage instructions"""
    print("""
Simple TODO CLI Application

Usage:
    python main.py list                    - List all tasks
    python main.py add "Task description"  - Add a new task
    python main.py complete <id>           - Mark task as completed
    python main.py delete <id>             - Delete a task
    python main.py help                    - Show this help message

Examples:
    python main.py add "Buy groceries"
    python main.py complete 1
    python main.py delete 2
""")


def main():
    import sys

    if len(sys.argv) < 2:
        print_help()
        return

    manager = TodoManager()
    command = sys.argv[1].lower()

    if command == 'add':
        if len(sys.argv) < 3:
            print("Error: Please provide a task description")
            return
        task = ' '.join(sys.argv[2:]).strip()
        if not task:
            print("Error: Task description cannot be empty")
            return
        manager.add_todo(task)

    elif command == 'list':
        manager.list_todos()

    elif command == 'complete':
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID")
            return
        try:
            todo_id = int(sys.argv[2])
            manager.complete_todo(todo_id)
        except ValueError:
            print("Error: Task ID must be a number")

    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID")
            return
        try:
            todo_id = int(sys.argv[2])
            manager.delete_todo(todo_id)
        except ValueError:
            print("Error: Task ID must be a number")

    elif command == 'help':
        print_help()

    else:
        print(f"Unknown command: {command}")
        print_help()


if __name__ == '__main__':
    main()
