# Import the modules
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox
import subprocess

# Define the main window
window = tk.Tk()
window.title("BRL-CAD g-stl GUI")
window.geometry("800x600")

# Define the widgets
# A label to show the input file name
input_label = tk.Label(window, text="Input file:")
input_label.grid(row=0, column=0, sticky="w")

# A button to browse for the input file
def browse_input():
    # Get the input file name from the file dialog
    input_file = filedialog.askopenfilename(title="Select input file", filetypes=[("BRL-CAD files", "*.g")])
    # Update the input entry with the file name
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_file)

input_button = tk.Button(window, text="Browse", command=browse_input)
input_button.grid(row=0, column=2, sticky="w")

# An entry to show the input file name
input_entry = tk.Entry(window, width=50)
input_entry.grid(row=0, column=1, sticky="w")

# A label to show the output file name
output_label = tk.Label(window, text="Output file:")
output_label.grid(row=1, column=0, sticky="w")

# A button to browse for the output file
def browse_output():
    # Get the output file name from the file dialog
    output_file = filedialog.asksaveasfilename(title="Save output file", filetypes=[("STL files", "*.stl")])
    # Update the output entry with the file name
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_file)

output_button = tk.Button(window, text="Browse", command=browse_output)
output_button.grid(row=1, column=2, sticky="w")

# An entry to show the output file name
output_entry = tk.Entry(window, width=50)
output_entry.grid(row=1, column=1, sticky="w")

# A label to show the object name
object_label = tk.Label(window, text="Object name:")
object_label.grid(row=2, column=0, sticky="w")

# An entry to enter the object name
object_entry = tk.Entry(window, width=50)
object_entry.grid(row=2, column=1, sticky="w")

# A label to show the options
options_label = tk.Label(window, text="Options:")
options_label.grid(row=3, column=0, sticky="w")

# A frame to hold the options
options_frame = tk.Frame(window)
options_frame.grid(row=3, column=1, columnspan=2, sticky="w")

# A checkbox to select the binary output option
binary_var = tk.IntVar()
binary_check = tk.Checkbutton(options_frame, text="Binary output", variable=binary_var)
binary_check.grid(row=0, column=0, sticky="w")

# A checkbox to select the inches output option
inches_var = tk.IntVar()
inches_check = tk.Checkbutton(options_frame, text="Inches output", variable=inches_var)
inches_check.grid(row=0, column=1, sticky="w")

# A checkbox to select the marching cubes option
cubes_var = tk.IntVar()
cubes_check = tk.Checkbutton(options_frame, text="Marching cubes", variable=cubes_var)
cubes_check.grid(row=0, column=2, sticky="w")

# A label to show the distance tolerance
distance_label = tk.Label(options_frame, text="Distance tolerance:")
distance_label.grid(row=1, column=0, sticky="w")

# An entry to enter the distance tolerance
distance_entry = tk.Entry(options_frame, width=10)
distance_entry.grid(row=1, column=1, sticky="w")

# A label to show the absolute tolerance
absolute_label = tk.Label(options_frame, text="Absolute tolerance:")
absolute_label.grid(row=2, column=0, sticky="w")

# An entry to enter the absolute tolerance
absolute_entry = tk.Entry(options_frame, width=10)
absolute_entry.grid(row=2, column=1, sticky="w")

# A label to show the relative tolerance
relative_label = tk.Label(options_frame, text="Relative tolerance:")
relative_label.grid(row=3, column=0, sticky="w")

# An entry to enter the relative tolerance
relative_entry = tk.Entry(options_frame, width=10)
relative_entry.grid(row=3, column=1, sticky="w")

# A label to show the normal tolerance
normal_label = tk.Label(options_frame, text="Normal tolerance:")
normal_label.grid(row=4, column=0, sticky="w")

# An entry to enter the normal tolerance
normal_entry = tk.Entry(options_frame, width=10)
normal_entry.grid(row=4, column=1, sticky="w")

# A scrolled text to show the output messages
output_text = scrolledtext.ScrolledText(window, width=80, height=20)
output_text.grid(row=4, column=0, columnspan=3, sticky="w")

# A button to run the g-stl command
def run_gstl():
    # Get the input and output file names
    input_file = input_entry.get()
    output_file = output_entry.get()
    # Check if they are valid
    if not input_file or not output_file:
        messagebox.showerror("Error", "Please select valid input and output files.")
        return
    # Get the object name
    object_name = object_entry.get()
    # Check if it is valid
    if not object_name:
        messagebox.showerror("Error", "Please enter a valid object name.")
        return
    # Build the g-stl command
    command = ["g-stl", "-o", output_file]
    # Add the options
    if binary_var.get():
        command.append("-b")
    if inches_var.get():
        command.append("-i")
    if cubes_var.get():
        command.append("-8")
    if distance_entry.get():
        command.extend(["-D", distance_entry.get()])
    if absolute_entry.get():
        command.extend(["-a", absolute_entry.get()])
    if relative_entry.get():
        command.extend(["-r", relative_entry.get()])
    if normal_entry.get():
        command.extend(["-n", normal_entry.get()])
    # Add the input file and object name
    command.extend([input_file, object_name])
    # Run the command and capture the output
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
    # Decode the output and show it on the scrolled text
    output_text.delete(1.0, tk.END)
    output_text.insert(1.0, output.decode())

run_button = tk.Button(window, text="Run", command=run_gstl)
run_button.grid(row=5, column=0, sticky="w")

# Start the main loop
window.mainloop()
