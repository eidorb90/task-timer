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
import time
import select
import sys
from colorama import Fore

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

def clear_console():
    """
    Clears the terminal screen, depending on the operating system.
    
    This function works by executing the appropriate command to clear the console:
    'cls' for Windows and 'clear' for Unix-based systems (e.g., Linux, macOS).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def non_blocking_input():
    """
    Checks for non-blocking user input by using the select method, which allows
    the program to continue running while waiting for user input.
    
    Returns:
        str or None: The user input as a string, or None if no input was detected.
    """
    i, o, e = select.select([sys.stdin], [], [], 1)
    if i:
        return sys.stdin.readline().strip()
    else:
        
        return None

@click.group()
def main():
    """Task Timer CLI"""
    pass

@main.command()
def list():
    """Lists all the current tasks with their names, statuses, and run times."""
    task_list = load_tasks()
    if len(task_list) == 0:
        click.echo(f"No current tasks. Use the {Fore.MAGENTA}'create'{Fore.RESET} command to add tasks.")
        return

    click.echo("")
    click
    print("Task Name      | Task Status  | Task Time")
    print("-----------------------------------------")
    for task in task_list:
        click.echo(task)
    print("-----------------------------------------")
    
@main.command()
@click.option("--name", type=str, help="Create New Tasks.")
def create(name):
    """Create a new task."""

    task_list = load_tasks()
    task_name = name if name else f"task{len(task_list) + 1}"
    new_task = Task(task_name)

    task_list.append(new_task)
    save_tasks(task_list)
    click.echo(f"{Fore.MAGENTA}{name}{Fore.RESET}{Fore.WHITE}:{Fore.RESET}{Fore.GREEN} Successfully Created{Fore.RESET}")

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
        click.echo(f"{Fore.RED}Faild to toggle task. {e}{Fore.RESET}")

    save_tasks(task_list)

@main.command()
@click.option("--name", type=click.Choice([task.task_name for task in load_tasks()], case_sensitive=False), help="Real time display of the selected timer(s)")
def display(name):
    """
    Displays the status and run time of tasks in real-time.
    Provides the option to view all tasks or a specific task.
    Allows the user to exit the display loop by pressing 'c'.
    """
    task_list = load_tasks()
    display_tasks = True

    if name == None:
        """
        Displays all tasks in real-time, updating every second.
        """
        if len(task_list) == 0:
            print(f"No current tasks. Use the {Fore.MAGENTA}'Create'{Fore.RESET} command to create tasks.")

        print("")
        while display_tasks:
            clear_console()
            print(f"Enter {Fore.BLUE}'c'{Fore.RESET} to exit display:")
            print("Task Name      | Task Status  | Task Time")
            print("-----------------------------------------")

            for task in task_list:
                print(task)
            print("-----------------------------------------")
            
            user_input = non_blocking_input()
            try:
                if user_input.lower() == "c":
                    display_tasks = False
            except: 
                continue
            time.sleep(1)

    elif name in (task.task_name for task in task_list):
        """
        Displays a specific task in real-time, updating every second.
        """
        print("")
        while display_tasks:
            clear_console()
            print("Enter 'c' to exit display (hint: you have to hit enter right away)")
            print("Task Name | Task Status | Task Time")
            for task in task_list:
                if task.task_name == name:
                    print(task)
            user_input = non_blocking_input()
            try:
                if user_input.lower() == "c":
                    display_tasks = False
            except: 
                continue
            time.sleep(1)

    else:
        print(f"{Fore.MAGENTA}{name}{Fore.RESET}{Fore.WHITE}:{Fore.RESET}{Fore.RED} NOT A VALID TASK!!!{Fore.RESET}")

@main.command()
@click.option("--name", type=click.Choice([task.task_name for task in load_tasks()], case_sensitive=False), required=True, help="Delete a given task")
def delete(name):
    """Deletes the given task from the CSV file."""
    task_list = load_tasks()
    
    # Find the task to remove
    task_to_remove = next((task for task in task_list if task.task_name == name), None)

    if not task_to_remove:
        click.echo(f"{Fore.RED}Task {Fore.RESET}{Fore.MAGENTA}'{name}'{Fore.RESET}{Fore.RED} not found.{Fore.RESET}")
        return

    # Remove the task and save the updated list
    task_list.remove(task_to_remove)
    save_tasks(task_list)

    click.echo(f"{Fore.GREEN}Successfully removed task{Fore.RESET} {Fore.MAGENTA}'{name}'{Fore.RESET}{Fore.GREEN}!{Fore.RESET}") 
    
@main.command()
@click.option('--filename', default='tasks.csv', help="The name of the CSV file to save task data to.")
def save(filename):
    """Saves the current tasks to csv file."""
    task_list = load_tasks()
    if len(task_list) == 0:
        click.echo(f"{Fore.RED}No tasks to save.{Fore.RESET}")
    
    else:
        try:
            with open(filename, mode="w",  newline='') as file:
                writer = csv.writer(file)

                writer.writerow(["Task Name", "Status", "Time", "Start_time", "End_time", "Pre_pause_time"])

                for task in task_list:
                    writer.writerow([task.task_name, task.status, task.current_time, task.start_time, task.end_time, task.pre_paused_time])
        except Exception as e:
            click.echo(f"{Fore.RED}Faild to save tasks. {e}{Fore.RESET}")

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
            
            click.echo(f"{Fore.MAGENTA}{len(task_list)}{Fore.RESET} {Fore.GREEN}Tasks loaded from CSV{Fore.RESET}")
            for task in task_list:
                print(task)

    except Exception as e:
        click.echo(f"{Fore.RED}Faild to load tasks. {e}{Fore.RESET}")

@main.command()
@click.option("--timer", type=click.Choice([task.task_name for task in load_tasks()]), required=True, help="Reset a given timer.")
def reset(timer):   
    """
    Resets the given timer.
    """
    task_list = load_tasks()
    task_names = [task.task_name for task in task_list]
    if timer not in task_names:
        click.echo(f"{Fore.MAGENTA}{timer}{Fore.RESET}{Fore.RED} Couldn't reset.{Fore.RESET}")
        return 
    
    for task in task_list:
        if task.task_name == timer:
            task.start_time = None
            task.end_time = None
            task.current_time = 0
            task.pre_paused_time = 0

    save_tasks(task_list)
    click.echo(f"{Fore.MAGENTA}{timer}{Fore.RESET}{Fore.WHITE}:{Fore.RESET}{Fore.RED} Successfully reset.{Fore.RESET}")
x``




if __name__ == "__main__":
    main()
