"""
__main__.py
Brodie Rogers <brodie.rogers@students.cune.edu>
2025-01-22

A Python-based task timer application to help you manage and track time for multiple tasks efficiently. 
This program provides functionality to create, toggle, and display timers for tasks in real-time, making it an excellent tool for productivity and time management.
"""
import click
import csv
from task_timer.task import Task

new_task = Task("test")
task_list = [new_task]

@click.group()
def main():
    """Task Timer CLI"""
    pass

@main.command()
def list():
    """Lists all the current tasks with their names, statuses, and run times."""
    new_task = Task("test")
    task_list = [new_task]
    if len(task_list) == 0:
        click.echo("No current tasks. Use the 'create' command to add tasks.")
        return

    click.echo("")
    click.echo("Task Name | Task Status | Task Time")
    for task in task_list:
        click.echo(task)

@main.command()
# @main.option(type=str, help="Create New Tasks.")
def create():
    """Create a new task."""
    click.echo("Feature coming soon!")

@main.command()
@main.option("--task", type=str, help="Toggle selected timer on or off.")
def toggle(task):
    """Toggle a task's timer."""
    click.echo(f"Toggling task: {task}")


if __name__ == "__main__":
    main()
