"""
__main__.py
Brodie Rogers <brodie.rogers@students.cune.edu>
2025-01-22

A Python-based task timer application to help you manage and track time for multiple tasks efficiently. 
This program provides functionality to create, toggle, and display timers for tasks in real-time, making it an excellent tool for productivity and time management.
"""


import time
import os
import select
import sys

class Task():
    """
    A class to manage and track time for individual tasks.
    
    This class provides functionality to start, pause, resume, and monitor task durations.
    It handles time tracking with various states (Off, Active, Paused) and provides
    formatted time output.
    
    Attributes:
        task_name (str): The name of the task
        task_len (float): The total length of the task
        start_time (float): Unix timestamp when task was started
        end_time (float): Unix timestamp when task was ended/paused
        current_time (float): Current Unix timestamp for calculations
        status (str): Current status of the task ("Off", "Active", "Paused")
        pre_paused_time (float): Accumulated time before pauses
    
    Methods:
        start(): Initiates the task timer
        pause(): Temporarily stops the task timer
        resume(): Continues the task timer from where it was paused
        calc_time(start, end): Calculates and formats the elapsed time
        __str__(): Returns a string representation of the task's current state
    
    Example:
        task = Task("My Task")
        task.start()
        task.pause()
        task.resume()
        print(task)  # Output: My Task | Active | MM:SS
    """
    
    def __init__(self, task_name):
        """
        Initializes a Task instance with a name and sets all attributes to their default values.
        
        Parameters:
            task_name (str): The name of the task being created.
        """
        self.task_name = task_name
        self.task_len = 0
        self.start_time = None
        self.end_time = None
        self.current_time = None
        self.status = "Off"
        self.pre_paused_time = 0

    def start(self):
        """
        Starts the task timer by recording the current time as the start time.
        Sets the status of the task to 'Active'.
        """
        self.start_time = time.time()
        self.status = "Active"
        print(f"{self.task_name}: Started Successfully")
    
    def pause(self):
        """
        Pauses the task timer by recording the current time as the end time.
        The elapsed time before the pause is added to the pre-paused time.
        Sets the task status to 'Paused'.
        """
        self.end_time = time.time()
        self.pre_paused_time += self.end_time - (self.start_time + self.pre_paused_time)
        self.status = "Paused"
        print(f"{self.task_name}: Paused Successfully")

    def resume(self):
        """
        Resumes the task timer by resetting the start time and subtracting the pre-paused time.
        Sets the task status to 'Active'.
        """
        self.end_time = None
        self.start_time = time.time() - self.pre_paused_time
        self.status = "Active"
        print(f"{self.task_name}: Resumed Successfully")

    def calc_time(self, start, end):
        """
        Calculates and formats the elapsed time between a start time and an end time.
        
        Parameters:
            start (float): The start time of the task.
            end (float): The end time of the task.
        
        Returns:
            str: The formatted elapsed time as a string in HH:MM:SS or MM:SS format.
        """
        tot_time = end - start
        if tot_time <= 60:
            tot_time = f"{tot_time:.0f}"
        elif tot_time > 60 and tot_time < 3600:
            tot_time = time.strftime("%M:%S", time.gmtime(tot_time))
        elif tot_time >= 3600:
            tot_time = time.strftime("%H:%M:%S", time.gmtime(tot_time))
        return tot_time

    def __str__(self):
        """
        Returns a string representation of the task's current state, including task name, 
        status, and the formatted run time.
        
        Returns:
            str: A formatted string representing the task's status and run time.
        """
        self.current_time = time.time()

        if self.end_time is not None:
            timer_time = self.calc_time(self.start_time, self.end_time)
            return f"{self.task_name} | {self.status} | {timer_time}"
        
        elif self.start_time is not None:
            timer_time = self.calc_time(self.start_time, self.current_time)
            return f"{self.task_name} | {self.status} | {timer_time}"
    
        else:
            return f"{self.task_name} | {self.status} | {0}"

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

def show_options():
    """
    Displays the available commands for the user to interact with the task timer application.
    """
    print("")
    print("Options:")
    print("List:   Lists out all of your timers.")
    print("Create: Creates timer.")
    print("Toggle: Toggles a timer on or off.")
    print("Display: Displays live updates for your timer(s).")
    print("")

def list(task_list):
    """
    Lists all the current tasks with their names, statuses, and run times.
    If there are no tasks, it notifies the user to create one.
    """
    if len(task_list) == 0:
        print("No current tasks. Use the 'Create' command to create tasks.")

    print("")
    print("Task Name | Task Status | Task Time")
    for task in task_list:
        print(task)

def create():
    """
    Creates a new task by prompting the user for a name.
    Adds the new task to the task list and task name list.
    """
    task_name = input("New Task Name: ").lower()
    user_task = Task(task_name)
    task_list.append(user_task)
    task_name_list.append(user_task.task_name)

def toggle(task_list, task_name_list):
    """
    Toggles the state of a task (start, pause, resume) based on its current status.
    If the task does not exist, it notifies the user.
    """
    task_name = input("Task to toggle: ").lower()

    if task_name in task_name_list:
        for task in task_list:
            if task.task_name == task_name:
                if task.status == "Off":
                    task.start()
                elif task.status == "Paused":
                    task.resume()
                elif task.status == "Active" and task.start_time is not None:
                    task.pause()
    else:
        print(f"{task_name}: NOT A VALID TASK!!!")

def display(task_list, task_name_list):
    """
    Displays the status and run time of tasks in real-time.
    Provides the option to view all tasks or a specific task.
    Allows the user to exit the display loop by pressing 'c'.
    """
    display_tasks = True
    task_to_display = input("Tasks to display?('all' or 'task-name'): ").lower()

    if task_to_display == "all":
        """
        Displays all tasks in real-time, updating every second.
        """
        if len(task_list) == 0:
            print("No current tasks. Use the 'Create' command to create tasks.")

        print("")
        while display_tasks:
            clear_console()
            print("Enter 'c' to exit display:")
            print("Task Name | Task Status | Task Time")
            for task in task_list:
                print(task)
            user_input = non_blocking_input()
            try:
                if user_input.lower() == "c":
                    display_tasks = False
            except: 
                continue
            time.sleep(1)

    elif task_to_display in task_name_list:
        """
        Displays a specific task in real-time, updating every second.
        """
        print("")
        while display_tasks:
            clear_console()
            print("Enter 'c' to exit display (hint: you have to hit enter right away)")
            print("Task Name | Task Status | Task Time")
            for task in task_list:
                if task.task_name == task_to_display:
                    print(task)
            user_input = non_blocking_input()
            try:
                if user_input.lower() == "c":
                    display_tasks = False
            except: 
                continue
            time.sleep(1)

    else:
        print(f"{task_to_display}: NOT A VALID TASK!!!")

new_task = Task("test")


running = True
task_list = [new_task]
task_name_list = [new_task.task_name]

print("--------------------- Brodie's Task Timer --------------------- ")
while running:
    show_options()

    user_command = input("").lower()

    if user_command == "list":
        list(task_list)

    elif user_command == "create":
        create()
    
    elif user_command == "toggle":
        toggle(task_list, task_name_list)

    elif user_command == "display":
        display(task_list, task_name_list)
  
    else:
        """
        Displays an error message for invalid commands.
        """
        print(f"'{user_command}' ISN'T A VALID COMMAND!!")
