# **Brodie’s Task Timer**

A Python-based task timer application to help you manage and track time for multiple tasks efficiently. This program provides functionality to create, toggle, and display timers for tasks in real-time, making it an excellent tool for productivity and time management.

---

## **Features**
- **Task Management**: Create and manage multiple tasks with ease.
- **Time Tracking**: Start, pause, and resume timers for tasks.
- **Real-Time Display**: View live updates of task durations.

---

## **Getting Started**

### **Prerequisites**
- Python 3.7 or higher installed on your system.

### **Installation**
1. Clone or download the repository to your local machine:
   ```bash
   git clone https://github.com/eidorb90/task-timer
   ```
2. Navigate to the directory containing the script:
   ```bash
   cd task_timer
   ```

3. Run the program:
   ```bash
   python task_timer.py
   ```

---

## **How to Use**

### **Options**
1. **List**: Lists all active tasks with their name, status, and elapsed time.
2. **Create**: Creates a new task. You’ll be prompted to enter a task name.
3. **Toggle**: Toggles a task’s state between:
   - **Off → Active**: Starts the task.
   - **Paused → Active**: Resumes the task.
   - **Active → Paused**: Pauses the task.
4. **Display**: Displays the real-time status and time of:
   - **All Tasks**: Shows all active tasks.
   - **Specific Task**: Shows a specific task of your choosing.

### **Steps**
1. Run the script to see the menu options.
2. Enter the desired command (e.g., `list`, `create`, `toggle`, `display`).
3. Follow the prompts for task management.
4. Press **`c`** then hit **enter** to exit the real-time display view.


## **Example**

Here’s an example of how you might use the program:

1. Start the program:
   ```bash
   python task_timer.py
   ```

2. Create a new task:
   ```
   Options:
   List:   Lists out all of your timers.
   Create: Creates timer.
   Toggle: Toggles a timer on or off.
   Display: Displays live updates for your timer(s).

   create
   New Task Name: study
   ```

3. Toggle the task to start timing:
   ```
   toggle
   Task to toggle: study
   study: Started Successfully
   ```

4. Display all tasks in real time:
   ```
   display
   Tasks to display?('all' or 'task-name'): all
   ```

5. Exit real-time display by typing `c` and pressing Enter.

---

## **Known Limitations**
- Tasks cannot be deleted once created (future updates can add this functionality).
- Does not currently save tasks or time between sessions.

---

## **Future Enhancements**
- Add functionality to save and load tasks from a file.
- Include the ability to delete tasks.
- Improve UI with a graphical interface or web app integration.

---

## **Contributing**
Contributions are welcome! Feel free to submit issues or pull requests for enhancements and bug fixes.

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.

