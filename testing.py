import tkinter as tk
from tkinter import ttk

# Sample dictionary with data
data_dict = {
    "Option 1": 100,
    "Option 2": 200,
    "Option 3": 300,
}

# Create the Tkinter application window
root = tk.Tk()
root.title("ComboBox with Dictionary")

my_vars = tk.StringVar()

# Create a ComboBox and populate it with dictionary keys
combo = ttk.Combobox(root, values=list(data_dict.keys()), textvariable=my_vars)
combo.pack()

# Function to handle ComboBox selection
def on_selection(event):
    selected_key = combo.get()
    selected_value = data_dict.get(selected_key)
    print(f'This is current function: {combo.current()}')
    print(f'This is get function: {my_vars.get()}')


# Bind the ComboBox selection event to the function
combo.bind("<<ComboboxSelected>>", on_selection)

# Start the main event loop
root.mainloop()
