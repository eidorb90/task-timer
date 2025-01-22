import time 

class Task():
    def __init__(self, task_name):
        self.task_name = task_name
        self.task_len = 0
        self.start_time = None
        self.end_time = None
        self.current_time = None
        self.status = "Off"
        self.timer_time = None  

    def start(self):
        self.start_time = time.time()
        self.status = "Active"
        print(f"{self.task_name}: Started Successfully")
    
    def stop(self):
        self.end_time = time.time()
        self.task_len = self.start_time - self.end_time
        self.status = "Off"
        print(f"{self.task_name}: Stopped Successfully")

    def get_current_len(self):
        self.current_time = time.time()
        return self.start_time - self.current_time

    def __str__(self):
        self.current_time = time.time()

        if self.end_time != None:
            self.timer_time = self.end_time - self.start_time

            if self.end_time <= 60:
                self.timer_time = f"{self.end_time:.0f}"
            elif self.end_time > 60:
                mins = self.end_time // 60
                remainder = self.end_time % (mins * 60)
                self.timer_time = f"{mins:.0f}:{remainder:.0f}"

            return(f"Task : {self.task_name} | Status: {self.status} | Run Time : {self.timer_time}")   
        
        elif self.start_time != None:
            self.current_time = self.current_time - self.start_time

            if self.current_time <= 60:
                self.timer_time = f"{self.current_time:.0f}"
            elif self.current_time > 60:
                mins = self.current_time // 60
                remainder = self.current_time % (mins * 60)
                self.timer_time = f"{mins:.0f}:{remainder:.0f}"

            return(f"Task : {self.task_name} | Status: {self.status} | Run Time : {self.timer_time}")   
    
        else:
            return(f"Task : {self.task_name} | Status: {self.status} | Run Time : {self.timer_time}")
    

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
    
    elif user_command == "toggle":
        task_name = input("Task to toggle: ").lower()

        for task in task_list:

            if task.task_name == task_name:
                if task.status == "Off":
                    task.start()
                else: 
                    task.stop()
            else:
                print(f"'{task_name}' NOT VALID TASK NAME!!!")
    
    else: 
        print(f"'{user_command}' ISN'T A VALID COMMAND!!")