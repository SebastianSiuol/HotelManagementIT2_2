import tkinter as tk

def get_selected_index():
    # Get the index of the selected item(s)
    selected_indices = listbox.curselection()

    # If no item is selected, return
    if not selected_indices:
        return

    # If you want to work with a single selection, you can directly use the first index
    index = selected_indices[0]

    # Do something with the index
    print("Selected index:", index)

# Create the tkinter window
root = tk.Tk()
root.title("Listbox Example")

# Create a Listbox and populate it with some items
listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=30)  # Set the width to make the scrollbar visible
listbox.pack()

items = ["Apple", "Banana", "Orange", "Grapes", "Watermelon", "Mangoqweqwewqewewqewqeqwewqeqweqw"]
for item in items:
    listbox.insert(tk.END, item)

# Create a horizontal scrollbar
x_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
x_scrollbar.pack(fill=tk.X)

# Link the Listbox and the scrollbar
listbox.config(xscrollcommand=x_scrollbar.set)
x_scrollbar.config(command=listbox.xview)

# Create a button to get the selected index
button = tk.Button(root, text="Get Selected Index", command=get_selected_index)
button.pack()

# Run the main event loop
root.mainloop()
