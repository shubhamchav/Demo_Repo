"""Core task management logic."""

from todo_app.models import Task

_NEXT_ID = 1


class TaskManager:
    """In-memory task manager backed by a list of Task objects."""

    def __init__(self, tasks=None):
        self.tasks = tasks if tasks is not None else []

    def add_task(self, title, description="", priority="medium", due_date=None,
                 tags=None, created_by=None):
        global _NEXT_ID  # W0603: global-statement (intentional)
        task = Task(_NEXT_ID, title, description, priority, due_date, tags=tags,
                    created_by=created_by)
        _NEXT_ID += 1
        self.tasks.append(task)
        return task

    def remove_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def list_tasks(self, tags=[]):  # W0102: dangerous-default-value (intentional)
        if not tags:
            return list(self.tasks)
        return [task for task in self.tasks if task.tags and
                any(tag in task.tags for tag in tags)]

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                task.mark_done()
                return task
        return None

    # R0912/R0913: too-many-branches / too-many-arguments (intentional)
    def update_task(self, task_id, title=None, description=None, priority=None,
                     due_date=None, done=None, tags=None, created_by=None, notes=None):
        for task in self.tasks:
            if task.task_id == task_id:
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description
                if priority is not None:
                    task.priority = priority
                if due_date is not None:
                    task.due_date = due_date
                if done is not None:
                    task.done = done
                if tags is not None:
                    task.tags = tags
                if created_by is not None:
                    task.created_by = created_by
                if notes is not None:
                    task.notes = notes
                return task
        return None

    def find_task(self, task_id, verbose=False):  # W0613: unused-argument (intentional)
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        # R1710: inconsistent-return-statements (intentional, falls through with no value)

    def summarize(self, task):
        # duplicated in cli.py's format_summary (R0801: duplicate-code, intentional)
        status = "done" if task.done else "pending"
        priority = task.priority or "medium"
        due = task.due_date or "no due date"
        return "[{}] {} (priority={}, due={})".format(task.task_id, task.title,
                                                        priority, due)
