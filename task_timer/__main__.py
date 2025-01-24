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
import os

TASK_FILE = "tasks.csv"

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []

    task_list = []
    try:
        with open(TASK_FILE, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None) 
            for row in reader:
                task_name, status, current_time, start_time, end_time, pre_paused_time = row
                new_task = Task(task_name)
                new_task.status = status
                new_task.current_time = float(current_time)
                new_task.start_time = float(start_time) if start_time else None
                new_task.end_time = float(end_time) if end_time else None
                new_task.pre_paused_time = float(pre_paused_time) if pre_paused_time else None
                task_list.append(new_task)
            save_tasks(task_list)

    except Exception as e:
        click.echo(f"Failed to load tasks: {e}")
    return task_list

def save_tasks(task_list):
    try:
        with open(TASK_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Task Name", "Status", "Time", "Start_time", "End_time", "Pre_pause_time"])
            for task in task_list:
                writer.writerow([task.task_name, task.status, task.current_time, task.start_time, task.end_time, task.pre_paused_time])
    except Exception as e:
        click.echo(f"Failed to save tasks: {e}")


@click.group()
def main():
    """Task Timer CLI"""
    pass

@main.command()
def list():
    """Lists all the current tasks with their names, statuses, and run times."""
    task_list = load_tasks()
    if len(task_list) == 0:
        click.echo("No current tasks. Use the 'create' command to add tasks.")
        return

    click.echo("")
    click
    click.echo("Task Name | Task Status | Task Time")
    for task in task_list:
        click.echo(task)

@main.command()
@click.option("--name", type=str, help="Create New Tasks.")
def create(name):
    """Create a new task."""

    task_list = load_tasks()
    task_name = name if name else f"task{len(task_list) + 1}"
    new_task = Task(task_name)

    task_list.append(new_task)
    save_tasks(task_list)

@main.command()
@click.option("--name", type=click.Choice([task.task_name for task in load_tasks()], case_sensitive=False), required=True, help="Toggle selected timer on or off.")
def toggle(name):
    """Toggle a task's timer."""
    task_list = load_tasks()
    try:
        for task in task_list:
            if task.task_name == name:
                if task.status == "Off":
                    task.start()
                elif task.status == "Paused":
                    task.resume()
                elif task.status == "Active" and task.start_time is not None:
                    task.pause()
    except Exception as e:
        click.echo(f"Faild to toggle task. {e}")

    save_tasks(task_list)

@main.command()
@click.option("--name", type=click.Choice([task.task_name for task in load_tasks()], case_sensitive=False), required=True, help="Delete a given task")
def delete(name):
    """Deletes the given task from the CSV file."""
    task_list = load_tasks()
    
    # Find the task to remove
    task_to_remove = next((task for task in task_list if task.task_name == name), None)

    if not task_to_remove:
        click.echo(f"Task '{name}' not found.")
        return

    # Remove the task and save the updated list
    task_list.remove(task_to_remove)
    save_tasks(task_list)

    click.echo(f"Successfully removed task '{name}'!")
    

@main.command()
@click.option('--filename', default='tasks.csv', help="The name of the CSV file to save task data to.")
def save(filename):
    """Saves the current tasks to csv file."""
    task_list = load_tasks()
    if len(task_list) == 0:
        click.echo("No tasks to save.")
    
    else:
        try:
            with open(filename, mode="w",  newline='') as file:
                writer = csv.writer(file)

                writer.writerow(["Task Name", "Status", "Time", "Start_time", "End_time", "Pre_pause_time"])

                for task in task_list:
                    writer.writerow([task.task_name, task.status, task.current_time, task.start_time, task.end_time, task.pre_paused_time])
        except Exception as e:
            click.echo(f"Faild to save tasks. {e}")

@main.command()
@click.option("--filename", default='tasks.csv', help="Loads task data from a csv file.")
def load(filename):
    """Loads the task data from file"""
    task_list = load_tasks()
    try:
        with open(filename, mode="r") as file:
            reader = csv.reader(file)

            #skip the header row
            next(reader, None)

            for row in reader:
                task_name, status, current_time, start_time, end_time, pre_paused_time = row
                new_task = Task(task_name)
                new_task.status = status
                new_task.current_time = float(current_time)
                new_task.start_time = float(start_time) if start_time else None
                new_task.end_time = float(end_time) if end_time else None
                new_task.pre_paused_time = float(pre_paused_time) if pre_paused_time else None

                task_list.append(new_task)

            save_tasks(task_list)
            
            click.echo(f"{len(task_list)} Tasks loaded from CSV")
            for task in task_list:
                print(task)

    except Exception as e:
        click.echo(f"Faild to load tasks. {e}")




if __name__ == "__main__":
    main()
