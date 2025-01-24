"""
old.py
Brodie Rogers <brodie.rogers@students.cune.edu>
2025-01-23

This is the task class that im using to create and manage tasks,
and their indicidual processes.
"""

import time

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
        self.current_time = 0
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
