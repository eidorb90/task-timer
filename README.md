# Task Timer

A Python-based task timer application to help you efficiently manage and track time for multiple tasks. This tool is designed to improve productivity by providing real-time updates, easy-to-use CLI commands, and CSV-based persistence for tasks.

## Features

### **Commands**

1. **List**  
   Lists all active tasks with their name, status, and elapsed time.
   ```bash
   python __main__.py list
   ```

2. **Create**  
   Creates a new task. You can specify a name or let the program assign one.
   ```bash
   python __main__.py create --name <task_name>
   ```

3. **Toggle**  
   Toggles a task’s state:
   - **Off → Active**: Starts the task.
   - **Paused → Active**: Resumes the task.
   - **Active → Paused**: Pauses the task.
   ```bash
   python __main__.py toggle --name <task_name>
   ```

4. **Display**  
   Displays the real-time status and elapsed time for:
   - **All tasks**
   - **A specific task**  
   ```bash
   python __main__.py display --name <task_name>
   ```

5. **Delete**  
   Deletes a specific task.
   ```bash
   python __main__.py delete --name <task_name>
   ```

6. **Save**  
   Saves the current tasks to a specified CSV file (default: `tasks.csv`).
   ```bash
   python __main__.py save --filename <file_name>
   ```

7. **Load**  
   Loads tasks from a specified CSV file (default: `tasks.csv`).
   ```bash
   python __main__.py load --filename <file_name>
   ```

8. **Reset**  
   Resets the timer for a specific task to `0`.
   ```bash
   python __main__.py reset --timer <task_name>
   ```

---

## CSV File Structure

The tasks are saved in `tasks.csv` with the following fields:
- **Task Name**: The name of the task.
- **Status**: Current status (`Off`, `Active`, or `Paused`).
- **Time**: Elapsed time for the task in seconds.
- **Start Time**: Timestamp of when the task was started.
- **End Time**: Timestamp of when the task was stopped or paused.
- **Pre-pause Time**: The accumulated time before the task was paused.

---

## Notes

- Real-time display can be exited by pressing **'c'** and hitting **Enter**.
- Ensure the `tasks.csv` file is not open in another program while using the application.

---
