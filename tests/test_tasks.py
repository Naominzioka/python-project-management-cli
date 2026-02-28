import os
import pytest

from models.task import Task


def setup_function():
    # reset class state between tests
    Task.tasks = []
    Task.id_counter = 1


def test_task_creation_and_mark_complete():
    t = Task(project_id=1, title="Test Task", assigned_to="user@example.com")
    assert t.id == 1
    assert t.status == "Incomplete"

    t.mark_as_complete()
    assert t.status == "Complete"

    d = t.to_dict()
    assert d["id"] == 1
    assert d["project_id"] == 1
    assert d["title"] == "Test Task"
    assert d["assigned_to"] == "user@example.com"
    assert d["status"] == "Complete"


def test_id_counter_with_provided_id():
    # provide a high id and ensure id_counter updates
    t = Task(project_id=2, title="Other", assigned_to="a@b.com", id=5)
    assert t.id == 5
    assert Task.id_counter == 6


def test_read_from_file_missing(tmp_path, monkeypatch):
    # point task_data to a non-existent file and ensure read_from_file sets defaults
    Task.task_data = str(tmp_path / "no_tasks.json")
    # ensure file does not exist
    if os.path.exists(Task.task_data):
        os.remove(Task.task_data)

    Task.read_from_file()
    assert Task.tasks == []
    assert Task.id_counter == 1
