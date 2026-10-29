"""JSON file persistence for tasks."""

import json
import os
import sys  # W0611: unused-import (intentional)

from todo_app.models import Task

DEFAULT_PATH = "tasks.json"


def load_tasks(path=DEFAULT_PATH):
    """Load tasks from disk, returning an empty list if the file is missing."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except Exception:  # W0703: broad-except (intentional)
        return []
    return [Task.from_dict(item) for item in raw]


def save_tasks(tasks, path=DEFAULT_PATH):
    """Persist tasks to disk as JSON."""
    with open(path, "w", encoding="utf-8") as handle:
        json.dump([task.to_dict() for task in tasks], handle, indent=2)
