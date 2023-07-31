import tkinter as tk
from tkinter import ttk


class MyApp:
    def __init__(self, root):
        self.root = root
        self.options = ["Option 1", "Option 2", "Option 3"]

        self.combobox = ttk.Combobox(root, values=self.options)
        self.combobox.set("Select an option")  # Set a default value

        self.combobox.pack()

        # Bind the event function to the <<ComboboxSelected>> event
        self.combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)

    def on_combobox_select(self, event):
        selected_item = self.combobox.get()
        print("Selected Item:", selected_item)


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
