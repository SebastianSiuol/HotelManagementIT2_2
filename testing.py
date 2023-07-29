import tkinter as tk

def hide_widget():
    label.grid_remove()

def show_widget():
    label.grid()

# Create the tkinter window
window = tk.Tk()
window.title("Hide Widgets Example")

# Create a label widget
label = tk.Label(window, text="This is a label.")
label.grid(row=0, column=0, pady=10)

# Create buttons to hide and show the label
hide_button = tk.Button(window, text="Hide Label", command=hide_widget)
hide_button.grid(row=1, column=0, pady=5)

show_button = tk.Button(window, text="Show Label", command=show_widget)
show_button.grid(row=1, column=1, pady=5)

# Start the tkinter main loop
window.mainloop()
