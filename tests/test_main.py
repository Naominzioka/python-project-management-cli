import argparse
import pytest

from models.user import User
from models.project import Project
from models.task import Task
from main import CLI


def setup_function():
    User.users = []
    Project.projects = []
    Task.tasks = []
    Task.id_counter = 1
    Project.id_counter = 1


def test_handle_add_user(monkeypatch, capsys):
    # prevent file IO during CLI init
    monkeypatch.setattr(User, "read_from_file", lambda: None)
    monkeypatch.setattr(Project, "read_from_file", lambda: None)
    monkeypatch.setattr(Task, "read_from_file", lambda: None)
    monkeypatch.setattr(User, "save_users_to_file", lambda: None)

    cli = CLI()
    args = argparse.Namespace(name="Alice", email="alice@example.com")
    cli.handle_add_user(args)

    captured = capsys.readouterr()
    assert "User Alice created" in captured.out
    assert any(u.email == "alice@example.com" for u in User.users)


def test_handle_add_task_project_not_found(monkeypatch, capsys):
    monkeypatch.setattr(User, "read_from_file", lambda: None)
    monkeypatch.setattr(Project, "read_from_file", lambda: None)
    monkeypatch.setattr(Task, "read_from_file", lambda: None)

    # ensure no projects exist
    Project.projects = []
    User.users = [User(name="Bob", email="bob@example.com")]

    cli = CLI()
    args = argparse.Namespace(project_id=99, title="T1", status="Incomplete", assigned_to="bob@example.com")
    cli.handle_add_task(args)

    captured = capsys.readouterr()
    assert "Error: Project with ID 99 not found." in captured.out


def test_handle_add_task_success(monkeypatch, capsys):
    monkeypatch.setattr(User, "read_from_file", lambda: None)
    monkeypatch.setattr(Project, "read_from_file", lambda: None)
    monkeypatch.setattr(Task, "read_from_file", lambda: None)
    # prevent saving to file
    monkeypatch.setattr(Task, "save_to_file", lambda: None)

    User.users = [User(name="Carol", email="carol@example.com")]
    Project.projects = [Project(title="P", description="D", due_date="2026-12-31", owner_email="carol@example.com", id=1)]

    cli = CLI()
    args = argparse.Namespace(project_id=1, title="Task A", status="Incomplete", assigned_to="carol@example.com")
    cli.handle_add_task(args)

    captured = capsys.readouterr()
    assert "✅ Task 'Task A' added to Project 1." in captured.out
    assert any(t.title == "Task A" and t.project_id == 1 for t in Task.tasks)
