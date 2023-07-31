from tkinter import *
number = 0

window = Tk()
window.title("Programme")
window.geometry('350x250')

label = Label(window, text=number)
label.grid(column=0,row=0)

def clicked():
    global number
    number += 1
    label.config(text=number)

button = Button(window, text="Push Me", command=clicked)
button.grid(column=1, row=2)

window.mainloop()