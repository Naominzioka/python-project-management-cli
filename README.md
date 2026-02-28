# Python Project Management CLI

A small command-line project management tool for creating users, projects and tasks, with JSON-backed persistence.

This repository provides a minimal, test-covered CLI that demonstrates a simple data model (`User`, `Project`, `Task`), a small modular CLI parser, and file-based storage utilities.

**Quick links**

- CLI entrypoint: [main.py](main.py)
- CLI parser: [cli_parser.py](cli_parser.py)
- Command handlers: [handlers.py](handlers.py)
- Models: [models/user.py](models/user.py), [models/project.py](models/project.py), [models/task.py](models/task.py)
- Storage helper: [utils/storage_handler.py](utils/storage_handler.py)
- Tests: [tests/](tests/)

## Features

- Create and list users
- Create, list and delete projects (projects are owned by users)
- Create tasks assigned to projects and users
- Mark tasks as complete
- JSON file persistence stored under the `data/` directory

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt` (used for development and testing)

Install dependencies (recommended in a virtual environment):

```bash
python -m pip install -r requirements.txt
```

## Project layout

- `main.py` — program entry point that wires the CLI. It now uses `cli_parser.setup_parser()` and `handlers` functions.
- `cli_parser.py` — builds the `argparse` parser and maps subcommands to handlers.
- `handlers.py` — command handler functions that implement the CLI behavior.
- `models/` — data models for `User`, `Project`, and `Task` with file read/write helpers.
- `utils/storage_handler.py` — small helper for reading/writing JSON files.
- `data/` — JSON files created at runtime: `users.json`, `projects.json`, `tasks.json`.
- `tests/` — pytest test suite covering models and handlers.

## Usage

The CLI is executed via `python main.py <command> [args...]`.

Examples:

- Add a user

```bash
python main.py add-user "John Doe" john@example.com
```

- List users

```bash
python main.py list-users
```

- Add a project (owner must be an existing user email)

```bash
python main.py add-project "Website" "Landing page redesign" 2026-12-31 john@example.com
```

- List projects for a user

```bash
python main.py list-projects john@example.com
```

- Delete a project by id

```bash
python main.py delete-project 1
```

- Add a task to a project (project id must exist, assigned user must exist)

```bash
python main.py add-task 1 "Design hero" Incomplete john@example.com
```

- Mark a task complete

```bash
python main.py mark-task-as-complete 2
```

Notes:

- Commands are wired in `cli_parser.py` and call functions in `handlers.py`.
- The handlers operate on in-memory model lists and persist using the utility `save_to_file` when modifications occur.

## Data files

By default the app saves JSON files into the `data/` directory:

- `data/users.json` — list of users
- `data/projects.json` — list of projects
- `data/tasks.json` — list of tasks

`utils/storage_handler.py` ensures the directory exists before writing.

## Tests

Run the test suite with `pytest`:

```bash
pytest -q
```

Tests currently cover model behavior and handler functions. When modifying CLI wiring, update `tests/test_main.py` to match the handler names (the project uses `handlers.py` functions rather than a `CLI` class).

## Development notes

- The CLI used to be implemented as a `CLI` class inside `main.py`. It has been refactored so `main.py` now uses `cli_parser.setup_parser()` and top-level handler functions in `handlers.py`. If you refactor further, keep tests in `tests/test_main.py` synced with the handler interface.
- Models expose class-level lists (`User.users`, `Project.projects`, `Task.tasks`) which are reset by tests — tests reset these lists to keep state isolated.
- `Project.due_date` uses a setter to validate the `YYYY-MM-DD` format and falls back to `TBD` for invalid values.

## Contributing

1. Fork the repo and create a feature branch.
2. Run and update tests in `tests/`.
3. Open a PR with a clear description and test coverage for behavior changes.

## License

This project is provided as-is for learning and demonstration purposes.
