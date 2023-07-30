import tkinter as tk
from tkinter import ttk


def button():
    if my_string.get():
        print('the string is not empty')
    else:
        print('the string is empty')

root = tk.Tk()
root.geometry('400x200')
my_string = tk.StringVar()

ttk.Entry(root, textvariable=my_string).pack(expand=True, fill='both')
ttk.Button(root, text='Button', command=button).pack(expand=True, fill='both')

root.mainloop()
