# import tkinter as tk
# from tkinter import *
# from tkinter import ttk
#
# root_window = Tk()
# root_window.title('Hotel Management')
# root_window.geometry('640x480')
# tab_menu = ttk.Notebook(root_window)
#
# # Tab Menus Initialization
# guests_tab = Frame(tab_menu)
# rooms_tab = Frame(tab_menu)
# employees_tab = Frame(tab_menu)
# schedule_tab = Frame(tab_menu)
# # Tab Menus Initialization
# tab_menu.add(guests_tab, text='Guests')
# tab_menu.add(rooms_tab, text='Rooms')
# tab_menu.add(employees_tab, text='Employees')
# tab_menu.add(schedule_tab, text='Schedules')
# tab_menu.pack(expand=True, fill=BOTH)
# # Guest List and Label Initialization
# guests_list_frame = Frame(guests_tab, highlightbackground="gray", highlightthickness=1, pady=10, padx=10, relief=RAISED)
# guests_list_label = Label(guests_list_frame, text="Guests List", font="Arial")
# guest_lists = Listbox(guests_list_frame)
#
# guests_list_label.pack(side=TOP)
# guest_lists.pack(side=TOP, expand=True, fill=Y)
# guests_list_frame.pack(side=LEFT, fill=Y)
# # Guest Button Tools Initialization
# guest_tab_tools = Frame(guests_tab, highlightbackground="blue", highlightthickness=1, pady=10, padx=10, relief=RAISED)
# new_button = Button(guest_tab_tools, text='New')
# open_button = Button(guest_tab_tools, text='Open')
# modify_button = Button(guest_tab_tools, text='Modify')
# delete_button = Button(guest_tab_tools, text='Delete')
#
# new_button.pack(side=LEFT)
# open_button.pack(side=LEFT)
# modify_button.pack(side=LEFT)
# delete_button.pack(side=LEFT)
# guest_tab_tools.pack(side=TOP, fill=X)
#
# root_window.eval('tk::PlaceWindow . center')
# root_window.mainloop()
#
