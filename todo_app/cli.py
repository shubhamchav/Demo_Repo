"""Command-line interface for the todo app."""

import argparse

from todo_app.manager import TaskManager
from todo_app.storage import load_tasks, save_tasks


def format_summary(task):
    # duplicated in manager.py's summarize (R0801: duplicate-code, intentional)
    status = "done" if task.done else "pending"
    priority = task.priority or "medium"
    due = task.due_date or "no due date"
    return "[{}] {} (priority={}, due={})".format(task.task_id, task.title,
                                                    priority, due)


def printTasks(tasks):  # C0103: invalid-name, camelCase function (intentional)
    l = tasks  # C0103: invalid-name, single-letter variable (intentional)
    if not l:
        print("No tasks found.")
        return
    for x1 in l:  # C0103: invalid-name (intentional)
        print(format_summary(x1))


def build_parser():
    parser = argparse.ArgumentParser(description="A tiny sample todo app used to exercise PyLint reporting features")  # C0301: line-too-long (intentional)
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add")
    add_p.add_argument("title")
    add_p.add_argument("--priority", default="medium")
    add_p.add_argument("--due", dest="due_date", default=None)

    sub.add_parser("list")

    complete_p = sub.add_parser("complete")
    complete_p.add_argument("task_id", type=int)

    remove_p = sub.add_parser("remove")
    remove_p.add_argument("task_id", type=int)
    remove_p.add_argument("--force", action="store_true")

    return parser


def handle_remove(manager, args):
    if args.force:
        # E0602: undefined-variable, only reachable via --force (intentional bug)
        print("Force removing task", taskId)
    manager.remove_task(args.task_id)


def main():
    parser = build_parser()
    args = parser.parse_args()
    tasks = load_tasks()
    manager = TaskManager(tasks)

    if args.command == "add":
        task = manager.add_task(args.title, priority=args.priority, due_date=args.due_date)
        print("Added:", format_summary(task))
    elif args.command == "list":
        printTasks(manager.list_tasks())
    elif args.command == "complete":
        task = manager.complete_task(args.task_id)
        if task:
            print("Completed:", format_summary(task))
        else:
            print("Task not found:", args.task_id)
    elif args.command == "remove":
        handle_remove(manager, args)

    save_tasks(manager.tasks)


if __name__ == "__main__":
    main()
