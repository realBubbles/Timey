import tkinter as tk
from tkinter import simpledialog
from datetime import datetime, timedelta

class Timey:
    def __init__(self, root):
        self.root = root
        self.root.title("Timey")

        self.tasks = {}
        self.current_task = None
        self.start_time = None
        self.timer_running = False

        self.add_task_button = tk.Button(root, text="Add a Task", command=self.add_task)
        self.add_task_button.pack()

        self.task_frame = tk.Frame(root)
        self.task_frame.pack()

    def add_task(self):
        task_name = simpledialog.askstring("Task", "Taskname:", parent=self.root)
        if task_name and task_name not in self.tasks:
            var = tk.IntVar()
            task_row = tk.Frame(self.task_frame)
            task_row.pack(anchor='w')

            cb = tk.Checkbutton(task_row, text=task_name, variable=var, command=lambda: self.toggle_task(task_name, var))
            cb.pack(side='left')

            time_label = tk.Label(task_row, text="00:00:00")
            time_label.pack(side='left')

            self.tasks[task_name] = {'button': cb, 'time': timedelta(0), 'var': var, 'label': time_label}

    def toggle_task(self, task_name, var):
        if var.get() == 1:
            # Checkbutton active
            if self.current_task and self.current_task != task_name:
                # Stop if another task is running
                self.stop_timer()
            self.current_task = task_name
            self.start_timer()
        else:
            # Checkbutton not active
            if self.current_task == task_name:
                self.stop_timer()
                self.current_task = None

    def start_timer(self):
        self.start_time = datetime.now()
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        if self.current_task:
            elapsed_time = datetime.now() - self.start_time
            self.tasks[self.current_task]['time'] += elapsed_time
            self.tasks[self.current_task]['label'].config(text=str(self.tasks[self.current_task]['time']).split('.')[0])
        self.timer_running = False

    def update_timer(self):
        if self.timer_running and self.current_task:
            elapsed_time = datetime.now() - self.start_time
            total_time = self.tasks[self.current_task]['time'] + elapsed_time
            self.tasks[self.current_task]['label'].config(text=str(total_time).split('.')[0])
            self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = Timey(root)
    root.mainloop()
