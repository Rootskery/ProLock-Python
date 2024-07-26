import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

# Function to add attendance
def add_attendance():
    student_name = student_name_entry.get()
    name = name_entry.get()
    date = date_entry.get()
    time_in = time_in_entry.get()
    time_out = time_out_entry.get()
    if not student_name or not name or not date or not time_in or not time_out:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    try:
        # Ensure the date is in the correct format
        datetime.strptime(date, "%Y-%m-%d")
        # Ensure the time format is correct
        datetime.strptime(time_in, "%H:%M")
        datetime.strptime(time_out, "%H:%M")
    except ValueError:
        messagebox.showerror("Error", "Date must be in YYYY-MM-DD format and Time must be in HH:MM format")
        return

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS attendance (student_name TEXT, name TEXT, date TEXT, time_in TEXT, time_out TEXT)')
    c.execute('INSERT INTO attendance (student_name, name, date, time_in, time_out) VALUES (?, ?, ?, ?, ?)', (student_name, name, date, time_in, time_out))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Attendance recorded successfully")
    student_name_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    time_in_entry.delete(0, tk.END)
    time_out_entry.delete(0, tk.END)

# Function to view attendance records
def view_attendance():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM attendance')
    records = c.fetchall()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)

    for record in records:
        tree.insert('', tk.END, values=record)

# Create the main window
root = tk.Tk()
root.title("Attendance Monitoring System")
root.geometry("800x400")

# Main frame to contain everything
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame for displaying the image
image_frame = tk.Frame(main_frame)
image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

# # Load and display an image
# try:
#     # Adjust the path to your image file
#     image_path = 'path/to/your/image.png'
#     image = Image.open(image_path)
#     image = image.resize((150, 150), Image.LANCZOS)  # Resize the image
#     photo = ImageTk.PhotoImage(image)
#     img_label = tk.Label(image_frame, image=photo)
#     img_label.image = photo  # Keep a reference to avoid garbage collection
#     img_label.pack()
# except Exception as e:
#     print(f"Error loading image: {e}")

# Frame to contain the input fields and the Treeview
content_frame = tk.Frame(main_frame)
content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Header label at the top of the content_frame
header = tk.Label(content_frame, text="Attendance Monitoring System", font=("Arial", 25, "bold"))
header.pack(pady=(0, 10), padx=10, fill=tk.X, anchor='center')

header = tk.Label(content_frame, text="Please Tap You ID!", font=("Arial", 18, "bold"))
header.pack(pady=(0, 10), padx=10, fill=tk.X, anchor='center')

# Create a frame for input fields and buttons
input_frame = tk.Frame(content_frame, borderwidth=2, relief="sunken")
input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

# Input fields
tk.Label(input_frame, text="Student Number:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
student_name_entry = tk.Entry(input_frame)
student_name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
name_entry = tk.Entry(input_frame)
name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
date_entry = tk.Entry(input_frame)
date_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Time In (HH:MM):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
time_in_entry = tk.Entry(input_frame)
time_in_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Time Out (HH:MM):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
time_out_entry = tk.Entry(input_frame)
time_out_entry.grid(row=4, column=1, padx=10, pady=5)

# # Buttons
# button_frame = tk.Frame(input_frame)
# button_frame.grid(row=5, columnspan=2, pady=10)
#
# tk.Button(button_frame, text="Add Attendance", command=add_attendance).pack(side=tk.LEFT, padx=5)
# tk.Button(button_frame, text="View Attendance", command=view_attendance).pack(side=tk.LEFT, padx=5)

# Create a frame for the Treeview
tree_frame = tk.Frame(content_frame, borderwidth=2, relief="sunken")
tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

# Define columns
columns = ('Name', 'Date')
tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
tree.heading('Name', text='Name')
tree.heading('Date', text='Date')

tree.pack(fill=tk.BOTH, expand=True)

# Start the Tkinter main loop
root.mainloop()
