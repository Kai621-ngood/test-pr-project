# Simple TODO CLI Application

A lightweight command-line TODO list manager written in Python. Perfect for managing your daily tasks right from the terminal.

## Features

- Add new tasks
- List all tasks
- Mark tasks as completed
- Delete tasks
- Persistent storage using JSON
- Simple and intuitive command-line interface

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd PythonProject1
```

2. Make sure you have Python 3.6 or higher installed:
```bash
python --version
```

## Usage

### Add a new task
```bash
python main.py add "Buy groceries"
```

### List all tasks
```bash
python main.py list
```

### Complete a task
```bash
python main.py complete 1
```

### Delete a task
```bash
python main.py delete 1
```

### Show help
```bash
python main.py help
```

## Examples

```bash
# Add some tasks
python main.py add "Finish project documentation"
python main.py add "Review pull requests"
python main.py add "Update dependencies"

# List all tasks
python main.py list

# Output:
# Your TODO List:
# ------------------------------------------------------------
# ○ [1] Finish project documentation
# ○ [2] Review pull requests
# ○ [3] Update dependencies
# ------------------------------------------------------------

# Complete a task
python main.py complete 1

# Delete a task
python main.py delete 3
```

## Running Tests

Run the unit tests to verify everything works correctly:

```bash
python test_1.py
```

## Data Storage

Tasks are stored in a `todos.json` file in the project directory. This file is created automatically when you add your first task.

## Project Structure

```
PythonProject1/
├── main.py           # Main application code
├── test_1.py         # Unit tests
├── README.md         # This file
├── requirements.txt  # Python dependencies (if any)
├── .gitignore       # Git ignore rules
└── todos.json       # Data file (created automatically)
```

## Contributing

Feel free to fork this project and submit pull requests with improvements!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Chris Xing

## Version

1.0.0
