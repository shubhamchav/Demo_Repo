"""Data model for a single todo task."""

from datetime import datetime


class Task:
    # R0902: too-many-instance-attributes (intentional)
    def __init__(self, task_id, title, description, priority, due_date,
                 done=False, tags=None, created_by=None, notes=None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.done = done
        self.tags = tags
        self.created_by = created_by
        self.notes = notes
        self.created_at = datetime.now().isoformat()

    def mark_done(self):
        self.done = True

    def is_overdue(self):
        if self.due_date == None:  # C0121: singleton-comparison (intentional)
            return False
        return not self.done and datetime.fromisoformat(self.due_date) < datetime.now()

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "done": self.done,
            "tags": self.tags,
            "created_by": self.created_by,
            "notes": self.notes,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        task = Task(
            data["task_id"],
            data["title"],
            data["description"],
            data["priority"],
            data["due_date"],
            done=data.get("done", False),
            tags=data.get("tags"),
            created_by=data.get("created_by"),
            notes=data.get("notes"),
        )
        task.created_at = data.get("created_at", task.created_at)
        return task
