import tkinter as tk

def open_toplevel():
    top_level = tk.Toplevel(root)
    top_level.title("Toplevel Window")
    top_level.geometry("200x100")
    top_level.grab_set()  # This prevents interaction with the main window until the Toplevel is closed

def close_toplevel():
    top_level.grab_release()  # Release the grab, allowing interaction with the main window
    top_level.destroy()

root = tk.Tk()
root.title("Main Window")

button_open = tk.Button(root, text="Open Toplevel", command=open_toplevel)
button_open.pack(pady=20)

button_close = tk.Button(root, text="Close Toplevel", command=close_toplevel)
button_close.pack(pady=10)

root.mainloop()
