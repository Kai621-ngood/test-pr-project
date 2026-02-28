#!/usr/bin/env python3
"""
Simple TODO CLI Application
A command-line tool to manage your daily tasks
"""
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional
import os.path
import json

class TodoManager:
    def __init__(self, data_file: str = 'todos.json'):
        # 验证文件名，防止路径遍历
        if not data_file or '..' in data_file or '/' in data_file or '\\' in data_file:
            raise ValueError("Invalid data file name")

        # 限制在当前目录或指定安全目录
        safe_dir = os.path.abspath('.')
        self.data_file = os.path.join(safe_dir, os.path.basename(data_file))

        # 确保文件在安全目录内
        if not os.path.abspath(self.data_file).startswith(safe_dir):
            raise ValueError("File path not allowed")

    def load_todos(self) -> List[Dict]:
        """Load todos from JSON file with size and structure validation"""
        if not os.path.exists(self.data_file):
            return []

        try:
            # 检查文件大小，防止过大文件导致内存耗尽
            file_size = os.path.getsize(self.data_file)
            if file_size > 10 * 1024 * 1024:  # 10MB 限制
                raise ValueError("File too large")

            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 验证数据结构
            if not isinstance(data, list):
                raise ValueError("Invalid data format: expected list")

            # 验证每个 todo 项的结构
            for item in data:
                if not isinstance(item, dict):
                    raise ValueError("Invalid todo item format")
                required_fields = ['id', 'task', 'completed']
                if not all(field in item for field in required_fields):
                    raise ValueError("Missing required fields in todo item")

            return data

        except (json.JSONDecodeError, IOError, ValueError) as e:
            print(f"⚠ Warning: Could not load {self.data_file}: {e}")
            print("Starting with empty todo list")
            return []

    def save_todos(self) -> None:
        """Save todos to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"✗ Error saving todos: {e}")

    def add_todo(self, task: str, priority: str = 'normal') -> None:
        """Add a new todo item with optional priority"""
        next_id = max([t['id'] for t in self.todos], default=0) + 1
        todo = {
            'id': next_id,
            'task': task,
            'completed': False,
            'priority': priority,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'completed_at': None
        }
        self.todos.append(todo)
        self.save_todos()
        priority_icon = self._get_priority_icon(priority)
        print(f"✓ Added: {priority_icon} {task} [ID: {next_id}]")

    def list_todos(self, show_all: bool = True) -> None:
        """List todo items"""
        if not self.todos:
            print("📝 No tasks found. Add one with: python main.py add 'Your task'")
            return

        display_todos = self.todos if show_all else [t for t in self.todos if not t['completed']]

        if not display_todos:
            print("📝 No pending tasks!")
            return

        print("\n📋 Your TODO List:")
        print("=" * 70)

        # Sort by priority and completion status
        priority_order = {'high': 0, 'normal': 1, 'low': 2}
        sorted_todos = sorted(
            display_todos,
            key=lambda x: (x['completed'], priority_order.get(x.get('priority', 'normal'), 1))
        )

        for todo in sorted_todos:
            status = "✓" if todo['completed'] else "○"
            priority_icon = self._get_priority_icon(todo.get('priority', 'normal'))
            task_display = todo['task']

            if todo['completed']:
                task_display = f"\033[9m{task_display}\033[0m"  # Strikethrough

            print(f"{status} [{todo['id']:3d}] {priority_icon} {task_display}")

        print("=" * 70)
        completed = sum(1 for t in self.todos if t['completed'])
        print(f"Total: {len(self.todos)} | Completed: {completed} | Pending: {len(self.todos) - completed}\n")

    def complete_todo(self, todo_id: int) -> None:
        """Mark a todo as completed"""
        todo = self._find_todo(todo_id)
        if todo:
            if todo['completed']:
                print(f"⚠ Task already completed: {todo['task']}")
                return
            todo['completed'] = True
            todo['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_todos()
            print(f"✓ Completed: {todo['task']}")
        else:
            print(f"✗ Task with ID {todo_id} not found")

    def delete_todo(self, todo_id: int) -> None:
        """Delete a todo item"""
        for i, todo in enumerate(self.todos):
            if todo['id'] == todo_id:
                task = todo['task']
                self.todos.pop(i)
                self.save_todos()
                print(f"✓ Deleted: {task}")
                return
        print(f"✗ Task with ID {todo_id} not found")

    def clear_completed(self) -> None:
        """Remove all completed tasks"""
        completed_count = sum(1 for t in self.todos if t['completed'])
        self.todos = [t for t in self.todos if not t['completed']]
        self.save_todos()
        print(f"✓ Cleared {completed_count} completed task(s)")

    def _find_todo(self, todo_id: int) -> Optional[Dict]:
        """Find a todo by ID"""
        return next((t for t in self.todos if t['id'] == todo_id), None)

    def _get_priority_icon(self, priority: str) -> str:
        """Get icon for priority level"""
        icons = {'high': '🔴', 'normal': '🟡', 'low': '🟢'}
        return icons.get(priority, '🟡')


def print_help():
    """Print usage instructions"""
    print("""
📝 Simple TODO CLI Application

Usage:
    python main.py list [--pending]        - List all tasks (or only pending)
    python main.py add "Task" [priority]   - Add a new task (priority: high/normal/low)
    python main.py complete <id>           - Mark task as completed
    python main.py delete <id>             - Delete a task
    python main.py clear                   - Remove all completed tasks
    python main.py help                    - Show this help message

Examples:
    python main.py add "Buy groceries" high
    python main.py add "Read book"
    python main.py complete 1
    python main.py delete 2
    python main.py list --pending
    python main.py clear
""")


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    manager = TodoManager()
    command = sys.argv[1].lower()

    try:
        if command == 'add':
            if len(sys.argv) < 3:
                print("✗ Error: Please provide a task description")
                return

            # Check if last argument is a priority
            valid_priorities = ['high', 'normal', 'low']
            if sys.argv[-1].lower() in valid_priorities:
                task = ' '.join(sys.argv[2:-1]).strip()
                priority = sys.argv[-1].lower()
            else:
                task = ' '.join(sys.argv[2:]).strip()
                priority = 'normal'

            if not task:
                print("✗ Error: Task description cannot be empty")
                return

            manager.add_todo(task, priority)

        elif command == 'list':
            show_all = '--pending' not in sys.argv
            manager.list_todos(show_all)

        elif command == 'complete':
            if len(sys.argv) < 3:
                print("✗ Error: Please provide a task ID")
                return
            todo_id = int(sys.argv[2])
            manager.complete_todo(todo_id)

        elif command == 'delete':
            if len(sys.argv) < 3:
                print("✗ Error: Please provide a task ID")
                return
            todo_id = int(sys.argv[2])
            manager.delete_todo(todo_id)

        elif command == 'clear':
            manager.clear_completed()

        elif command == 'help':
            print_help()

        else:
            print(f"✗ Unknown command: {command}")
            print_help()

    except ValueError:
        print("✗ Error: Task ID must be a number")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


if __name__ == '__main__':
    main()