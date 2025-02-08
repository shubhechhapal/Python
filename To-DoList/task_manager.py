import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to create/connect to database
def setup_database():
    conn = sqlite3.connect("tasks.db")  # Create database file
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        task TEXT, 
                        completed INTEGER)''')  # Create table
    conn.commit()
    conn.close()

# Function to add a task
def add_task():
    task = task_entry.get()
    if task.strip():
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, ?)", (task, 0))
        conn.commit()
        conn.close()
        task_listbox.insert(tk.END, task)  # Add to listbox
        task_entry.delete(0, tk.END)  # Clear input field
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

# Function to load tasks from database
def load_tasks():
    task_listbox.delete(0, tk.END)  # Clear listbox
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT task FROM tasks WHERE completed=0")  # Fetch only incomplete tasks
    tasks = cursor.fetchall()
    conn.close()
    for task in tasks:
        task_listbox.insert(tk.END, task[0])

# Function to delete selected task
def delete_task():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())  # Get selected task
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE task=?", (selected_task,))
        conn.commit()
        conn.close()
        load_tasks()  # Refresh list
    except:
        messagebox.showwarning("Warning", "Please select a task to delete!")

# Function to mark task as completed
def mark_completed():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())  # Get selected task
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed=1 WHERE task=?", (selected_task,))
        conn.commit()
        conn.close()
        load_tasks()  # Refresh list
    except:
        messagebox.showwarning("Warning", "Please select a task to mark as completed!")

# Initialize database
setup_database()

# Create main application window
root = tk.Tk()
root.title("Task Manager")
root.geometry("400x500")
root.config(bg="#f4f4f4")  # Light gray background

# UI Styling
font_style = ("Arial", 12)

# Task Entry Field
task_entry = tk.Entry(root, width=40, font=font_style, bd=2, relief="solid")
task_entry.pack(pady=10)

# Buttons Styling (without bg in the style)
button_style = {"font": font_style, "width": 20, "fg": "white", "bd": 2, "relief": "raised"}

# Create buttons with individual bg color
add_button = tk.Button(root, text="Add Task", command=add_task, bg="#4CAF50", **button_style)
add_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task, bg="red", **button_style)
delete_button.pack(pady=5)

complete_button = tk.Button(root, text="Mark as Completed", command=mark_completed, bg="blue", **button_style)
complete_button.pack(pady=5)

# Task Listbox Styling
task_listbox = tk.Listbox(root, width=50, height=10, font=font_style, bg="white", bd=2, relief="solid")
task_listbox.pack(pady=10)

# Load tasks on startup
load_tasks()

# Run the Tkinter event loop
root.mainloop()
