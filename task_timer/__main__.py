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
    """
    Loads task data from the CSV file and creates Task objects.
    
    This function reads task data from a CSV file and reconstructs Task objects
    with their saved state. If the file doesn't exist, returns an empty list.
    
    Returns:
        list: A list of Task objects loaded from the CSV file.
              Returns empty list if file doesn't exist or on error.
    
    File Format:
        CSV with headers: Task Name, Status, Time, Start_time, End_time, Pre_pause_time
        Each row represents one task with its saved state
    """
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
    """
    Saves the current task list to a CSV file.
    
    This function writes all task data to a CSV file for persistence.
    Each task's state is preserved including timing information and status.
    
    Parameters:
        task_list (list): List of Task objects to save
    
    CSV Structure:
        Headers: Task Name, Status, Time, Start_time, End_time, Pre_pause_time
        Each row contains the corresponding values for one task
    """
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
    """
    Task Timer CLI: A command-line interface for managing task timers.
    
    Provides a suite of commands for creating, managing, and monitoring task timers.
    Supports concurrent task tracking, time editing, and data persistence.
    """
    pass

@main.command()
def list():
    """
    Displays all current tasks with their names, statuses, and run times.
    
    Output Format:\n
        Task Name      | Task Status  | Task Time\n
        -----------------------------------------\n
        [task entries]\n
        -----------------------------------------\n
    
    Status Colors:\n
        - Red: Off\n
        - Magenta: Paused\n
        - Green: Active\n
    """
    task_list = load_tasks()
    if len(task_list) == 0:
        click.echo(f"No current tasks. Use the {Fore.MAGENTA}'create'{Fore.RESET} command to add tasks.")
        return

    click.echo("")
    click
    print(f"{Fore.WHITE}Task Name      | Task Status  | Task Time{Fore.RESET}")
    print(f"{Fore.WHITE}-----------------------------------------{Fore.RESET}")
    for task in task_list:
        click.echo(task)
    print(f"{Fore.WHITE}-----------------------------------------{Fore.RESET}")
    
@main.command()
@click.option("--name", type=str, help="Create New Tasks.")
def create(name):
    """
    Creates a new task timer instance.
    
    If no name is provided, automatically generates a name in the format 'taskN'
    where N is the next available number. Prevents duplicate task names to ensure
    unique identification of each task.
    
    Parameters:\n
        - name (str, optional): Custom name for the task\n
    
    Returns:\n
        - Confirmation message indicating success or failure of task creation\n
    
    Error Handling:\n
        - Prevents creation of tasks with duplicate names\n
        - Provides feedback on creation status with color-coded output\n
    """

    task_list = load_tasks()
    task_name_list = [task.task_name for task in task_list]
    if name in task_name_list:
        return click.echo(f"{Fore.MAGENTA}{name}{Fore.RESET}{Fore.WHITE}:{Fore.RESET}{Fore.RED} Couldn't be Created due to the name being in use!{Fore.RESET}")

    task_name = name if name else f"task{len(task_list) + 1}"
    new_task = Task(task_name)

    task_list.append(new_task)
    save_tasks(task_list)
    click.echo(f"{Fore.MAGENTA}{name}{Fore.RESET}{Fore.WHITE}:{Fore.RESET}{Fore.GREEN} Successfully Created{Fore.RESET}")

@main.command()
@click.option("--name", type=click.Choice([task.task_name for task in load_tasks()], case_sensitive=False), required=True, help="Toggle selected timer on or off.")
def toggle(name):
    """
    Toggles the state of a specified task timer.
    
    Manages the task's state transitions between Off, Active, and Paused states.
    Each toggle action updates the task's timing information appropriately.
    
    State Transitions:\n
        - Off -> Active: Starts the timer\n
        - Paused -> Active: Resumes the timer\n
        - Active -> Paused: Pauses the timer\n
    
    Parameters:\n
        - name (str): Name of the task to toggle, must match existing task\n
    
    Error Handling:\n
        - Validates task existence before attempting state change\n
        - Preserves accumulated time during pause/resume cycles\n
    """
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
    Provides real-time display of task timer information.
    
    Continuously updates the display showing current task status and elapsed time.
    Supports viewing either a single specified task or all tasks simultaneously.
    
    Display Modes:\n
        - Single Task: Shows detailed information for specified task\n
        - All Tasks: Displays overview of all tasks when no name specified\n
    
    Parameters:\n
        - name (str, optional): Name of specific task to display\n
    
    User Interface:\n
        - Updates every second\n
        - Provides clean display with task status and elapsed time\n
        - Supports 'c' key to exit display mode\n
        
    Format:\n
        Task Name      | Task Status  | Task Time\n
        -----------------------------------------\n
        [task entries]\n
        -----------------------------------------\n
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
            print(f"{Fore.WHITE}Task Name      | Task Status  | Task Time{Fore.RESET}")
            print(f"{Fore.WHITE}-----------------------------------------{Fore.RESET}")

            for task in task_list:
                print(task)
            print(f"{Fore.WHITE}-----------------------------------------{Fore.RESET}")
            
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
            print(f"Enter {Fore.BLUE}'c'{Fore.RESET} to exit display:")
            print("Task Name      | Task Status  | Task Time")
            print("-----------------------------------------")
            for task in task_list:
                if task.task_name == name:
                    print(task)
                    print("-----------------------------------------")
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
    """
    Removes a specified task from the task list.
    
    Permanently deletes a task and its associated timing data.
    Automatically updates the persistent storage after deletion.
    
    Parameters:\n
        - name (str): Name of the task to delete\n
    
    Error Handling:\n
        - Validates task existence before deletion\n
        - Provides feedback on deletion status\n
        - Updates CSV file to reflect changes\n
    """
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
    """
    Exports current task data to a CSV file.
    
    Saves all task information including status, timing data, and metadata
    to a specified CSV file for persistence or data transfer.
    
    Parameters:\n
        - filename (str): Target CSV file name, defaults to 'tasks.csv'\n
    
    File Format:\n
        - CSV with headers for all task attributes\n
        - Preserves complete task state including timing information\n
    
    Error Handling:\n
        - Handles file write errors gracefully\n
        - Provides feedback on save operation status\n
    """
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
    """
    Imports task data from a CSV file.
    
    Reconstructs task objects from saved data, including all timing
    information and status data. Updates current task list with loaded data.
    
    Parameters:\n
        - filename (str): Source CSV file name, defaults to 'tasks.csv'\n
    
    Data Handling:\n
        - Preserves all task attributes from file\n
        - Maintains timing accuracy for loaded tasks\n
        - Updates runtime task list with loaded data\n
    
    Error Handling:\n
        - Validates CSV format and data integrity\n
        - Provides feedback on load operation status\n
    """
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
@click.option("--name", type=click.Choice([task.task_name for task in load_tasks()]), required=True, help="Reset a given timer.")
def reset(name):   
    """
    Resets a specified task timer to initial state.
    
    Clears all timing data while preserving the task's existence.
    Resets start time, end time, and accumulated time to zero.
    
    Parameters:\n
        - timer (str): Name of the task to reset\n
    
    Reset Actions:\n
        - Clears start_time, end_time, current_time\n
        - Resets pre_paused_time to zero\n
        - Maintains task name and existence\n
    
    Error Handling:\n
        - Validates task existence before reset\n
        - Provides feedback on reset operation status\n
    """
    task_list = load_tasks()
    task_names = [task.task_name for task in task_list]
    if name not in task_names:
        click.echo(f"{Fore.MAGENTA}{name}{Fore.RESET}{Fore.RED}{Fore.WHITE}:{Fore.RESET} Couldn't reset.{Fore.RESET}")
        return 
    
    for task in task_list:
        if task.task_name == name:
            task.start_time = None
            task.end_time = None
            task.current_time = 0
            task.pre_paused_time = 0

    save_tasks(task_list)
    click.echo(f"{Fore.MAGENTA}{name}{Fore.RESET}{Fore.WHITE}:{Fore.RESET}{Fore.GREEN} Successfully reset.{Fore.RESET}")

@main.command()
@click.option("--name", type=click.Choice([task.task_name for task in load_tasks()]), required=True, help="The name of the timer to edit.")
@click.option("-n", type=str, help="Use this when wanting to change name.")
@click.option("-t", type=int, help="Seconds to add use '-' value to subtract seconds. Must be toggled off!")
def edit(name, n, t):
    """
    Modifies properties of an existing task.
    
    Supports editing task names and adjusting accumulated time.
    Provides atomic operations for name changes and time adjustments.
    
    Parameters:\n
        - timer (str): Name of the task to edit\n
        - n (str, optional): New name for the task\n
        - t (int, optional): Time adjustment in seconds (positive to add, negative to subtract)
    
    Edit Operations:\n
        - Name Change: Updates task identifier while preventing duplicates\n
        - Time Adjustment: Modifies accumulated time while preserving task state\n
    
    Error Handling:\n
        - Prevents duplicate names during rename\n
        - Validates time adjustments\n
        - Ensures task is in appropriate state for editing\n
        - Provides detailed feedback on edit operations\n
    """
    task_list = load_tasks()
    task_name_list = [task.task_name for task in task_list]
    if n:
        for task in task_list:
            if task.task_name == name:
                if n in task_name_list:
                    return click.echo(f"{Fore.MAGENTA}{n}{Fore.RESET}{Fore.WHITE}:{Fore.RESET}{Fore.RED} Couldn't be Created due to the name being in use!{Fore.RESET}")
                old_name = task.task_name
                task.task_name = n
                click.echo(f"{Fore.MAGENTA}{task.task_name}{Fore.RESET}{Fore.WHITE}:{Fore.RESET}{Fore.GREEN} Successfully changed from {Fore.RESET}'{Fore.MAGENTA}{old_name}{Fore.RESET}'{Fore.RESET}")

    if t:
        for task in task_list:
            if task.task_name == name:
                if task.start_time is not None and task.status != "Active":
                    task.current_time = time.time()
                    
                    if task.end_time:
                        elapsed = task.end_time - task.start_time
                    else:
                        elapsed = task.current_time - task.start_time
                    
                    if t > 0:
                        elapsed += t
                        task.start_time = task.end_time - elapsed
                    else:
                        new_elapsed = max(0, elapsed + t)
                        task.start_time = task.end_time - new_elapsed
                        
                        if new_elapsed == 0:
                            click.echo(f"{Fore.MAGENTA}{task.task_name}{Fore.RESET}:{Fore.RESET}{Fore.GREEN} Timer set to {Fore.MAGENTA}0{Fore.RED} seconds.{Fore.RESET}")
                            continue
                        
                    if t >= 0:
                        click.echo(f"{Fore.MAGENTA}{task.task_name}{Fore.RESET}:{Fore.RESET}{Fore.GREEN} Successfully added {Fore.RESET}{Fore.MAGENTA}{t}{Fore.RESET} seconds.{Fore.RESET}")
                    else:
                        click.echo(f"{Fore.MAGENTA}{task.task_name}{Fore.RESET}:{Fore.RESET}{Fore.GREEN} Successfully subtracted {Fore.RESET}{Fore.MAGENTA}{t*-1}{Fore.RESET} seconds.{Fore.RESET}")
                else:
                    click.echo(f"{Fore.MAGENTA}{task.task_name}{Fore.RESET}:{Fore.RESET}{Fore.RED} time can't be edited {Fore.RESET}")
        save_tasks(task_list)


if __name__ == "__main__":
    main()
