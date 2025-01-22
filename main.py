import time 
import os 
import select 
import sys

class Task():
    def __init__(self, task_name):
        self.task_name = task_name
        self.task_len = 0
        self.start_time = None
        self.end_time = None
        self.current_time = None
        self.status = "Off"
        self.pre_paused_time = 0

    def start(self):
        self.start_time = time.time()
        self.status = "Active"
        print(f"{self.task_name}: Started Successfully")
    
    # def stop(self):
    #     self.end_time = time.time()
    #     self.task_len = self.start_time - self.end_time
    #     self.status = "Off"
    #     print(f"{self.task_name}: Stopped Successfully")

    def pause(self):
        self.end_time = time.time()
        self.pre_paused_time += self.end_time - (self.start_time + self.pre_paused_time)
        self.status = "Paused"  
        print(f"{self.task_name}: Paused Successfully")

    def resume(self):
        self.end_time = None
        self.start_time = time.time() - self.pre_paused_time
        self.status = "Active"
        print(f"{self.task_name}: Resumed Successfully")

    def calc_time(self, start, end):
        tot_time = end - start
        if tot_time <= 60:
            tot_time = f"{tot_time:.0f}"  
        elif tot_time > 60 and tot_time < 3600:
            tot_time = time.strftime("%M:%S", time.gmtime(tot_time))  
        elif tot_time >= 3600:
            tot_time = time.strftime("%H:%M:%S", time.gmtime(tot_time))
        return tot_time

    def __str__(self):
        self.current_time = time.time()

        if self.end_time != None:
            timer_time = self.calc_time(self.start_time, self.end_time)
            return(f"{self.task_name} | {self.status} | {timer_time}")   
        
        elif self.start_time != None:
            timer_time = self.calc_time(self.start_time, self.current_time)
            return(f"{self.task_name} | {self.status} | {timer_time}")   
    
        else:
            return(f"{self.task_name} | {self.status} | {0}")
    

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def non_blocking_input():
    # This method is for Linux and Mac OS
    i, o, e = select.select([sys.stdin], [], [], 0.1)
    if i:
        return sys.stdin.readline().strip()
    else:
        return None

new_task = Task("test")

def show_options():
    print("")
    print("Options:")
    print("List:   Lists out all of your timers.")
    print("Create: Creates timer.")
    print("Toggle: Toggles a timer on or off.")
    print("")


running = True
task_list = [new_task]
task_name_list = [new_task.task_name]

print("--------------------- Brodie's Task Timer --------------------- ")
while running:
    show_options()

    user_command = input("").lower()

    if user_command == "list":
        if len(task_list) == 0:
            print("No current tasks. Use the 'Create' command to create tasks.")

        print("")
        print("Task Name | Task Status | Task Time")
        for task in task_list:
            print(task)

    elif user_command == "create":
        task_name = input("New Task Name: ").lower()
        user_task = Task(task_name)
        task_list.append(user_task)
        task_name_list.append(user_task.task_name)
    
    elif user_command == "toggle":
        task_name = input("Task to toggle: ").lower()

        if task_name in task_name_list:
            for task in task_list:
                if task.task_name == task_name:
                    if task.status == "Off":
                        task.start()
                    elif task.status == "Paused":
                        task.resume()
                    elif task.status == "Active" and task.start_time != None:
                        task.pause()
        else:
            print(f"{task_to_display}: NOT A VALID TASK!!!")

    elif user_command == "display":
        display_tasks = True
        task_to_display = input("Tasks to display?: ").lower()

        if task_to_display == "all":
            if len(task_list) == 0:
                print("No current tasks. Use the 'Create' command to create tasks.")

            print("")
            while display_tasks:
                clear_console()
                print("Enter 'c' to exit display (hint: you have to hit enter right away)")
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
            print("")
            while display_tasks:
                clear_console()
                print("Enter 'c' to exit display (hint: you have to hit enter right away)")
                print("Task Name | Task Status | Task Time")
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
  
    else: 
        print(f"'{user_command}' ISN'T A VALID COMMAND!!")  