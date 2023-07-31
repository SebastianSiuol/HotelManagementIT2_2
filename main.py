import datetime
import tkinter

import sql_connection
import re
import traceback
import tkinter as tk
from sql_connection import *
from tkinter import ttk
from tkinter.messagebox import *
from datetime import date, timedelta, datetime


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Hotel Management')
        # width x height
        self.geometry('1000x600')
        self.minsize(800, 600)

        self.tab_menu = HotelTabs(self)
        self.mainloop()


class HotelTabs(ttk.Notebook):
    def __init__(self, root):
        super().__init__(master=root)

        # Tabs
        self.guest_tab = GuestTab(self)
        self.room_tab = RoomTab(self)
        self.schedule_tab = ScheduleTab(self)
        self.employee_tab = EmployeeTab(self)
        self.billing_tab = BillingTab(self)
        self.job_tab = JobsTab(self)
        self.add(self.guest_tab, text='Guests')
        self.add(self.room_tab, text='Rooms')
        self.add(self.employee_tab, text='Employees')
        self.add(self.schedule_tab, text='Schedules')
        self.add(self.billing_tab, text='Bills')
        self.add(self.job_tab, text='Jobs')

        self.pack(expand=True, fill="both")


class GuestTab(ttk.Frame):
    def __init__(self, root):
        super().__init__(master=root)

        self.guests_treeview = None

        # Variables Initialization
        self.guest_id_variable = tk.StringVar()
        self.guest_firstname_variable = tk.StringVar()
        self.guest_lastname_variable = tk.StringVar()
        self.guest_email_variable = tk.StringVar()
        self.guest_phone_number_variable = tk.StringVar()
        self.guest_room_number_variable = tk.StringVar()
        self.guest_ongoing_payment_variable = tk.StringVar()

        self.guest_sql = GuestTabSQL()

        self.guest_id_entry = tk.Entry()
        self.guest_firstname_entry = tk.Entry()
        self.guest_lastname_entry = tk.Entry()
        self.guest_email_entry = tk.Entry()
        self.guest_phone_number_entry = tk.Entry()
        self.guest_room_number_entry = tk.Entry()

        self.guests_table(self).pack(side='left', fill='y')
        self.guests_widgets().pack(side='left', expand=True, fill='both')
        self.pack()

    def guests_table(self, frame):
        guests_table_frame = ttk.Frame(master=frame)
        guests_table_frame.configure(borderwidth=10, relief='groove')
        self.guests_treeview = ttk.Treeview(
            master=guests_table_frame,
            columns=('guest_id', 'fullname', 'room_assigned', 'check_in_out'),
            show='headings',
            selectmode='browse'
        )

        self.guests_treeview.heading('guest_id', text='Guest ID')
        self.guests_treeview.heading('fullname', text='Full Name')
        self.guests_treeview.heading('room_assigned', text='Room Assigned')
        self.guests_treeview.heading('check_in_out', text='Check In:Check Out')

        self.guests_treeview.column('guest_id', width=60)
        self.guests_treeview.column('fullname', width=120)
        self.guests_treeview.column('room_assigned', width=100)
        self.guests_treeview.column('check_in_out', width=150)

        self.guests_treeview.pack(expand=True, fill='both')
        self.populate_guests_list()
        return guests_table_frame

    def guests_widgets(self):
        widgets_frame = ttk.Frame(master=self)
        widgets_frame.configure(borderwidth=10, relief='groove')

        self.guests_buttons(widgets_frame).pack()
        self.guest_details(widgets_frame).pack()

        return widgets_frame

    def guests_buttons(self, frame):
        tools_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')

        tk.Button(
            tools_frame,
            text='New',
            command=self.new_guest_button
        ).pack(side='left', expand=True, fill='both', padx=2, )

        tk.Button(
            tools_frame,
            text='Open',
            command=self.open_guest_button
        ).pack(side='left', expand=True, fill='both', padx=2)
        tk.Button(tools_frame, text='Modify', command=self.modify_guest_button).pack(
            side='left', expand=True, fill='both', padx=2
        )
        tk.Button(tools_frame, text='Delete', command=self.delete_guest_button).pack(
            side='left', expand=True, fill='both', padx=2
        )
        tk.Button(tools_frame, text='Refresh', command=self.refresh_table_button).pack(
            side='left', expand=True, fill='both', padx=2
        )

        tools_frame.pack(fill='x')
        return tools_frame

    def guest_details(self, frame):
        guests_details_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')
        guests_details_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
        guests_details_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        # Labels for Guests Details
        tk.Label(guests_details_frame, text='Guest ID:').grid(row=0, column=0, sticky='nsew')
        tk.Label(guests_details_frame, text='First Name:').grid(row=1, column=0, sticky='nsew')
        tk.Label(guests_details_frame, text='Last Name:').grid(row=2, column=0, sticky='nsew')
        tk.Label(guests_details_frame, text='Email:').grid(row=3, column=0, sticky='nsew')
        tk.Label(guests_details_frame, text='Phone Number:').grid(row=4, column=0, sticky='nsew')
        tk.Label(guests_details_frame, text='Room Number:').grid(row=5, column=0, sticky='nsew')
        tk.Label(guests_details_frame, text='Ongoing Payment: ').grid(row=6, column=0, sticky='nsew')

        # Entries for Guest Details
        self.guest_id_entry = tk.Entry(
            guests_details_frame,
            textvariable=self.guest_id_variable,
            state='readonly'
        )
        self.guest_firstname_entry = tk.Entry(
            guests_details_frame,
            textvariable=self.guest_firstname_variable,
            state='readonly'
        )
        self.guest_lastname_entry = tk.Entry(
            guests_details_frame,
            textvariable=self.guest_lastname_variable,
            state='readonly'
        )
        self.guest_email_entry = tk.Entry(
            guests_details_frame,
            textvariable=self.guest_email_variable,
            state='readonly'
        )
        self.guest_phone_number_entry = tk.Entry(
            guests_details_frame,
            textvariable=self.guest_phone_number_variable,
            state='readonly'
        )
        self.guest_room_number_entry = tk.Entry(
            guests_details_frame,
            textvariable=self.guest_room_number_variable,
            state='readonly'
        )
        ttk.Label(
            guests_details_frame,
            textvariable=self.guest_ongoing_payment_variable,
            state='readonly'
        ).grid(row=6, column=1, sticky='ew')

        # Placing the Entries
        self.guest_id_entry.grid(row=0, column=1, sticky='ew')
        self.guest_firstname_entry.grid(row=1, column=1, sticky='ew')
        self.guest_lastname_entry.grid(row=2, column=1, sticky='ew')
        self.guest_email_entry.grid(row=3, column=1, sticky='ew')
        self.guest_phone_number_entry.grid(row=4, column=1, sticky='ew')
        self.guest_room_number_entry.grid(row=5, column=1, sticky='ew')

        guests_details_frame.pack(expand=True, fill='both')
        return guests_details_frame

    # Frames
    ##########################################################
    # Button Functions

    def new_guest_button(self):
        GuestCreationWindow(self)

    def open_guest_button(self):
        if not self.guests_treeview.focus():
            showwarning(title="Error!",
                        message='No guest is selected!')
        else:
            guest_index = self.guests_treeview.focus()
            selected_guest = self.guests_treeview.item(guest_index)
            selected_guest_id = selected_guest.get('values')[0]
            retrieved_guest = sql_connection.retrieve_a_guest(selected_guest_id)
            retrieved_guest_room = sql_connection.retrieve_guest_room(retrieved_guest[0])

            if sql_connection.check_if_guest_has_bill(selected_guest_id) == 1:
                guest_has_bill = 'Yes'
            else:
                guest_has_bill = 'No'

            self.guest_id_variable.set(retrieved_guest[0])
            self.guest_firstname_variable.set(retrieved_guest[1])
            self.guest_lastname_variable.set(retrieved_guest[2])
            self.guest_email_variable.set(retrieved_guest[3])
            self.guest_phone_number_variable.set(retrieved_guest[4])
            self.guest_room_number_variable.set(retrieved_guest_room)
            self.guest_ongoing_payment_variable.set(guest_has_bill)

    def modify_guest_button(self):
        if not self.guests_treeview.focus():
            showwarning(title="Error!",
                        message='No guest is selected!')
        else:
            guest_index = self.guests_treeview.focus()
            selected_guest = self.guests_treeview.item(guest_index)
            selected_guest_id = selected_guest.get('values')[0]
            selected_guest_name = selected_guest.get('values')[1]
            confirm_modify = askyesno(title="Modify?",
                                      message=f"You are about to modify {selected_guest_name}.\nContinue?")
            if confirm_modify:
                GuestModifyWindow(self, selected_guest_id)

    def delete_guest_button(self):
        if not self.guests_treeview.focus():
            showwarning(title="Error!",
                        message='No guest is selected!')
        else:
            guest_index = self.guests_treeview.focus()
            selected_guest = self.guests_treeview.item(guest_index)
            selected_guest_id = selected_guest.get('values')[0]
            retrieved_guest_room = sql_connection.retrieve_guest_room(selected_guest_id)

            confirm_delete = askyesno(title="Deletion!",
                                      message=f"You are deleting {selected_guest.get('values')[1]}.\nConfirm?")
            if confirm_delete:
                if sql_connection.check_if_guest_has_bill(selected_guest_id) == 1:
                    showwarning(title="Error!",
                                message='Cannot Delete!\nThis guest has ongoing payment!')
                else:
                    sql_connection.soft_delete_guest(selected_guest_id)
                    sql_connection.set_room_availability_after_guest_delete(retrieved_guest_room)
                    self.refresh_table_button()
                    self.clear_entries()

    def refresh_table_button(self):
        for item in self.guests_treeview.get_children():
            self.guests_treeview.delete(item)
        self.populate_guests_list()

    # Button Functions
    ##########################################################
    # Logics

    def populate_guests_list(self):
        guests = self.guest_sql.retrieve_guest_list_to_populate_table()
        for i in guests:
            if i[-1] == 0:
                self.guests_treeview.insert(
                    parent='',
                    index=tk.END,
                    iid=None,
                    values=(i[0], i[1], i[2], i[3])
                )

    def clear_entries(self):
        self.guest_id_variable.set("")
        self.guest_firstname_variable.set("")
        self.guest_lastname_variable.set("")
        self.guest_email_variable.set("")
        self.guest_phone_number_variable.set("")
        self.guest_room_number_variable.set("")
        self.guest_ongoing_payment_variable.set("")


class RoomTab(ttk.Frame):
    def __init__(self, root):
        super().__init__(master=root)

        self.rooms_widgets_frame = ttk.Frame()
        self.room_id_variable = tk.StringVar()
        self.room_number_variable = tk.StringVar()
        self.room_type_variable = tk.StringVar()
        self.room_price_variable = tk.StringVar()
        self.room_availability_variable = tk.StringVar()
        self.room_managed_by_variable = tk.StringVar()
        self.room_sql = RoomTabSQL()

        self.room_id_entry = tk.Entry()
        self.room_number_entry = tk.Entry()
        self.room_type_entry = tk.Entry()
        self.room_price_entry = tk.Entry()
        self.room_availability_entry = tk.Entry()
        self.room_sql = RoomTabSQL()

        self.rooms_treeview = None
        self.modify_frame = ttk.Frame()
        self.rooms_list(self).pack(side='left', expand=True, fill='both')
        self.rooms_widgets(self).pack(side='left', expand=True, fill='both')
        self.pack()

    def rooms_list(self, frame):
        rooms_table_frame = ttk.Frame(master=frame)
        rooms_table_frame.configure(borderwidth=10, relief='groove')
        self.rooms_treeview = ttk.Treeview(
            master=rooms_table_frame,
            columns=('room_id', 'room_number'),
            show='headings',
            selectmode='browse'
        )

        self.rooms_treeview.heading('room_id', text='Room ID')
        self.rooms_treeview.heading('room_number', text='Room Number')

        self.rooms_treeview.column('room_id', width=50)
        self.rooms_treeview.column('room_number', width=50)

        self.rooms_treeview.pack(expand=True, fill='both')

        self.populate_room_table()

        return rooms_table_frame

    def rooms_widgets(self, frame):
        self.rooms_widgets_frame = ttk.Frame(master=frame)
        self.rooms_widgets_frame.configure(borderwidth=10, relief='groove')

        self.rooms_buttons(self.rooms_widgets_frame).pack()
        self.rooms_details(self.rooms_widgets_frame).pack(expand=True, fill='both')

        return self.rooms_widgets_frame

    def rooms_buttons(self, frame):
        room_buttons_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')

        tk.Button(
            room_buttons_frame,
            text='New',
            command=self.new_room_button
        ).pack(side='left', expand=True, fill='both', padx=2, )

        tk.Button(
            room_buttons_frame,
            text='Open',
            command=self.open_room_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            room_buttons_frame,
            text='Modify',
            command=self.modify_room_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            room_buttons_frame,
            text='Delete',
            command=self.delete_room_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            room_buttons_frame,
            text='Refresh',
            command=self.refresh_room_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        room_buttons_frame.pack(fill='x')
        return room_buttons_frame
        pass

    def rooms_details(self, frame):
        """Labels and Entries that shows room details"""
        room_details_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')
        room_details_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        room_details_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')

        # Labels for Room
        tk.Label(room_details_frame, text='Room ID:').grid(row=0, columnspan=2, column=0, sticky='nsew')
        tk.Label(room_details_frame, text='Room Name:').grid(row=1, column=0, sticky='nsew')
        tk.Label(room_details_frame, text='Room Type:').grid(row=2, column=0, sticky='nsew')
        tk.Label(room_details_frame, text='Room Price:').grid(row=3, column=0, sticky='nsew')
        tk.Label(room_details_frame, text='Room Availability:').grid(row=4, column=0, sticky='nsew')
        tk.Label(room_details_frame, text='Managed by: ').grid(row=5, column=0, sticky='nsew')

        # Entries for Room
        self.room_id_entry = tk.Entry(
            room_details_frame,
            textvariable=self.room_id_variable,
            state='readonly'
        )

        self.room_number_entry = tk.Entry(
            room_details_frame,
            textvariable=self.room_number_variable,
            state='readonly'
        )

        self.room_type_entry = tk.Entry(
            room_details_frame,
            textvariable=self.room_type_variable,
            state='readonly'
        )

        self.room_price_entry = tk.Entry(
            room_details_frame,
            textvariable=self.room_price_variable,
            state='readonly'
        )

        self.room_availability_entry = tk.Entry(
            room_details_frame,
            textvariable=self.room_availability_variable,
            state='readonly'
        )

        tk.Label(
            room_details_frame,
            textvariable=self.room_managed_by_variable,
        ).grid(row=5, column=2, sticky='ew')

        # Placing Entries
        self.room_id_entry.grid(row=0, column=2, sticky='ew')
        self.room_number_entry.grid(row=1, column=2, sticky='ew')
        self.room_type_entry.grid(row=2, column=2, sticky='ew')
        self.room_price_entry.grid(row=3, column=2, sticky='ew')
        self.room_availability_entry.grid(row=4, column=2, sticky='ew')

        return room_details_frame

    def populate_room_table(self):
        all_rooms = sql_connection.retrieve_rooms_list()
        for i in all_rooms:
            if i[-1] == 0:
                self.rooms_treeview.insert(
                    parent='',
                    index=tk.END,
                    iid=None,
                    values=(i[0], i[1])
                )

    def new_room_button(self):
        RoomCreationWindow(self)

    def open_room_button(self):
        if not self.rooms_treeview.focus():
            showwarning(title="Error!",
                        message='No room is selected!')
        else:
            highlighted_room = self.rooms_treeview.focus()
            selected_room = self.rooms_treeview.item(highlighted_room)
            selected_room_id = selected_room.get('values')[0]
            retrieved_room = self.room_sql.retrieve_a_specific_room(selected_room_id)
            if retrieved_room[5] is None:
                employee_room_manager = "None"

            else:
                retrieved_employee = retrieve_an_employee(retrieved_room[5])
                employee_room_manager = f'{retrieved_employee[1]} {retrieved_employee[2]}'

            self.room_id_variable.set(retrieved_room[0])
            self.room_number_variable.set(retrieved_room[1])
            self.room_type_variable.set(retrieved_room[2])
            self.room_price_variable.set(retrieved_room[3])
            self.room_availability_variable.set(retrieved_room[4])
            self.room_managed_by_variable.set(employee_room_manager)

    def modify_room_button(self):
        if not self.rooms_treeview.focus():
            showwarning(title="Error!",
                        message='No room is selected!')
        else:
            highlighted_room = self.rooms_treeview.focus()
            selected_room = self.rooms_treeview.item(highlighted_room)
            selected_room_id = selected_room.get('values')[0]
            if self.room_sql.check_if_room_available(selected_room_id):
                RoomModificationWindow(self, selected_room_id)
            else:
                showwarning(title="Error!",
                            message='Cannot modify!\n'
                                    'Room is currently occupied or unavailable!')

    def delete_room_button(self):
        if not self.rooms_treeview.focus():
            showwarning(title="Error!",
                        message='No room is selected!')
        else:

            highlighted_room = self.rooms_treeview.focus()
            selected_room = self.rooms_treeview.item(highlighted_room)
            selected_room_id = selected_room.get('values')[0]
            confirm_delete = askyesno(title="Deletion!",
                                      message=f"You are deleting Room {selected_room.get('values')[1]}.\nConfirm?")
            if confirm_delete:
                if self.room_sql.check_if_room_available(selected_room_id):
                    self.room_sql.soft_delete_room(selected_room_id)
                    self.refresh_room_button()
                else:
                    showwarning(title="Error!",
                                message='Cannot Delete!\n'
                                        'Room is currently occupied or unavailable!')

    def refresh_room_button(self):
        for item in self.rooms_treeview.get_children():
            self.rooms_treeview.delete(item)
        self.populate_room_table()

        self.room_id_variable.set('')
        self.room_type_variable.set('')
        self.room_price_variable.set('')
        self.room_number_variable.set('')
        self.room_availability_variable.set('')
        self.room_managed_by_variable.set('')


class ScheduleTab(ttk.Frame):
    def __init__(self, root):
        super().__init__(master=root)

        # Entry Variables
        self.schedule_id_variable = tk.StringVar()
        self.schedule_start_date_variable = tk.StringVar()
        self.schedule_end_date_variable = tk.StringVar()
        self.schedule_availability_variable = tk.StringVar()

        #
        self.schedules = []

        # SQL Instance
        self.schedule_sql = ScheduleTabSQL()

        self.schedules_list = tk.Listbox
        self.schedule_table(self).pack(side='left', fill='both')
        self.schedule_widgets(self).pack(side='left', expand=True, fill='both')
        self.pack()

    def schedule_table(self, frame):
        schedule_list_frame = ttk.Frame(master=frame)
        schedule_list_frame.configure(borderwidth=10, relief='groove')

        # Label
        ttk.Label(
            schedule_list_frame,
            text='Schedules',
            font='Arial'
        ).pack(fill='x')

        # Schedule List
        schedule_list_items = tk.StringVar()
        self.schedules_list = tk.Listbox(
            schedule_list_frame,
            listvariable=schedule_list_items
        )
        self.populate_schedule_list()

        self.schedules_list.pack(expand=True, fill='both')
        return schedule_list_frame

    def schedule_widgets(self, frame):
        schedule_widgets_frame = ttk.Frame(master=frame)
        schedule_widgets_frame.configure(borderwidth=10, relief='groove')

        self.schedule_buttons(schedule_widgets_frame).pack(fill='x')
        self.schedule_details(schedule_widgets_frame).pack(expand=True, fill='both')
        return schedule_widgets_frame

    def schedule_buttons(self, frame):
        schedule_buttons_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')

        tk.Button(
            schedule_buttons_frame,
            text='New',
            command=self.new_schedule_button
        ).pack(side='left', expand=True, fill='both', padx=2, )

        tk.Button(
            schedule_buttons_frame,
            text='Open',
            command=self.open_schedule_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            schedule_buttons_frame,
            text='Modify',
            command=self.modify_schedule_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            schedule_buttons_frame,
            text='Delete',
            command=self.delete_schedule_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            schedule_buttons_frame,
            text='Refresh',
            command=self.refresh_schedule_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        schedule_buttons_frame.pack(fill='x')
        return schedule_buttons_frame

    def schedule_details(self, frame):
        schedule_details_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')
        schedule_details_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        schedule_details_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        # Labels for Schedule
        ttk.Label(schedule_details_frame, text="Schedule ID").grid(row=0, column=0, sticky='nsew')
        ttk.Label(schedule_details_frame, text="Start Date").grid(row=1, column=0, sticky='nsew')
        ttk.Label(schedule_details_frame, text="End Date").grid(row=2, column=0, sticky='nsew')
        ttk.Label(schedule_details_frame, text="Availability").grid(row=3, column=0, sticky='nsew')

        # Entries for Schedule
        ttk.Entry(
            schedule_details_frame,
            textvariable=self.schedule_id_variable,
            state='readonly'
        ).grid(row=0, column=1, sticky='ew')

        ttk.Entry(
            schedule_details_frame,
            textvariable=self.schedule_start_date_variable,
            state='readonly'
        ).grid(row=1, column=1, sticky='ew')

        ttk.Entry(
            schedule_details_frame,
            textvariable=self.schedule_end_date_variable,
            state='readonly'
        ).grid(row=2, column=1, sticky='ew')

        ttk.Entry(
            schedule_details_frame,
            textvariable=self.schedule_availability_variable,
            state='readonly'
        ).grid(row=3, column=1, sticky='ew')

        return schedule_details_frame

    def new_schedule_button(self):
        ScheduleCreationWindow(self)

    def open_schedule_button(self):
        if not self.schedules_list.curselection():
            showwarning("Error!", "No schedule selected!")
        else:
            selected_schedule_index = self.schedules_list.curselection()
            selected_schedule = self.schedules[selected_schedule_index[0]]
            self.schedule_id_variable.set(selected_schedule['id'])
            self.schedule_start_date_variable.set(selected_schedule['start_date'])
            self.schedule_end_date_variable.set(selected_schedule['end_date'])
            self.schedule_availability_variable.set(selected_schedule['availability'])

    def modify_schedule_button(self):
        if not self.schedules_list.curselection():
            showwarning("Error!", "No schedule selected!")
        else:
            selected_schedule_index = self.schedules_list.curselection()
            selected_schedule = self.schedules[selected_schedule_index[0]]
            ScheduleModificationWindow(self, selected_schedule['id'])

    def delete_schedule_button(self):
        if not self.schedules_list.curselection():
            showwarning("Error!", "No schedule selected!")
        else:
            selected_schedule_index = self.schedules_list.curselection()
            selected_schedule = self.schedules[selected_schedule_index[0]]
            confirm_delete = askyesno(title="Delete schedule?",
                                      message=f"You are deleting schedule ID: {selected_schedule['id']}.\n"
                                              f"Confirm?")
            if confirm_delete:
                confirm_hard_delete = askyesno(
                    title="Delete schedule?",
                    message=f"Schedule ID:{selected_schedule['id']} will be deleted permanently\n"
                            f"Are you sure?")
                if confirm_hard_delete:
                    self.schedule_sql.hard_delete_a_schedule(selected_schedule['id'])

    def refresh_schedule_button(self):
        self.schedules_list.delete(0, 'end')
        self.schedules.clear()
        self.populate_schedule_list()

    def populate_schedule_list(self):
        """Populate the combo box of schedules"""
        all_schedules = self.schedule_sql.retrieve_all_schedule()

        for i in all_schedules:
            schedules_details = {"id": i[0],
                                 "start_date": i[1],
                                 "end_date": i[2],
                                 "availability": i[3]}

            self.schedules.append(schedules_details)

        for items in self.schedules:
            self.schedules_list.insert(tk.END, items['start_date'])


class EmployeeTab(ttk.Frame):
    def __init__(self, root):
        super().__init__(master=root)

        self.manager_name_label = tk.Label()
        self.job_position = None
        self.employee_treeview = None

        # Entry Tkinter Variables
        self.room_entry = None
        self.employee_phone_entry = None
        self.employee_email_entry = None
        self.employee_last_name_entry = None
        self.employee_first_name_entry = None
        self.employee_id_entry = None

        # StringVars
        self.manager_id_variable = tk.IntVar()
        self.employee_job_position_variable = tk.StringVar()
        self.employee_phone_number_variable = tk.StringVar()
        self.employee_email_variable = tk.StringVar()
        self.employee_lastname_variable = tk.StringVar()
        self.employee_firstname_variable = tk.StringVar()
        self.employee_id_variable = tk.StringVar()
        self.manager_name_variable = tk.StringVar()

        self.employee_sql = EmployeeTabSQL()

        self.employee_table(self).pack(side='left', expand=True, fill='both')
        self.employee_widgets(self).pack(side='left', expand=True, fill='both')
        self.pack()

    def employee_table(self, frame):
        employee_table_frame = ttk.Frame(master=frame)
        employee_table_frame.configure(borderwidth=10, relief='groove')
        self.employee_treeview = ttk.Treeview(
            master=employee_table_frame,
            columns=('employee_id', 'full_name', 'job_title'),
            show='headings',
            selectmode='browse'
        )

        self.employee_treeview.heading('employee_id', text='Employee ID')
        self.employee_treeview.heading('full_name', text='Full Name')
        self.employee_treeview.heading('job_title', text='Job Title')

        self.employee_treeview.column('employee_id', width=120)
        self.employee_treeview.column('full_name', width=120)
        self.employee_treeview.column('job_title', width=120)

        self.employee_treeview.pack(expand=True, fill='both')

        self.populate_employee_list()
        return employee_table_frame

    def employee_widgets(self, frame):
        employee_widgets_frame = ttk.Frame(master=frame)
        employee_widgets_frame.configure(borderwidth=10, relief='groove')

        self.employee_buttons(employee_widgets_frame).pack()
        self.employee_details(employee_widgets_frame).pack(expand=True, fill='both')

        return employee_widgets_frame

    def employee_buttons(self, frame):
        employee_buttons_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')

        tk.Button(
            employee_buttons_frame,
            text='New',
            command=self.new_employee_button
        ).pack(side='left', expand=True, fill='both', padx=2, )

        tk.Button(
            employee_buttons_frame,
            text='Open',
            command=self.open_employee_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            employee_buttons_frame,
            text='Modify',
            command=self.modify_employee_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            employee_buttons_frame,
            text='Delete',
            command=self.delete_employee_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            employee_buttons_frame,
            text='Refresh',
            command=self.refresh_employee_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            employee_buttons_frame,
            text='Assign Schedule',
            command=self.assign_schedule_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        employee_buttons_frame.pack(fill='x')
        return employee_buttons_frame

    def employee_details(self, frame):
        employee_details_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')
        employee_details_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        employee_details_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        # Labels for Employ
        tk.Label(employee_details_frame, text='Employee ID:').grid(row=0, columnspan=2, column=0, sticky='nsew')
        tk.Label(employee_details_frame, text='First Name:').grid(row=1, column=0, sticky='nsew')
        tk.Label(employee_details_frame, text='Last Name:').grid(row=2, column=0, sticky='nsew')
        tk.Label(employee_details_frame, text='Email:').grid(row=3, column=0, sticky='nsew')
        tk.Label(employee_details_frame, text='Phone Number:').grid(row=4, column=0, sticky='nsew')
        tk.Label(employee_details_frame, text='Job Position: ').grid(row=5, column=0, sticky='nsew')
        tk.Label(employee_details_frame, text='Manager: ').grid(row=6, column=0, sticky='nsew')

        self.employee_id_entry = tk.Entry(
            employee_details_frame,
            textvariable=self.employee_id_variable,
            state='disabled'
        )
        self.employee_first_name_entry = tk.Entry(
            employee_details_frame,
            textvariable=self.employee_firstname_variable
        )
        self.employee_last_name_entry = tk.Entry(
            employee_details_frame,
            textvariable=self.employee_lastname_variable
        )
        self.employee_email_entry = tk.Entry(
            employee_details_frame,
            textvariable=self.employee_email_variable
        )
        self.employee_phone_entry = tk.Entry(
            employee_details_frame,
            textvariable=self.employee_phone_number_variable
        )
        self.job_position = tk.Label(
            employee_details_frame,
            textvariable=self.employee_job_position_variable
        )
        self.manager_name_label = tk.Label(
            employee_details_frame,
            textvariable=self.manager_name_variable
        )

        # Placing the Entries/Texts
        self.employee_id_entry.grid(row=0, column=2, sticky='ew')
        self.employee_first_name_entry.grid(row=1, columnspan=2, column=2, sticky='ew')
        self.employee_last_name_entry.grid(row=2, columnspan=2, column=2, sticky='ew')
        self.employee_email_entry.grid(row=3, columnspan=2, column=2, sticky='ew')
        self.employee_phone_entry.grid(row=4, columnspan=2, column=2, sticky='ew')
        self.job_position.grid(row=5, columnspan=2, column=2, sticky='ew')
        self.manager_name_label.grid(row=6, columnspan=2, column=2, sticky='ew')

        return employee_details_frame

    def populate_employee_list(self):
        employees = self.employee_sql.retrieve_employees_to_populate_list()
        for i in employees:
            if i[-1] == 0:
                self.employee_treeview.insert(
                    parent='',
                    index=tk.END,
                    iid=None,
                    values=(i[0], i[1], i[2])
                )

    def new_employee_button(self):
        EmployeeCreationWindow(self)

    def open_employee_button(self):
        if not self.employee_treeview.focus():
            showwarning(title="Error!",
                        message='No Employee is selected!')
        else:
            highlighted_employee = self.employee_treeview.focus()
            selected_employee = self.employee_treeview.item(highlighted_employee)
            selected_employee_id = selected_employee.get('values')[0]
            retrieved_employee = self.employee_sql.retrieve_a_specific_employee(selected_employee_id)

            print(retrieved_employee)

            self.employee_id_variable.set(retrieved_employee[0])
            self.employee_firstname_variable.set(retrieved_employee[1])
            self.employee_lastname_variable.set(retrieved_employee[2])
            self.employee_email_variable.set(retrieved_employee[3])
            self.employee_phone_number_variable.set(retrieved_employee[4])
            self.employee_job_position_variable.set(retrieved_employee[5])
            self.manager_id_variable.set(retrieved_employee[6])

            if retrieved_employee[6] is None:
                self.manager_name_variable.set('No Manager')
            else:
                manager_name = self.employee_sql.retrieve_a_manager(self.manager_id_variable.get())
                self.manager_name_variable.set(manager_name[0])

    def modify_employee_button(self):
        if not self.employee_treeview.focus():
            showwarning(title="Error!",
                        message='No Employee is selected!')
        else:
            employee_index = self.employee_treeview.focus()
            selected_employee = self.employee_treeview.item(employee_index)
            selected_employee_id = selected_employee.get('values')[0]
            selected_employee_name = (selected_employee.get('values')[1]).split(" ")
            confirm_modify = askyesno(title="Modify?",
                                      message=f"You are about to modify {selected_employee_name[0]}'s information"
                                              f".\nContinue?")
            if confirm_modify:
                EmployeeModificationWindow(self, selected_employee_id)

    def refresh_employee_button(self):
        for item in self.employee_treeview.get_children():
            self.employee_treeview.delete(item)
        self.populate_employee_list()

        self.manager_id_variable = tk.IntVar()
        self.employee_job_position_variable.set('')
        self.employee_phone_number_variable.set('')
        self.employee_email_variable.set('')
        self.employee_lastname_variable.set('')
        self.employee_firstname_variable.set('')
        self.employee_id_variable.set('')
        self.manager_name_variable.set('')

    def delete_employee_button(self):
        if not self.employee_treeview.focus():
            showwarning(title="Error!",
                        message='No Employee is selected!')
        else:
            employee_index = self.employee_treeview.focus()
            selected_employee = self.employee_treeview.item(employee_index)
            selected_employee_id = selected_employee.get('values')[0]
            selected_employee_name = (selected_employee.get('values')[1]).split(" ")
            confirm_delete = askyesno(title="Delete?",
                                      message=f"You are about to delete {selected_employee_name[0]}"
                                              f".\nContinue?")
            if confirm_delete:
                if self.employee_sql.check_if_employee_still_manages(selected_employee_id):
                    showwarning(title="Error!",
                                message='Employee is managing other employees!\nCannot delete!')
                else:
                    self.employee_sql.soft_delete_an_employee(selected_employee_id)

    def assign_schedule_button(self):
        if not self.employee_treeview.focus():
            showwarning(title="Error!",
                        message='No Employee is selected!')
        else:
            pass


class BillingTab(ttk.Frame):
    def __init__(self, root):
        super().__init__(master=root)

        self.bills_treeview = ttk.Treeview()

        self.bills_id_variable = tk.IntVar()
        self.bills_guest_variable = tk.StringVar()
        self.bills_total_price_variable = tk.StringVar()
        self.bills_payment_info_variable = tk.StringVar()

        self.bills_sql = BillTabSQL()

        self.bills_table(self).pack(side='left', expand=True, fill='both')
        self.bills_widgets(self).pack(side='left', expand=True, fill='both')
        self.pack()

    def bills_table(self, frame):
        bills_table_frame = ttk.Frame(master=frame)
        bills_table_frame.configure(borderwidth=10, relief='groove')

        self.bills_treeview = ttk.Treeview(
            master=bills_table_frame,
            columns=('bill_id', 'guest_name', 'total_price'),
            show='headings',
            selectmode='browse',
            height=50
        )

        self.bills_treeview.heading('bill_id', text='Bill ID')
        self.bills_treeview.heading('guest_name', text='Guest Name')
        self.bills_treeview.heading('total_price', text='Total Price')

        self.bills_treeview.column('bill_id', width=50)
        self.bills_treeview.column('guest_name', width=50)
        self.bills_treeview.column('total_price', width=50)

        self.populate_bill_list()
        self.bills_treeview.pack(expand=True, fill='both')
        return bills_table_frame

    def bills_widgets(self, frame):
        bills_widgets_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')

        self.bills_buttons(bills_widgets_frame).pack()
        self.bills_details(bills_widgets_frame).pack(expand=True, fill='both')

        return bills_widgets_frame

    def bills_buttons(self, frame):
        bills_buttons_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')

        tk.Button(
            bills_buttons_frame,
            text='Open',
            command=self.open_bills_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            bills_buttons_frame,
            text='Process',
            command=self.pay_bills_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            bills_buttons_frame,
            text='Refresh',
            command=self.refresh_bills_table
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            bills_buttons_frame,
            text='Assign Employee',
            command=self.assign_employee_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        bills_buttons_frame.pack(fill='x')

        return bills_buttons_frame

    def bills_details(self, frame):
        bills_details_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')
        bills_details_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        bills_details_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        # Labels containing what are the information for the bill
        ttk.Label(bills_details_frame, text="Bill ID:").grid(row=0, column=0, sticky='nsew')
        ttk.Label(bills_details_frame, text="Guest Name:").grid(row=1, column=0, sticky='nsew')
        ttk.Label(bills_details_frame, text="Bill Total:").grid(row=2, column=0, sticky='nsew')
        ttk.Label(bills_details_frame, text="Guest Payment Info:").grid(row=3, column=0, sticky='nsew')

        # Labels containing what are information shown
        ttk.Label(
            bills_details_frame,
            textvariable=self.bills_id_variable
        ).grid(row=0, column=1, sticky='nsew')

        ttk.Label(
            bills_details_frame,
            textvariable=self.bills_guest_variable
        ).grid(row=1, column=1, sticky='nsew')

        ttk.Label(
            bills_details_frame,
            textvariable=self.bills_total_price_variable
        ).grid(row=2, column=1, sticky='nsew')

        ttk.Label(
            bills_details_frame,
            textvariable=self.bills_payment_info_variable
        ).grid(row=3, column=1, sticky='nsew')

        return bills_details_frame

    # Frames
    ##########################################################
    # Button Functions

    def open_bills_button(self):
        if not self.bills_treeview.focus():
            showwarning(title="Error!",
                        message='No Bill is selected!')
        else:
            bills_index = self.bills_treeview.focus()
            selected_bill = self.bills_treeview.item(bills_index)
            selected_bill_id = selected_bill.get('values')[0]
            retrieved_bill = sql_connection.retrieve_a_bill_and_guest(selected_bill_id)

            self.bills_id_variable.set(retrieved_bill[0])
            self.bills_guest_variable.set(retrieved_bill[1])
            self.bills_total_price_variable.set(retrieved_bill[2])
            self.bills_payment_info_variable.set(retrieved_bill[3])

    def pay_bills_button(self):
        if not self.bills_treeview.focus():
            showwarning(title="Error!",
                        message='No Bill is selected!')
        else:
            bills_index = self.bills_treeview.focus()
            selected_bill = self.bills_treeview.item(bills_index)
            selected_bill_id = selected_bill.get('values')[0]
            selected_bill_guest = selected_bill.get('values')[1]
            if self.check_if_bill_has_employee(selected_bill_id):
                confirm_pay = askyesno(title="Process the bill?",
                                       message=f"{selected_bill_guest}'s bill is about to be paid.\nConfirm?")
                if confirm_pay:
                    self.bills_sql.pay_bills(selected_bill_id)
                    self.refresh_bills_table()
            else:
                showwarning(title="Error!",
                            message='Selected bill should have an employee before procesing!')

    def refresh_bills_table(self):
        for item in self.bills_treeview.get_children():
            self.bills_treeview.delete(item)
        self.populate_bill_list()

    def assign_employee_button(self):
        if not self.bills_treeview.focus():
            showwarning(title="Error!",
                        message='No Bill is selected!')
        else:
            bills_index = self.bills_treeview.focus()
            selected_bill = self.bills_treeview.item(bills_index)
            selected_bill_id = selected_bill.get('values')[0]
            selected_bill_guest = selected_bill.get('values')[1]
            AssignEmployeeToBill(self, selected_bill_id)

    # Button Functions
    ##########################################################
    # Logics

    def populate_bill_list(self):
        bill_items = sql_connection.retrieve_bills_and_guest()
        for i in bill_items:
            if i[-1] == 1:
                self.bills_treeview.insert(
                    parent='',
                    index=tk.END,
                    iid=None,
                    values=(i[0], i[1], i[2])
                )

    def check_if_bill_has_employee(self, bill_id):
        if self.bills_sql.does_bill_have_employee(bill_id):
            return True
        else:
            return False



class JobsTab(ttk.Frame):
    def __init__(self, root):
        super().__init__(master=root)

        self.jobs_id_variable = tk.IntVar()
        self.jobs_title_variable = tk.StringVar()
        self.jobs_department_variable = tk.StringVar()

        self.jobs_treeview = ttk.Treeview()
        self.jobs_treeview_variables = tk.StringVar()

        self.jobs_sql = JobsTabSQL()

        self.jobs_table().pack(side='left', expand=True, fill='both')
        self.jobs_widgets().pack(side='left', expand=True, fill='both')
        self.pack()

    def jobs_table(self):
        jobs_table_frame = ttk.Frame(self)
        jobs_table_frame.configure(borderwidth=10, relief='groove')

        self.jobs_treeview = ttk.Treeview(
            master=jobs_table_frame,
            columns=('job_id', 'job_title', 'job_department'),
            show='headings',
            selectmode='browse'
        )
        self.jobs_treeview.heading('job_id', text='Job ID')
        self.jobs_treeview.heading('job_title', text='Job Title')
        self.jobs_treeview.heading('job_department', text='Job Department')

        self.jobs_treeview.column('job_id', width=20)
        self.jobs_treeview.column('job_title', width=20)
        self.jobs_treeview.column('job_department', width=20)

        self.jobs_treeview.pack(expand=True, fill='both')
        self.populate_jobs_table()
        return jobs_table_frame

    def jobs_widgets(self):
        jobs_widgets_container_frame = ttk.Frame(self)
        jobs_widgets_container_frame.configure(borderwidth=10, relief='groove')

        self.jobs_buttons().pack(fill='x')
        self.jobs_details().pack(expand=True, fill='both')

        return jobs_widgets_container_frame

    def jobs_buttons(self):
        jobs_widgets_container_frame = ttk.Frame(self)
        jobs_widgets_container_frame.configure(borderwidth=10, relief='groove')

        tk.Button(
            jobs_widgets_container_frame,
            text='New',
            command=self.new_jobs_button
        ).pack(side='left', expand=True, fill='both', padx=2, )

        tk.Button(
            jobs_widgets_container_frame,
            text='Open',
            command=self.open_jobs_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            jobs_widgets_container_frame,
            text='Modify',
            command=self.modify_jobs_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            jobs_widgets_container_frame,
            text='Delete',
            command=self.delete_jobs_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        tk.Button(
            jobs_widgets_container_frame,
            text='Refresh',
            command=self.refresh_jobs_button
        ).pack(side='left', expand=True, fill='both', padx=2)

        return jobs_widgets_container_frame

    def jobs_details(self):
        jobs_details_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        jobs_details_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        jobs_details_frame.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')

        ttk.Label(jobs_details_frame, text="Job ID:").grid(row=0, column=0, sticky='nsew')
        ttk.Label(jobs_details_frame, text="Job Title:").grid(row=1, column=0, sticky='nsew')
        ttk.Label(jobs_details_frame, text="Job Department:").grid(row=2, column=0, sticky='nsew')

        ttk.Entry(
            jobs_details_frame,
            textvariable=self.jobs_id_variable,
            state='readonly'
        ).grid(row=0, column=1, sticky='ew')

        ttk.Entry(
            jobs_details_frame,
            textvariable=self.jobs_title_variable,
            state='readonly'
        ).grid(row=1, column=1, sticky='ew')

        ttk.Entry(
            jobs_details_frame,
            textvariable=self.jobs_department_variable,
            state='readonly'
        ).grid(row=2, column=1, sticky='ew')

        return jobs_details_frame

    # Widgets
    ##########################################################
    # Button Functions

    def new_jobs_button(self):
        JobsCreationWindow(self)

    def open_jobs_button(self):
        self.populate_jobs_table()

    def modify_jobs_button(self):
        pass

    def delete_jobs_button(self):
        if not self.jobs_treeview.focus():
            showwarning(title="Error!",
                        message='No room is selected!')
        else:

            highlighted_jobs = self.jobs_treeview.focus()
            selected_jobs = self.jobs_treeview.item(highlighted_jobs)
            selected_jobs_id = selected_jobs.get('values')[0]
            confirm_delete = askyesno(title="Warning!",
                                      message=f"You are about to delete Job: {selected_jobs.get('values')[1]}."
                                              f"\nConfirm?")
            if confirm_delete:
                if selected_jobs_id == 4:
                    showerror(title="Error!",
                              message='The manager job cannot be deleted!')
                else:
                    if self.jobs_sql.check_if_job_is_referenced(selected_jobs_id):
                        showerror(title="Error!",
                                  message='The selected job is still being used!\nCannot delete!')
                    else:
                        confirm_hard_delete = askyesno(title="Warning!",
                                                       message=f"You are about to permanently "
                                                               f"delete the Job: {selected_jobs.get('values')[1]}."
                                                               f"\nContinue?")
                        if confirm_hard_delete:
                            self.jobs_sql.hard_delete_job(selected_jobs_id)

    def refresh_jobs_button(self):
        for job in self.jobs_treeview.get_children():
            self.jobs_treeview.delete(job)
        self.populate_jobs_table()

    # Button Functions
    ##########################################################
    # Logics

    def populate_jobs_table(self):
        all_retrieved_jobs = self.jobs_sql.retrieve_all_jobs()
        for jobs in all_retrieved_jobs:
            self.jobs_treeview.insert(
                parent='',
                index=tk.END,
                iid=None,
                values=(jobs[0], jobs[1], jobs[2])
            )


class GuestCreationWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        self.geometry('500x200')
        self.minsize(400, 200)

        self.title('Create new guest')

        # Basic Guest Information Variables
        self.firstname_variable = tk.StringVar()
        self.lastname_variable = tk.StringVar()
        self.email_variable = tk.StringVar()
        self.phone_number_variable = tk.StringVar()
        self.payment_method_variable = tk.StringVar()
        self.fullname_variable = tk.StringVar()

        # Room Variables
        self.rooms_variable = tk.StringVar()
        self.rooms_id_variable = tk.IntVar()
        self.rooms_name_variable = tk.StringVar()
        self.rooms_type_variable = tk.StringVar()
        self.rooms_price_variable = tk.StringVar()
        self.rooms_total_price_variable = tk.IntVar()

        # Check-in/out Variables
        self.check_in_date_variable = tk.StringVar()
        self.check_out_date_variable = tk.StringVar()
        self.check_in_year_variable = tk.StringVar()
        self.check_in_month_variable = tk.StringVar()
        self.check_in_day_variable = tk.StringVar()
        self.check_out_year_variable = tk.StringVar()
        self.check_out_month_variable = tk.StringVar()
        self.check_out_day_variable = tk.StringVar()

        self.rooms = []
        self.select_type_guest = ttk.Combobox()
        self.select_number_of_guest = ttk.Combobox()
        self.select_rooms_list = ttk.Combobox()

        self.create_a_guest_sql = CreateAGuest()

        self.guest_type = tk.StringVar()
        self.guest_numbers = tk.IntVar()
        self.current_frame = ttk.Frame()

        self.create_basic_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

        self.grab_set()

    def create_basic_information_frame(self):
        """First Frame"""
        basic_info_creation_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        basic_info_creation_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
        basic_info_creation_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, uniform='a')

        # Labels
        ttk.Label(basic_info_creation_frame, text="* First Name:").grid(row=0, column=0, sticky='nsew')
        ttk.Label(basic_info_creation_frame, text="* Last Name:").grid(row=1, column=0, sticky='nsew')
        ttk.Label(basic_info_creation_frame, text="* Email:").grid(row=2, column=0, sticky='nsew')
        ttk.Label(basic_info_creation_frame, text="* Phone Number:").grid(row=3, column=0, sticky='nsew')
        ttk.Label(basic_info_creation_frame, text="* Payment Method:").grid(row=4, column=0, sticky='nsew')
        ttk.Label(basic_info_creation_frame, text='Number of Guests:').grid(row=5, column=0, sticky='nsew')
        ttk.Label(basic_info_creation_frame, text='Visit Type:').grid(row=6, column=0, sticky='nsew')

        # Listbox of Number of Guests
        self.select_number_of_guest = ttk.Combobox(
            basic_info_creation_frame,
            textvariable=self.guest_numbers,
            state='readonly'
        )
        self.select_number_of_guest.grid(row=5, column=1, sticky='nsew')
        self.populate_guests_num_listbox()
        self.select_number_of_guest.current(0)

        # Listbox of Type
        self.select_type_guest = ttk.Combobox(
            basic_info_creation_frame,
            textvariable=self.guest_type,
            state='readonly'
        )
        self.select_type_guest.grid(row=6, column=1, sticky='nsew')
        self.populate_guests_type_listbox()
        self.select_type_guest.current()

        # Entries
        ttk.Entry(
            basic_info_creation_frame,
            textvariable=self.firstname_variable
        ).grid(row=0, column=1, sticky='ew')

        ttk.Entry(
            basic_info_creation_frame,
            textvariable=self.lastname_variable
        ).grid(row=1, column=1, sticky='ew')

        ttk.Entry(
            basic_info_creation_frame,
            textvariable=self.email_variable
        ).grid(row=2, column=1, sticky='ew')

        ttk.Entry(
            basic_info_creation_frame,
            textvariable=self.phone_number_variable
        ).grid(row=3, column=1, sticky='ew')

        ttk.Entry(
            basic_info_creation_frame,
            textvariable=self.payment_method_variable
        ).grid(row=4, column=1, sticky='ew')

        # Buttons
        tk.Button(
            basic_info_creation_frame,
            text="Next",
            command=self.next_to_create_rooms_button
        ).grid(row=8, columnspan=2, column=0, sticky='nsew')
        tk.Button(
            basic_info_creation_frame,
            text="Cancel",
            command=self.cancel_create_button
        ).grid(row=8, column=2, sticky='nsew')

        self.current_frame = basic_info_creation_frame
        return basic_info_creation_frame

    def create_room_information_frame(self):
        """Second Frame"""
        assign_to_a_room_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        assign_to_a_room_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        assign_to_a_room_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        self.fullname_variable.set(f'{self.firstname_variable.get()} {self.lastname_variable.get()}')

        # Labels
        ttk.Label(assign_to_a_room_frame, text='Name: ').grid(row=0, column=0, sticky='nsew')
        ttk.Label(assign_to_a_room_frame, text='Room').grid(row=1, column=0, sticky='nsew')
        ttk.Label(assign_to_a_room_frame, text='Room Type:').grid(row=2, column=0, sticky='nsew')
        ttk.Label(assign_to_a_room_frame, text='Room Price:').grid(row=3, column=0, sticky='nsew')
        ttk.Label(assign_to_a_room_frame, textvariable=self.fullname_variable).grid(row=0, column=1, sticky='nsew')
        ttk.Label(assign_to_a_room_frame, textvariable=self.rooms_type_variable).grid(row=2, column=1, sticky='nsew')
        ttk.Label(assign_to_a_room_frame, textvariable=self.rooms_price_variable).grid(row=3, column=1, sticky='nsew')

        # Listbox of Rooms
        self.select_rooms_list = ttk.Combobox(
            assign_to_a_room_frame,
            textvariable=self.rooms_variable,
            state='readonly'
        )
        self.select_rooms_list.grid(row=1, columnspan=2, column=1, sticky='nsew')
        self.populate_room_listbox()
        self.select_rooms_list.current()

        # Buttons
        tk.Button(
            assign_to_a_room_frame,
            text="Next",
            command=self.next_to_checkout_date_button
        ).grid(row=6, columnspan=2, column=0, sticky='nsew')
        tk.Button(
            assign_to_a_room_frame,
            text="Back",
            command=self.back_to_create_basic_information_button
        ).grid(row=6, column=2, sticky='nsew')
        tk.Button(
            assign_to_a_room_frame,
            text="Cancel",
            command=self.cancel_create_button
        ).grid(row=6, column=3, sticky='nsew')
        tk.Button(
            assign_to_a_room_frame,
            text='Check Room',
            command=self.check_room_button
        ).grid(row=5, column=3, sticky='nsew')

        self.current_frame = assign_to_a_room_frame
        return assign_to_a_room_frame

    def create_checkout_date_information_frame(self):
        """Third Frame"""
        checkout_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        checkout_frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        checkout_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        # Labels
        ttk.Label(checkout_frame, text='Check-in Date').grid(row=1, column=0, sticky='nsew')
        ttk.Label(checkout_frame, text='Check-out Date').grid(row=2, column=0, sticky='nsew')
        ttk.Label(checkout_frame, text='Year').grid(row=0, column=1, sticky='nsew')
        ttk.Label(checkout_frame, text='Month').grid(row=0, column=2, sticky='nsew')
        ttk.Label(checkout_frame, text='Day').grid(row=0, column=3, sticky='nsew')

        # Entries
        ttk.Entry(checkout_frame, textvariable=self.check_in_year_variable).grid(row=1, column=1, sticky='ew')
        ttk.Entry(checkout_frame, textvariable=self.check_in_month_variable).grid(row=1, column=2, sticky='ew')
        ttk.Entry(checkout_frame, textvariable=self.check_in_day_variable).grid(row=1, column=3, sticky='ew')
        ttk.Entry(checkout_frame, textvariable=self.check_out_year_variable).grid(row=2, column=1, sticky='ew')
        ttk.Entry(checkout_frame, textvariable=self.check_out_month_variable).grid(row=2, column=2, sticky='ew')
        ttk.Entry(checkout_frame, textvariable=self.check_out_day_variable).grid(row=2, column=3, sticky='ew')

        # Buttons
        tk.Button(checkout_frame, text="Today", command=self.get_date_button).grid(row=1, column=4, sticky='ew')

        tk.Button(
            checkout_frame,
            text="Next",
            command=self.next_to_confirm_guest_button
        ).grid(row=6, columnspan=2, column=0, sticky='ew')

        tk.Button(
            checkout_frame,
            text="Back",
            command=self.back_to_create_rooms_date_button
        ).grid(row=6, columnspan=2, column=2, sticky='ew')

        tk.Button(checkout_frame, text="Cancel", command=self.cancel_create_button).grid(row=6, column=4, sticky='ew')

        self.current_frame = checkout_frame
        return checkout_frame

    def create_confirm_information_frame(self):
        """Fourth Frame"""
        confirm_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        confirm_frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        confirm_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, uniform='a')

        # Labels
        ttk.Label(confirm_frame, text="Guest Confirmation").grid(row=0, columnspan=4, column=0, sticky='ew')
        ttk.Label(confirm_frame, text="Name:").grid(row=1, column=0, sticky='nsew')
        ttk.Label(confirm_frame, text="Room Number:").grid(row=2, column=0, sticky='nsew')
        ttk.Label(confirm_frame, text="Room Price:").grid(row=3, column=0, sticky='nsew')
        ttk.Label(confirm_frame, text="Room Type:").grid(row=4, column=0, sticky='nsew')
        ttk.Label(confirm_frame, text="Check-in:").grid(row=5, column=0, sticky='nsew')
        ttk.Label(confirm_frame, text="Check-out:").grid(row=6, column=0, sticky='nsew')
        ttk.Label(confirm_frame, text="Total Price:").grid(row=7, column=0, sticky='nsew')

        self.check_in_date_variable.set(
            f'{self.check_in_year_variable.get()}-'
            f'{self.check_in_month_variable.get()}-{self.check_in_day_variable.get()}'
        )
        self.check_out_date_variable.set(
            f'{self.check_out_year_variable.get()}-'
            f'{self.check_out_month_variable.get()}-{self.check_out_day_variable.get()}'
        )
        self.calculate_total_price()
        # Labels again with variables
        ttk.Label(confirm_frame, textvariable=self.fullname_variable).grid(row=1, column=1, sticky='nsew')
        ttk.Label(confirm_frame, textvariable=self.rooms_id_variable).grid(row=2, column=1, sticky='nsew')
        ttk.Label(confirm_frame, textvariable=self.rooms_price_variable).grid(row=3, column=1, sticky='nsew')
        ttk.Label(confirm_frame, textvariable=self.rooms_type_variable).grid(row=4, column=1, sticky='nsew')
        ttk.Label(confirm_frame, textvariable=self.check_in_date_variable).grid(row=5, column=1, sticky='nsew')
        ttk.Label(confirm_frame, textvariable=self.check_out_date_variable).grid(row=6, column=1, sticky='nsew')
        ttk.Label(confirm_frame, textvariable=self.rooms_total_price_variable).grid(row=7, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            confirm_frame,
            text="Confirm",
            command=self.create_confirm_button
        ).grid(row=8, columnspan=2, column=0, sticky='ew')

        tk.Button(
            confirm_frame,
            text="Back",
            command=self.back_to_create_checkout_date_button
        ).grid(row=8, columnspan=2, column=2, sticky='ew')

        tk.Button(confirm_frame, text="Cancel", command=self.cancel_create_button).grid(row=8, column=4, sticky='ew')

        self.current_frame = confirm_frame
        return confirm_frame

    def next_to_create_rooms_button(self):
        """First Frame 'Next' Button"""
        print(self.phone_number_variable.get())
        if self.if_first_frame_entry_is_empty():
            showwarning("Error!", "Please fill in all the blanks!")
        elif not self.check_phone_number_valid():
            showwarning("Error!", "Phone Number is Not Valid!")
        elif not self.check_email_valid(self.email_variable.get()):
            showwarning("Error!", "Enter Valid Email!")
        else:
            self.current_frame.pack_forget()
            self.create_room_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def next_to_checkout_date_button(self):
        """Second Frame 'Next' Button"""
        if not self.select_rooms_list.get():
            showwarning("Error!", "No Room Selected!")
        else:
            self.current_frame.pack_forget()
            self.create_checkout_date_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def back_to_create_basic_information_button(self):
        """Second Frame 'Back' Button"""
        self.rooms_id_variable.set('')
        self.rooms_name_variable.set('')
        self.rooms_type_variable.set('')
        self.rooms_price_variable.set('')
        self.current_frame.pack_forget()
        self.create_basic_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def next_to_confirm_guest_button(self):
        """Third Frame 'Next' Button"""
        try:
            yy1 = int(self.check_in_year_variable.get())
            mm1 = int(self.check_in_month_variable.get())
            dd1 = int(self.check_in_day_variable.get())
            yy2 = int(self.check_out_year_variable.get())
            mm2 = int(self.check_out_month_variable.get())
            dd2 = int(self.check_out_day_variable.get())
            if not self.check_date_valid(yy1, mm1, dd1):
                showwarning(title="Error", message="Improper Date!")
            elif not self.check_date_valid(yy2, mm2, dd2):
                showwarning(title="Error", message="Improper Date!")
            else:
                self.current_frame.pack_forget()
                self.create_confirm_information_frame().pack(expand=True, fill='both', padx=5, pady=5)
        except:
            showwarning(title="Error", message="Improper Date!")

    def back_to_create_rooms_date_button(self):
        self.current_frame.pack_forget()
        self.create_room_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def create_confirm_button(self):
        """Fourth Frame 'Submit' Button"""
        confirm = askyesno(title="Confirm Guest?", message="Confirm Guest?")
        if confirm:
            self.create_a_guest_sql.create_a_guest(self.firstname_variable.get(),
                                                   self.lastname_variable.get(),
                                                   self.email_variable.get(),
                                                   self.phone_number_variable.get(),
                                                   self.payment_method_variable.get()
                                                   )
            latest_guest_id = self.create_a_guest_sql.get_latest_guest_id()
            latest_billing_id = self.create_a_guest_sql.creates_billing_record(self.rooms_total_price_variable.get(),
                                                                               self.payment_method_variable.get())
            self.create_a_guest_sql.creates_visit_record(self.guest_type.get(),
                                                         self.guest_numbers.get(),
                                                         self.check_in_date_variable.get(),
                                                         self.check_out_date_variable.get(),
                                                         latest_guest_id,
                                                         self.rooms_id_variable.get(),
                                                         latest_billing_id
                                                         )
            self.create_a_guest_sql.set_room_availability(self.rooms_id_variable.get())
            self.destroy()

    def back_to_create_checkout_date_button(self):
        self.current_frame.pack_forget()
        self.create_checkout_date_information_frame().pack(expand=True, fill='both', padx=5, pady=5)
        pass

    def calculate_total_price(self):
        check_in_date = date(
            int(self.check_in_year_variable.get()),
            int(self.check_in_month_variable.get()),
            int(self.check_in_day_variable.get()))

        check_out_date = date(
            int(self.check_out_year_variable.get()),
            int(self.check_out_month_variable.get()),
            int(self.check_out_day_variable.get()))

        days = abs(check_out_date - check_in_date).days
        days = int(days)
        price = int(self.rooms_price_variable.get())
        self.rooms_total_price_variable.set((1 + days) * price)

    def check_room_button(self):
        if not self.select_rooms_list.get():
            showwarning("Error!", "No Room Selected!")
        else:
            selected_room_index = (self.select_rooms_list.get()).split(" ")
            selected_room = sql_connection.retrieve_a_room(selected_room_index[0])
            self.rooms_id_variable.set(selected_room[0])
            self.rooms_name_variable.set(selected_room[1])
            self.rooms_type_variable.set(selected_room[2])
            self.rooms_price_variable.set(selected_room[3])

    def get_date_button(self):
        full_date = datetime.now()
        today_date = str(full_date.date()).split("-")
        self.check_in_year_variable.set(today_date[0])
        self.check_in_month_variable.set(today_date[1])
        self.check_in_day_variable.set(today_date[2])

    def cancel_create_button(self):
        self.grab_release()
        self.destroy()

    def populate_room_listbox(self):
        all_rooms = sql_connection.retrieve_rooms_list()
        rooms = []

        if self.guest_numbers.get() == 1:
            for i in all_rooms:
                if i[-1] == 0 and i[4] == 1:
                    rooms.append((i[1], i[2]))

        elif self.guest_numbers.get() == 2:
            for i in all_rooms:
                if i[-1] == 0 and i[4] == 1 and i[2] != "Single":
                    rooms.append((i[1], i[2]))

        elif self.guest_numbers.get() == 3:
            for i in all_rooms:
                if i[-1] == 0 and i[4] == 1 and i[2] not in ["Single", "Double"]:
                    rooms.append((i[1], i[2]))

        else:
            for i in all_rooms:
                if i[-1] == 0 and i[4] == 1 and i[2] not in ["Single", "Double", "Triple"]:
                    rooms.append((i[1], i[2]))

        room_numbers = tuple(rooms)
        self.select_rooms_list['values'] = room_numbers

    def populate_guests_num_listbox(self):
        numbers_of_guests = ['1', '2', '3', '4', '5', '6']
        self.select_number_of_guest['values'] = numbers_of_guests

    def populate_guests_type_listbox(self):
        guest_type = ['Walk In', 'Reservation']
        self.select_type_guest['values'] = guest_type

    def check_date_valid(self, year, month, day):
        try:
            date(year, month, day)
            return True
        except ValueError as e:
            print("Something went wrong! Error: ", e)
            return False

    def check_email_valid(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, email):
            return True
        else:
            return False

    def check_phone_number_valid(self):
        pattern = r'^\+?[0-9]\d{1,14}$'
        if self.phone_number_variable:
            if re.match(pattern, self.phone_number_variable.get()):
                return True
            else:
                return False
        else:
            return False

    def if_first_frame_entry_is_empty(self):
        fname = self.firstname_variable.get()
        lname = self.lastname_variable.get()
        phone = self.phone_number_variable.get()
        email = self.email_variable.get()
        pay = self.payment_method_variable.get()
        gnumber = self.select_number_of_guest.get()
        gtype = self.select_type_guest.get()

        if [x for x in (fname, lname, phone, email, pay, gnumber, gtype) if x == ""]:
            return True
        else:
            return False


class GuestModifyWindow(tk.Toplevel):
    def __init__(self, root, guest_id_modify):
        super().__init__(root)

        self.geometry('500x200')
        self.minsize(400, 200)

        self.title("Modify Guest")

        # Guest ID that is passed to modify
        self.selected_guest_id = tk.StringVar()
        self.selected_guest_id.set(str(guest_id_modify))

        # Retrieved Variables
        self.firstname_variable = tk.StringVar()
        self.lastname_variable = tk.StringVar()
        self.email_variable = tk.StringVar()
        self.phone_number_variable = tk.StringVar()
        self.payment_info_variable = tk.StringVar()
        self.visit_id_variable = tk.StringVar()
        self.visit_type_variable = tk.StringVar()
        self.visit_number_of_guests_variable = tk.StringVar()
        self.check_in_date_variable = tk.StringVar()
        self.check_out_date_variable = tk.StringVar()
        self.current_rooms_id_variable = tk.StringVar()
        self.current_rooms_name_variable = tk.StringVar()
        self.current_rooms_type_variable = tk.StringVar()
        self.current_rooms_price_variable = tk.StringVar()
        self.billing_id_variable = tk.StringVar()

        # Entry and Derived Variables
        self.guest_name_variable = tk.StringVar()
        self.rooms_list_variable = tk.StringVar()
        self.rooms_id_variable = tk.StringVar()
        self.rooms_name_variable = tk.StringVar()
        self.rooms_type_variable = tk.StringVar()
        self.rooms_price_variable = tk.StringVar()
        self.rooms_total_price_variable = tk.IntVar()
        self.new_rooms_id_variable = tk.StringVar()
        self.new_rooms_name_variable = tk.StringVar()
        self.new_rooms_type_variable = tk.StringVar()
        self.new_rooms_price_variable = tk.StringVar()
        self.assigned_room_variable = tk.StringVar()
        self.new_room_flag = False

        # Entry and Derived Variables
        self.check_in_year_variable = tk.StringVar()
        self.check_in_month_variable = tk.StringVar()
        self.check_in_day_variable = tk.StringVar()
        self.check_out_year_variable = tk.StringVar()
        self.check_out_month_variable = tk.StringVar()
        self.check_out_day_variable = tk.StringVar()

        self.select_rooms = None
        self.current_frame = None

        # Retrieves guest information to modify
        self.get_guest_details_to_modify()
        self.modify_basic_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

        self.grab_set()

    # Frames
    def modify_basic_information_frame(self):
        """First Frame"""
        modify_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        modify_frame.columnconfigure((0, 1), weight=1, uniform='a')
        modify_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        # Labels
        ttk.Label(
            modify_frame,
            text="Guest ID: "
        ).grid(row=0, column=0, sticky='nsew')
        ttk.Label(
            modify_frame,
            text="* First Name:"
        ).grid(row=1, column=0, sticky='nsew')
        ttk.Label(
            modify_frame,
            text="* Last Name:"
        ).grid(row=2, column=0, sticky='nsew')
        ttk.Label(
            modify_frame,
            text="* Email:"
        ).grid(row=3, column=0, sticky='nsew')
        ttk.Label(
            modify_frame,
            text="Phone Number:"
        ).grid(row=4, column=0, sticky='nsew')
        ttk.Label(
            modify_frame,
            text="* Payment Info:"
        ).grid(row=5, column=0, sticky='nsew')

        # Entries To Fill In
        ttk.Label(modify_frame, textvariable=self.selected_guest_id).grid(row=0, column=1, sticky='ew')
        ttk.Entry(modify_frame, textvariable=self.firstname_variable).grid(row=1, column=1, sticky='ew')
        ttk.Entry(modify_frame, textvariable=self.lastname_variable).grid(row=2, column=1, sticky='ew')
        ttk.Entry(modify_frame, textvariable=self.email_variable).grid(row=3, column=1, sticky='ew')
        ttk.Entry(modify_frame, textvariable=self.phone_number_variable).grid(row=4, column=1, sticky='ew')
        ttk.Entry(modify_frame, textvariable=self.payment_info_variable).grid(row=5, column=1, sticky='ew')

        # Buttons For First Frame
        tk.Button(
            modify_frame,
            text="Next",
            command=self.next_to_rooms_information_button
        ).grid(row=6, column=0, sticky='nsew')
        tk.Button(
            modify_frame,
            text="Cancel",
            command=self.cancel_modify_button
        ).grid(row=6, column=1, sticky='nsew')

        self.current_frame = modify_frame
        return modify_frame

    def modify_room_information_frame(self):
        """Second Frame"""
        modify_room_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        modify_room_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        modify_room_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        self.guest_name_variable.set(f'{self.firstname_variable.get()} {self.lastname_variable.get()}')

        # Labels
        ttk.Label(modify_room_frame, text='Name: ').grid(row=0, column=0, sticky='nsew')
        ttk.Label(modify_room_frame, text='Room').grid(row=1, column=0, sticky='nsew')
        ttk.Label(modify_room_frame, text='Room Type:').grid(row=2, column=0, sticky='nsew')
        ttk.Label(modify_room_frame, text='Room Price:').grid(row=3, column=0, sticky='nsew')
        ttk.Label(modify_room_frame, text='Current Room: ').grid(row=4, column=0, sticky='nsew')
        ttk.Label(modify_room_frame, text='New Room: ').grid(row=5, column=0, sticky='nsew')

        # Labels with Variables
        ttk.Label(modify_room_frame, textvariable=self.guest_name_variable).grid(row=0, column=1, sticky='nsew')
        ttk.Label(modify_room_frame, textvariable=self.rooms_type_variable).grid(row=2, column=1, sticky='nsew')
        ttk.Label(modify_room_frame, textvariable=self.rooms_price_variable).grid(row=3, column=1, sticky='nsew')
        ttk.Label(modify_room_frame, textvariable=self.current_rooms_name_variable).grid(row=4, column=1, sticky='nsew')
        ttk.Label(modify_room_frame, textvariable=self.new_rooms_name_variable).grid(row=5, column=1, sticky='nsew')
        ttk.Label(modify_room_frame, textvariable=self.assigned_room_variable).grid(row=4, column=2, sticky='ew')

        # Listbox of Rooms
        self.select_rooms = ttk.Combobox(
            modify_room_frame,
            textvariable=self.rooms_list_variable,
            state='readonly'
        )
        self.select_rooms.grid(row=1, columnspan=2, column=1, sticky='nsew')
        self.populate_room_listbox()

        # Buttons
        tk.Button(
            modify_room_frame,
            text="Next",
            command=self.next_to_check_date_information_button
        ).grid(row=6, columnspan=2, column=0, sticky='nsew')
        tk.Button(
            modify_room_frame,
            text="Back",
            command=self.back_to_basic_information_button
        ).grid(row=6, column=2, sticky='nsew')
        tk.Button(
            modify_room_frame,
            text="Cancel",
            command=self.cancel_modify_button
        ).grid(row=6, column=3, sticky='nsew')
        tk.Button(
            modify_room_frame,
            text='Assign Room',
            command=self.assign_room_button
        ).grid(row=5, column=2, sticky='nsew')
        tk.Button(
            modify_room_frame,
            text='Check Room',
            command=self.check_room_button
        ).grid(row=5, column=3, sticky='nsew')

        self.current_frame = modify_room_frame
        return modify_room_frame

    def modify_checkout_information_frame(self):
        """Third Frame"""
        modify_checkout_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        modify_checkout_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        modify_checkout_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        # Get the check-in/out dates of the guest to modify
        self.get_check_in_out_date()

        # Labels
        ttk.Label(modify_checkout_frame, text='Check-in Date').grid(row=1, column=0, sticky='nsew')
        ttk.Label(modify_checkout_frame, text='Check-out Date').grid(row=2, column=0, sticky='nsew')
        ttk.Label(modify_checkout_frame, text='Year').grid(row=0, column=1, sticky='nsew')
        ttk.Label(modify_checkout_frame, text='Month').grid(row=0, column=2, sticky='nsew')
        ttk.Label(modify_checkout_frame, text='Day').grid(row=0, column=3, sticky='nsew')

        # Entries
        ttk.Entry(
            modify_checkout_frame,
            textvariable=self.check_in_year_variable,
            state='readonly'
        ).grid(row=1, column=1, sticky='ew')

        ttk.Entry(
            modify_checkout_frame,
            textvariable=self.check_in_month_variable,
            state='readonly'
        ).grid(row=1, column=2, sticky='ew')

        ttk.Entry(
            modify_checkout_frame,
            textvariable=self.check_in_day_variable,
            state='readonly'
        ).grid(row=1, column=3, sticky='ew')

        ttk.Entry(modify_checkout_frame, textvariable=self.check_out_year_variable).grid(row=2, column=1, sticky='ew')
        ttk.Entry(modify_checkout_frame, textvariable=self.check_out_month_variable).grid(row=2, column=2, sticky='ew')
        ttk.Entry(modify_checkout_frame, textvariable=self.check_out_day_variable).grid(row=2, column=3, sticky='ew')

        # Buttons
        tk.Button(
            modify_checkout_frame,
            text="Next",
            command=self.next_to_confirm_modify_information_button
        ).grid(row=6, columnspan=2, column=0, sticky='ew')

        tk.Button(
            modify_checkout_frame,
            text="Back",
            command=self.back_to_rooms_information_button
        ).grid(row=6, column=2, sticky='ew')

        tk.Button(
            modify_checkout_frame,
            text="Cancel",
            command=self.cancel_modify_button
        ).grid(row=6, column=3, sticky='ew')

        self.current_frame = modify_checkout_frame
        return modify_checkout_frame

    def modify_confirm_information_frame(self):
        """Fourth Frame"""
        modify_confirm_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        modify_confirm_frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        modify_confirm_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, uniform='a')

        # Labels
        ttk.Label(
            modify_confirm_frame,
            text="Guest Modification Confirmation"
        ).grid(row=0, columnspan=4, column=0, sticky='ew')

        # Labels with Text Only
        ttk.Label(modify_confirm_frame, text="Name:").grid(row=1, column=0, sticky='nsew')
        ttk.Label(modify_confirm_frame, text="Room Number:").grid(row=2, column=0, sticky='nsew')
        ttk.Label(modify_confirm_frame, text="Room Price:").grid(row=3, column=0, sticky='nsew')
        ttk.Label(modify_confirm_frame, text="Room Type:").grid(row=4, column=0, sticky='nsew')
        ttk.Label(modify_confirm_frame, text="Check-in:").grid(row=5, column=0, sticky='nsew')
        ttk.Label(modify_confirm_frame, text="Check-out:").grid(row=6, column=0, sticky='nsew')
        ttk.Label(modify_confirm_frame, text="Total Price:").grid(row=7, column=0, sticky='nsew')

        self.check_in_date_variable.set(
            f'{self.check_in_year_variable.get()}-'
            f'{self.check_in_month_variable.get()}-'
            f'{self.check_in_day_variable.get()}'
        )
        self.check_out_date_variable.set(
            f'{self.check_out_year_variable.get()}-'
            f'{self.check_out_month_variable.get()}-'
            f'{self.check_out_day_variable.get()}'
        )

        self.calculate_total_price()

        # Labels again with variables
        ttk.Label(modify_confirm_frame, textvariable=self.guest_name_variable).grid(row=1, column=1, sticky='nsew')

        if self.new_room_flag:
            ttk.Label(
                modify_confirm_frame,
                textvariable=self.new_rooms_name_variable
            ).grid(row=2, column=1, sticky='nsew')

            ttk.Label(
                modify_confirm_frame,
                textvariable=self.new_rooms_price_variable
            ).grid(row=3, column=1, sticky='nsew')

            ttk.Label(
                modify_confirm_frame,
                textvariable=self.new_rooms_type_variable
            ).grid(row=4, column=1, sticky='nsew')
        else:
            ttk.Label(
                modify_confirm_frame,
                textvariable=self.current_rooms_name_variable
            ).grid(row=2, column=1, sticky='nsew')

            ttk.Label(
                modify_confirm_frame,
                textvariable=self.current_rooms_price_variable
            ).grid(row=3, column=1, sticky='nsew')

            ttk.Label(
                modify_confirm_frame,
                textvariable=self.current_rooms_type_variable
            ).grid(row=4, column=1, sticky='nsew')

        ttk.Label(modify_confirm_frame, textvariable=self.check_in_date_variable).grid(row=5, column=1, sticky='nsew')
        ttk.Label(modify_confirm_frame, textvariable=self.check_out_date_variable).grid(row=6, column=1, sticky='nsew')
        ttk.Label(
            modify_confirm_frame,
            textvariable=self.rooms_total_price_variable
        ).grid(row=7, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            modify_confirm_frame,
            text="Confirm Update",
            command=self.modify_confirm_button
        ).grid(row=8, columnspan=2, column=0, sticky='nsew')

        tk.Button(
            modify_confirm_frame,
            text="Back",
            command=self.back_to_check_out_date_information_button
        ).grid(row=8, columnspan=2, column=2, sticky='nsew')

        tk.Button(
            modify_confirm_frame,
            text="Cancel",
            command=self.cancel_modify_button
        ).grid(row=8, column=4, sticky='nsew')

        self.current_frame = modify_confirm_frame
        return modify_confirm_frame

    # Buttons Functions Below
    def next_to_rooms_information_button(self):
        """First Frame 'Next' Button"""
        self.current_frame.pack_forget()
        self.modify_room_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def next_to_check_date_information_button(self):
        """Second Frame 'Next' Button"""
        self.current_frame.pack_forget()
        self.modify_checkout_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def back_to_basic_information_button(self):
        """Second Frame 'Back' Button"""
        self.current_frame.pack_forget()
        self.modify_basic_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def next_to_confirm_modify_information_button(self):
        """Third Frame 'Next' Button"""
        self.current_frame.pack_forget()
        self.modify_confirm_information_frame().pack(expand=True, fill='both', padx=5, pady=5)
        pass

    def back_to_rooms_information_button(self):
        """Third Frame 'Back' Button"""
        self.current_frame.pack_forget()
        self.modify_room_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def modify_confirm_button(self):
        confirm_modify = askyesnocancel(
            title="Confirm Guest Modification?",
            message="You will update the guest's information\nConfirm?")
        if confirm_modify:
            modify_sql = ModifyGuestSQL()

            modify_sql.update_guest_information(self.selected_guest_id.get(),
                                                self.firstname_variable.get(),
                                                self.lastname_variable.get(),
                                                self.email_variable.get(),
                                                self.phone_number_variable.get(),
                                                self.payment_info_variable.get()
                                                )

            modify_sql.update_visit_information(self.visit_type_variable.get(),
                                                self.visit_number_of_guests_variable.get(),
                                                self.check_in_date_variable.get(),
                                                self.check_out_date_variable.get(),
                                                self.billing_id_variable.get(),
                                                self.selected_guest_id.get(),
                                                self.visit_id_variable.get()
                                                )
            if self.new_room_flag:
                modify_sql.update_room_information(self.selected_guest_id.get(),
                                                   self.new_rooms_id_variable.get(),
                                                   self.current_rooms_id_variable.get()
                                                   )
            modify_sql.update_bill_information(self.billing_id_variable.get(),
                                               self.rooms_total_price_variable.get(),
                                               self.payment_info_variable.get())
            showinfo(title="Success!", message="Update Success!")
            self.destroy()
        elif confirm_modify is None:
            self.destroy()
        else:
            pass

    def back_to_check_out_date_information_button(self):
        """Fourth Frame 'Back' Button"""
        self.current_frame.pack_forget()
        self.modify_checkout_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def cancel_modify_button(self):
        self.grab_release()
        self.destroy()

    def populate_room_listbox(self):
        all_rooms = sql_connection.retrieve_rooms_list()
        rooms = []

        for i in all_rooms:
            if i[-1] == 0 and i[4] == 1:
                rooms.append(i[1])

        room_numbers = tuple(rooms)
        self.select_rooms['values'] = room_numbers

    def check_room_button(self):
        if not self.select_rooms.get():
            showwarning("Error!", "No Room Selected!")
        else:
            retrieved_room = sql_connection.retrieve_a_room(self.select_rooms.get())
            self.rooms_id_variable.set(retrieved_room[0])
            self.rooms_name_variable.set(retrieved_room[1])
            self.rooms_type_variable.set(retrieved_room[2])
            self.rooms_price_variable.set(retrieved_room[3])

    def calculate_total_price(self):
        check_in_date = date(
            int(self.check_in_year_variable.get()),
            int(self.check_in_month_variable.get()),
            int(self.check_in_day_variable.get()))

        check_out_date = date(
            int(self.check_out_year_variable.get()),
            int(self.check_out_month_variable.get()),
            int(self.check_out_day_variable.get()))

        days = abs(check_out_date - check_in_date).days
        days = int(days)

        self.new_rooms_price_variable.get()

        if self.new_room_flag:
            price = int(self.new_rooms_price_variable.get())
        else:
            price = int(self.current_rooms_price_variable.get())
        self.rooms_total_price_variable.set((1 + days) * price)

    def get_guest_details_to_modify(self):
        guest_id_index = self.selected_guest_id.get()
        guest_details = sql_connection.get_details_to_modify(guest_id_index)
        self.firstname_variable.set(guest_details[1])
        self.lastname_variable.set(guest_details[2])
        self.email_variable.set(guest_details[3])
        self.phone_number_variable.set(guest_details[4])
        self.payment_info_variable.set(guest_details[5])
        self.visit_id_variable.set(guest_details[6])
        self.visit_type_variable.set(guest_details[7])
        self.visit_number_of_guests_variable.set(guest_details[8])
        self.check_in_date_variable.set(guest_details[9])
        self.check_out_date_variable.set(guest_details[10])
        self.current_rooms_id_variable.set(guest_details[11])
        self.current_rooms_name_variable.set(guest_details[12])
        self.current_rooms_type_variable.set(guest_details[13])
        self.current_rooms_price_variable.set(guest_details[14])
        self.billing_id_variable.set(guest_details[15])

    def get_check_in_out_date(self):
        check_in_date = str(self.check_in_date_variable.get()).split('-')
        self.check_in_year_variable.set(check_in_date[0])
        self.check_in_month_variable.set(check_in_date[1])
        self.check_in_day_variable.set(check_in_date[2])

        check_out_date = str(self.check_out_date_variable.get()).split('-')
        self.check_out_year_variable.set(check_out_date[0])
        self.check_out_month_variable.set(check_out_date[1])
        self.check_out_day_variable.set(check_out_date[2])

    def assign_room_button(self):
        if not self.select_rooms.get():
            showwarning("Error!", "No Room Selected!")
        else:
            retrieved_room = sql_connection.retrieve_a_room(self.select_rooms.get())
            self.new_rooms_id_variable.set(retrieved_room[0])
            self.new_rooms_name_variable.set(retrieved_room[1])
            self.new_rooms_type_variable.set(retrieved_room[2])
            self.new_rooms_price_variable.set(retrieved_room[3])
            self.new_room_flag = True
            self.assigned_room_variable.set("Assigned!")


class RoomCreationWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        self.geometry('500x200')
        self.minsize(400, 200)

        self.title("Room Creation")

        # Variables
        self.create_room_name_variable = tk.StringVar()
        self.create_room_type_variable = tk.StringVar()
        self.create_room_price_variable = tk.StringVar()
        self.employees_variable = tk.StringVar()
        self.employee_id_variable = tk.StringVar()
        self.employee_list = ttk.Combobox()
        self.current_frame = ttk.Frame()
        self.employees = []
        self.room_sql = RoomTabSQL()

        # Frame Placement
        self.create_basic_room_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

        self.grab_set()

    def create_basic_room_information_frame(self):
        """First Frame"""
        create_room_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        create_room_frame.columnconfigure((0, 1), weight=1, uniform='a')
        create_room_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        # Labels Information
        ttk.Label(create_room_frame, text="Room Number:").grid(row=0, column=0, sticky='nsew')
        ttk.Label(create_room_frame, text="Room Type:").grid(row=1, column=0, sticky='nsew')
        ttk.Label(create_room_frame, text="Room Price:").grid(row=2, column=0, sticky='nsew')

        # Entries for Input
        ttk.Entry(
            create_room_frame,
            textvariable=self.create_room_name_variable
        ).grid(row=0, column=1, sticky='nsew')

        ttk.Entry(
            create_room_frame,
            textvariable=self.create_room_type_variable
        ).grid(row=1, column=1, sticky='nsew')

        ttk.Entry(
            create_room_frame,
            textvariable=self.create_room_price_variable
        ).grid(row=2, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            create_room_frame,
            text="Next",
            command=self.next_to_managed_by_button
        ).grid(row=6, column=0, sticky='nsew')

        tk.Button(
            create_room_frame,
            text="Cancel",
            command=self.cancel_button
        ).grid(row=6, column=1, sticky='nsew')

        self.current_frame = create_room_frame
        return create_room_frame

    def create_room_managed_by_frame(self):
        """Second Frame"""
        managed_by_room_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        managed_by_room_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
        managed_by_room_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        # Labels Information
        ttk.Label(
            managed_by_room_frame,
            text="Employee"
        ).grid(row=0, column=0, sticky='nsew')

        # Employee ComboBox
        self.employee_list = ttk.Combobox(
            managed_by_room_frame,
            textvariable=self.employees_variable,
            state='readonly'
        )
        self.populate_employee_list()
        self.employee_list.grid(row=1, columnspan=2, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            managed_by_room_frame,
            text="Confirm",
            command=self.create_confirm_room_button
        ).grid(row=6, column=0, sticky='nsew')

        tk.Button(
            managed_by_room_frame,
            text="Back",
            command=self.back_to_basic_room_information_button
        ).grid(row=6, column=1, sticky='nsew')

        tk.Button(
            managed_by_room_frame,
            text="Cancel",
            command=self.cancel_button
        ).grid(row=6, column=2, sticky='nsew')

        self.current_frame = managed_by_room_frame
        return managed_by_room_frame

    def next_to_managed_by_button(self):
        """First Frame 'Next' Button"""
        self.current_frame.pack_forget()
        self.create_room_managed_by_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def back_to_basic_room_information_button(self):
        self.current_frame.pack_forget()
        self.create_basic_room_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def create_confirm_room_button(self):
        confirm_create_room = askyesno(title="Create?",
                                       message=f"You are about to create Room {self.create_room_name_variable.get()}."
                                               f"\nConfirm?")
        if confirm_create_room:
            employee_list_index = self.employee_list.current()
            self.employee_id_variable.set(self.get_employee_id_from_dictionary(employee_list_index))
            self.room_sql.create_a_room(self.create_room_name_variable.get(),
                                        self.create_room_type_variable.get(),
                                        self.create_room_price_variable.get(),
                                        self.employee_id_variable.get()
                                        )
            self.destroy()

    def cancel_button(self):
        self.destroy()

    ##########################################################

    def populate_employee_list(self):
        """Populate the combo box of employees"""
        all_employee = sql_connection.retrieve_employee_list()

        for i in all_employee:
            if i[-1] == 0:
                employee_name = {"id": i[0], "names": (i[1], i[2]), "job_position": i[3]}

                self.employees.append(employee_name)

        self.employee_list['values'] = [items['names'] for items in self.employees]

    def get_employee_id_from_dictionary(self, index):
        if index >= 0:
            selected_employee = self.employees[index]
            employee_id = selected_employee['id']
            return employee_id


class RoomModificationWindow(tk.Toplevel):
    def __init__(self, root, selected_room_id):
        super().__init__(root)

        self.geometry('500x200')
        self.minsize(400, 200)

        self.title("Room Creation")

        # Variables
        self.modify_room_id_variable = tk.StringVar()
        self.modify_room_name_variable = tk.StringVar()
        self.modify_room_type_variable = tk.StringVar()
        self.modify_room_price_variable = tk.StringVar()
        self.current_employee_id_variable = tk.StringVar()
        self.employee_list = ttk.Combobox()
        self.employees_list_variable = tk.StringVar()
        self.employee_id_variable = tk.StringVar()
        self.current_frame = ttk.Frame()
        self.employees = []
        self.room_sql = RoomTabSQL()

        self.retrieve_room_details(selected_room_id)

        # Frame Placement
        self.modify_basic_room_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

        self.grab_set()

    def modify_basic_room_information_frame(self):
        """First Frame"""
        modify_room_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        modify_room_frame.columnconfigure((0, 1), weight=1, uniform='a')
        modify_room_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        # Labels Information
        ttk.Label(modify_room_frame, text="Room ID:").grid(row=0, column=0, sticky='nsew')
        ttk.Label(modify_room_frame, text="Room Number:").grid(row=1, column=0, sticky='nsew')
        ttk.Label(modify_room_frame, text="Room Type:").grid(row=2, column=0, sticky='nsew')
        ttk.Label(modify_room_frame, text="Room Price:").grid(row=3, column=0, sticky='nsew')

        # Entries for Input
        ttk.Label(
            modify_room_frame,
            textvariable=self.modify_room_id_variable
        ).grid(row=0, column=1, sticky='nsew')
        ttk.Entry(
            modify_room_frame,
            textvariable=self.modify_room_name_variable
        ).grid(row=1, column=1, sticky='nsew')

        ttk.Entry(
            modify_room_frame,
            textvariable=self.modify_room_type_variable
        ).grid(row=2, column=1, sticky='nsew')

        ttk.Entry(
            modify_room_frame,
            textvariable=self.modify_room_price_variable
        ).grid(row=3, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            modify_room_frame,
            text="Next",
            command=self.next_to_managed_by_button
        ).grid(row=6, column=0, sticky='nsew')

        tk.Button(
            modify_room_frame,
            text="Cancel",
            command=self.cancel_button
        ).grid(row=6, column=1, sticky='nsew')

        self.current_frame = modify_room_frame
        return modify_room_frame

    def modify_room_managed_by_frame(self):
        """Second Frame"""
        managed_by_room_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        managed_by_room_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
        managed_by_room_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        # Labels Information
        ttk.Label(
            managed_by_room_frame,
            text="Employee List"
        ).grid(row=0, column=1, sticky='nsew')

        ttk.Label(
            managed_by_room_frame,
            text="Employee"
        ).grid(row=1, column=0, sticky='nsew')

        ttk.Label(
            managed_by_room_frame,
            text="Current Managing: "
        ).grid(row=3, column=0, sticky='nsew')

        ttk.Label(
            managed_by_room_frame,
            textvariable=self.current_employee_id_variable
        ).grid(row=3, column=1, sticky='nsew')

        # Employee ComboBox
        self.employee_list = ttk.Combobox(
            managed_by_room_frame,
            textvariable=self.employees_list_variable,
            state='readonly'
        )
        self.populate_employee_list()
        self.employee_list.grid(row=1, columnspan=2, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            managed_by_room_frame,
            text="Confirm",
            command=self.modify_confirm_room_button
        ).grid(row=6, column=0, sticky='nsew')

        tk.Button(
            managed_by_room_frame,
            text="Back",
            command=self.back_to_basic_room_information_button
        ).grid(row=6, column=1, sticky='nsew')

        tk.Button(
            managed_by_room_frame,
            text="Cancel",
            command=self.cancel_button
        ).grid(row=6, column=2, sticky='nsew')

        self.current_frame = managed_by_room_frame
        return managed_by_room_frame

    def next_to_managed_by_button(self):
        """First Frame 'Next' Button"""
        self.current_frame.pack_forget()
        self.modify_room_managed_by_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def back_to_basic_room_information_button(self):
        self.current_frame.pack_forget()
        self.modify_basic_room_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def modify_confirm_room_button(self):
        confirm_create_room = askyesno(title="Modify?",
                                       message=f"You are about to update Room {self.modify_room_name_variable.get()}."
                                               f"\nConfirm?")
        if confirm_create_room:
            employee_list_index = self.employee_list.current()
            self.employee_id_variable.set(self.get_employee_id_from_dictionary(employee_list_index))
            self.room_sql.update_room_information(self.modify_room_id_variable.get(),
                                                  self.modify_room_name_variable.get(),
                                                  self.modify_room_type_variable.get(),
                                                  self.modify_room_price_variable.get(),
                                                  self.employee_id_variable.get()
                                                  )
            self.destroy()

    def cancel_button(self):
        self.destroy()

    ###################################################################################################################

    def populate_employee_list(self):
        """Populate the combo box of employees"""
        all_employee = sql_connection.retrieve_employee_list()

        for i in all_employee:
            if i[-1] == 0:
                employee_name = {"id": i[0], "names": (i[1], i[2]), "job_position": i[3]}

                self.employees.append(employee_name)

        self.employee_list['values'] = [items['names'] for items in self.employees]

    def get_employee_id_from_dictionary(self, index):
        if index >= 0:
            selected_employee = self.employees[index]
            employee_id = selected_employee['id']
            return employee_id

    def retrieve_room_details(self, index):
        self.modify_room_id_variable.set(index)
        retrieved_room = self.room_sql.retrieve_a_specific_room(index)

        self.modify_room_name_variable.set(retrieved_room[1])
        self.modify_room_type_variable.set(retrieved_room[2])
        self.modify_room_price_variable.set(retrieved_room[3])
        self.current_employee_id_variable.set(retrieved_room[5])


class ScheduleCreationWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        # Window Configurations
        self.geometry('500x200')
        self.minsize(400, 200)
        self.title('Schedule Creation')

        # Variables
        self.create_start_date_variable = tk.StringVar()
        self.create_end_date_variable = tk.StringVar()
        self.num_of_days = tk.StringVar()
        self.current_frame = ttk.Frame()
        self.sched_sql = ScheduleTabSQL()

        # Frame Placement
        self.create_basic_schedule_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

        self.grab_set()

    def create_basic_schedule_information_frame(self):
        create_schedule_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        create_schedule_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        create_schedule_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')

        # Labels
        ttk.Label(create_schedule_frame, text="Start Date").grid(row=1, column=0, sticky='nsew')
        ttk.Label(create_schedule_frame, text="End Date").grid(row=2, column=0, sticky='nsew')
        ttk.Label(create_schedule_frame, text='Number of Days').grid(row=3, column=0, sticky='nsew')
        ttk.Label(create_schedule_frame, textvariable=self.num_of_days).grid(row=3, column=1, sticky='nsew')

        # Entries
        ttk.Entry(
            create_schedule_frame,
            textvariable=self.create_start_date_variable,
        ).grid(row=1, column=1, sticky='nsew')

        ttk.Entry(
            create_schedule_frame,
            textvariable=self.create_end_date_variable,
        ).grid(row=2, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            create_schedule_frame,
            text="Today",
            command=self.today_button
        ).grid(row=1, column=3, sticky='nsew')

        tk.Button(
            create_schedule_frame,
            text="Add",
            command=self.add_a_day_button
        ).grid(row=2, column=3, sticky='nsew')

        tk.Button(
            create_schedule_frame,
            text="Subtract",
            command=self.subtract_a_day_button
        ).grid(row=3, column=3, sticky='nsew')

        tk.Button(
            create_schedule_frame,
            text="Confirm",
            command=self.confirm_button
        ).grid(row=5, columnspan=2, column=0, sticky='nsew')

        tk.Button(
            create_schedule_frame,
            text="Cancel",
            command=self.cancel_button
        ).grid(row=5, columnspan=2, column=2, sticky='nsew')

        self.current_frame = create_schedule_frame
        return create_schedule_frame

        # Button Frames

    def today_button(self):
        full_date_object = datetime.now()
        yy_mm_dd_object = full_date_object.date()
        self.create_start_date_variable.set(yy_mm_dd_object)
        self.create_end_date_variable.set(yy_mm_dd_object)
        self.num_of_days.set("0")

    def add_a_day_button(self):
        if self.validate_date_difference():
            initial_date_str = self.create_start_date_variable.get()
            initial_date_object = datetime.strptime(initial_date_str, '%Y-%m-%d')
        else:
            initial_date_str = self.create_end_date_variable.get()
            initial_date_object = datetime.strptime(initial_date_str, '%Y-%m-%d')

        # Variables to that will be used calculate days
        initial_day_str = self.create_start_date_variable.get()
        initial_day_object = datetime.strptime(initial_day_str, '%Y-%m-%d')

        new_date_object = initial_date_object + timedelta(days=1)
        self.create_end_date_variable.set(new_date_object.strftime('%Y-%m-%d'))
        days_object = new_date_object - initial_day_object
        self.num_of_days.set(days_object.days)

    def subtract_a_day_button(self):
        if self.validate_date_difference():
            initial_date_str = self.create_start_date_variable.get()
            initial_date_object = datetime.strptime(initial_date_str, '%Y-%m-%d')
        else:
            initial_date_str = self.create_end_date_variable.get()
            initial_date_object = datetime.strptime(initial_date_str, '%Y-%m-%d')

        # Variables to calculate days
        initial_day_str = self.create_start_date_variable.get()
        initial_day_object = datetime.strptime(initial_day_str, '%Y-%m-%d')
        today_object = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if initial_date_object > today_object:
            new_date_object = initial_date_object - timedelta(days=1)
            self.create_end_date_variable.set(new_date_object.strftime('%Y-%m-%d'))
            days_object = new_date_object - initial_day_object
            self.num_of_days.set(days_object.days)
        else:
            pass

    def confirm_button(self):
        if not self.create_start_date_variable.get():
            showwarning(title="Error!", message="Start Date is Empty!")
        elif not self.create_end_date_variable.get():
            showwarning(title="Error!", message="End Date is Empty!")
        else:
            if not self.validate_date():
                showwarning(title="Error!", message="Please try again!")
            else:
                confirm_create = askyesno("Confirm?", "You will add a new schedule.\nConfirm?")
                if confirm_create:
                    self.sched_sql.insert_a_schedule(self.create_start_date_variable.get(),
                                                     self.create_end_date_variable.get()
                                                     )
                    self.destroy()

    def cancel_button(self):
        self.destroy()

    def validate_date(self):
        start_date_str = self.create_start_date_variable.get()
        end_date_str = self.create_end_date_variable.get()

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').replace(hour=0,
                                                                               minute=0,
                                                                               second=0,
                                                                               microsecond=0)
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            if start_date >= end_date:
                showwarning(title='Error', message="Start date cannot be greater than end date")
                return False
            else:
                return True
        except ValueError:
            showwarning(title='Error', message="Invalid date format (use YYYY-MM-DD)")

    def validate_date_difference(self):
        start_date_str = self.create_start_date_variable.get()
        end_date_str = self.create_end_date_variable.get()
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            if start_date >= end_date:
                return True
            else:
                return False
        except ValueError:
            showwarning(title='Error', message="Invalid date format (use YYYY-MM-DD)")


class ScheduleModificationWindow(tk.Toplevel):
    def __init__(self, root, selected_sched):
        super().__init__(root)

        # Window Configurations
        self.geometry('500x200')
        self.minsize(400, 200)
        self.title('Schedule Creation')

        # Variables
        self.selected_schedule_id = tk.StringVar()
        self.modify_start_date_variable = tk.StringVar()
        self.modify_end_date_variable = tk.StringVar()
        self.num_of_days = tk.StringVar()
        self.current_frame = ttk.Frame()
        self.sched_sql = ScheduleTabSQL()

        self.selected_schedule_id.set(selected_sched)

        # Frame Placement
        self.modify_basic_schedule_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

        self.grab_set()

    def modify_basic_schedule_information_frame(self):
        modify_schedule_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        modify_schedule_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        modify_schedule_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        self.retrieve_schedule_information()

        # Labels
        ttk.Label(modify_schedule_frame, text="Schedule ID:").grid(row=0, column=0, sticky='nsew')
        ttk.Label(modify_schedule_frame, textvariable=self.selected_schedule_id).grid(row=0, column=1, sticky='nsew')
        ttk.Label(modify_schedule_frame, text="Start Date").grid(row=1, column=0, sticky='nsew')
        ttk.Label(modify_schedule_frame, text="End Date").grid(row=2, column=0, sticky='nsew')
        ttk.Label(modify_schedule_frame, text='Number of Days').grid(row=3, column=0, sticky='nsew')
        ttk.Label(modify_schedule_frame, textvariable=self.num_of_days).grid(row=3, column=1, sticky='nsew')

        # Entries
        ttk.Entry(
            modify_schedule_frame,
            textvariable=self.modify_start_date_variable,
        ).grid(row=1, column=1, sticky='nsew')

        ttk.Entry(
            modify_schedule_frame,
            textvariable=self.modify_end_date_variable,
        ).grid(row=2, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            modify_schedule_frame,
            text="Today",
            command=self.today_button
        ).grid(row=1, column=3, sticky='nsew')

        tk.Button(
            modify_schedule_frame,
            text="Add",
            command=self.add_a_day_button
        ).grid(row=2, column=3, sticky='nsew')

        tk.Button(
            modify_schedule_frame,
            text="Subtract",
            command=self.subtract_a_day_button
        ).grid(row=3, column=3, sticky='nsew')

        tk.Button(
            modify_schedule_frame,
            text="Confirm",
            command=self.confirm_button
        ).grid(row=5, columnspan=2, column=0, sticky='nsew')

        tk.Button(
            modify_schedule_frame,
            text="Cancel",
            command=self.cancel_button
        ).grid(row=5, columnspan=2, column=2, sticky='nsew')

        self.current_frame = modify_schedule_frame
        return modify_schedule_frame

        # Button Frames

    def today_button(self):
        full_date_object = datetime.now()
        yy_mm_dd_object = full_date_object.date()
        self.modify_start_date_variable.set(yy_mm_dd_object)
        self.modify_end_date_variable.set(yy_mm_dd_object)
        self.num_of_days.set("0")

    def add_a_day_button(self):
        if self.validate_date_difference():
            initial_date_str = self.modify_start_date_variable.get()
            initial_date_object = datetime.strptime(initial_date_str, '%Y-%m-%d')
        else:
            initial_date_str = self.modify_end_date_variable.get()
            initial_date_object = datetime.strptime(initial_date_str, '%Y-%m-%d')

        # Variables to that will be used calculate days
        initial_day_str = self.modify_start_date_variable.get()
        initial_day_object = datetime.strptime(initial_day_str, '%Y-%m-%d')

        new_date_object = initial_date_object + timedelta(days=1)
        self.modify_end_date_variable.set(new_date_object.strftime('%Y-%m-%d'))
        days_object = new_date_object - initial_day_object
        self.num_of_days.set(days_object.days)

    def subtract_a_day_button(self):
        if self.validate_date_difference():
            initial_date_str = self.modify_start_date_variable.get()
            initial_date_object = datetime.strptime(initial_date_str, '%Y-%m-%d')
        else:
            initial_date_str = self.modify_end_date_variable.get()
            initial_date_object = datetime.strptime(initial_date_str, '%Y-%m-%d')

        # Variables to calculate days
        initial_day_str = self.modify_start_date_variable.get()
        initial_day_object = datetime.strptime(initial_day_str, '%Y-%m-%d')
        today_object = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if initial_date_object > today_object:
            new_date_object = initial_date_object - timedelta(days=1)
            self.modify_end_date_variable.set(new_date_object.strftime('%Y-%m-%d'))
            days_object = new_date_object - initial_day_object
            self.num_of_days.set(days_object.days)
        else:
            pass

    def confirm_button(self):
        if not self.modify_start_date_variable.get():
            showwarning(title="Error!", message="Start Date is Empty!")
        elif not self.modify_end_date_variable.get():
            showwarning(title="Error!", message="End Date is Empty!")
        else:
            if not self.validate_date():
                showwarning(title="Error!", message="Please try again!")
            else:
                confirm_create = askyesno("Confirm?",
                                          message=f"You will update the schedule ID {self.selected_schedule_id.get()}."
                                                  f"\nConfirm?")
                if confirm_create:
                    self.sched_sql.update_a_schedule(self.selected_schedule_id.get(),
                                                     self.modify_start_date_variable.get(),
                                                     self.modify_end_date_variable.get()
                                                     )
                    self.destroy()

    def cancel_button(self):
        self.destroy()

    def validate_date(self):
        start_date_str = self.modify_start_date_variable.get()
        end_date_str = self.modify_end_date_variable.get()

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').replace(hour=0,
                                                                               minute=0,
                                                                               second=0,
                                                                               microsecond=0)
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            if start_date >= end_date:
                showwarning(title='Error', message="Start date cannot be greater than end date")
                return False
            else:
                return True
        except ValueError:
            showwarning(title='Error', message="Invalid date format (use YYYY-MM-DD)")

    def validate_date_difference(self):
        start_date_str = self.modify_start_date_variable.get()
        end_date_str = self.modify_end_date_variable.get()
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            if start_date >= end_date:
                return True
            else:
                return False
        except ValueError:
            showwarning(title='Error', message="Invalid date format (use YYYY-MM-DD)")

    def retrieve_schedule_information(self):
        retrieved_schedule = self.sched_sql.retrieve_a_schedule(self.selected_schedule_id.get())

        self.modify_start_date_variable.set(retrieved_schedule[0])
        self.modify_end_date_variable.set(retrieved_schedule[1])


class EmployeeCreationWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        self.geometry('500x200')
        self.minsize(400, 200)
        self.title("New Employee")

        # Basic Employee Information Variables
        self.firstname_variable = tk.StringVar()
        self.lastname_variable = tk.StringVar()
        self.email_variable = tk.StringVar()
        self.phone_number_variable = tk.StringVar()
        self.manager_information_variable = tk.StringVar()
        self.fullname_variable = tk.StringVar()
        self.manager_id = tk.IntVar()
        self.job_id_variable = tk.IntVar()

        self.schedules = []
        self.managers = []
        self.jobs = []
        self.job_position_variable = tk.StringVar()
        self.assign_schedule_variable = tk.StringVar()
        self.schedules_combo = ttk.Combobox()
        self.manager_variable = tk.StringVar()
        self.manager_combo = ttk.Combobox()
        self.job_combo = ttk.Combobox

        self.sched_sql = ScheduleTabSQL()
        self.employee_sql = EmployeeTabSQL()
        self.current_frame = ttk.Frame()
        self.create_basic_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

        self.grab_set()

    def create_basic_information_frame(self):
        """First Frame, entry fields for simple informations"""
        create_employee_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        create_employee_frame.columnconfigure((0, 1), weight=1, uniform='a')
        create_employee_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        ttk.Label(create_employee_frame, text="* First Name:").grid(row=0, column=0, sticky='nsew')
        ttk.Label(create_employee_frame, text="* Last Name:").grid(row=1, column=0, sticky='nsew')
        ttk.Label(create_employee_frame, text="* Email:").grid(row=2, column=0, sticky='nsew')
        ttk.Label(create_employee_frame, text="* Phone Number:").grid(row=3, column=0, sticky='nsew')
        ttk.Label(create_employee_frame, text="* Job:").grid(row=4, column=0, sticky='nsew')

        # Entries
        ttk.Entry(
            create_employee_frame,
            textvariable=self.firstname_variable
        ).grid(row=0, column=1, sticky='ew')

        ttk.Entry(
            create_employee_frame,
            textvariable=self.lastname_variable
        ).grid(row=1, column=1, sticky='ew')

        ttk.Entry(
            create_employee_frame,
            textvariable=self.email_variable
        ).grid(row=2, column=1, sticky='ew')

        ttk.Entry(
            create_employee_frame,
            textvariable=self.phone_number_variable
        ).grid(row=3, column=1, sticky='ew')

        self.job_combo = ttk.Combobox(
            create_employee_frame,
            textvariable=self.job_position_variable,
            state='readonly'
        )
        self.populate_job_list()
        self.job_combo.grid(row=4, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            create_employee_frame,
            text="Next",
            command=self.next_to_assign_schedule_button
        ).grid(row=8, columnspan=2, column=0, sticky='nsew')
        tk.Button(
            create_employee_frame,
            text="Cancel",
            command=self.cancel_create_button
        ).grid(row=8, column=2, sticky='nsew')

        self.current_frame = create_employee_frame
        return create_employee_frame

    def assign_schedule_frame(self):
        """Second Frame, assigns schedules or manager to employee"""
        assign_sched_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        assign_sched_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        assign_sched_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        ttk.Label(assign_sched_frame, text="Manager: ").grid(row=0, column=0, sticky='nsew')

        self.manager_combo = ttk.Combobox(assign_sched_frame,
                                          textvariable=self.manager_variable,
                                          state='readonly')
        self.populate_manager_list()
        self.manager_combo.grid(row=0, columnspan=2, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            assign_sched_frame,
            text="Next",
            command=self.next_to_confirm_info_button
        ).grid(row=8, columnspan=2, column=0, sticky='nsew')
        tk.Button(
            assign_sched_frame,
            text="Cancel",
            command=self.cancel_create_button
        ).grid(row=8, column=2, sticky='nsew')

        self.current_frame = assign_sched_frame
        return assign_sched_frame

    def confirm_employee_information_frame(self):
        """Third Frame, visualize whether the information entered are correct"""
        confirm_information_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        confirm_information_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        confirm_information_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        ttk.Label(confirm_information_frame, text="Name:").grid(row=0, column=0, sticky='nsew')
        ttk.Label(confirm_information_frame, text="Email:").grid(row=1, column=0, sticky='nsew')
        ttk.Label(confirm_information_frame, text="Phone Number:").grid(row=2, column=0, sticky='nsew')
        ttk.Label(confirm_information_frame, text="Job:").grid(row=3, column=0, sticky='nsew')
        ttk.Label(confirm_information_frame, text="Manager:").grid(row=4, column=0, sticky='nsew')

        ttk.Label(confirm_information_frame,
                  textvariable=self.fullname_variable
                  ).grid(row=0, column=1, sticky='nsew')
        ttk.Label(confirm_information_frame,
                  textvariable=self.email_variable
                  ).grid(row=1, column=1, sticky='nsew')
        ttk.Label(confirm_information_frame,
                  textvariable=self.phone_number_variable
                  ).grid(row=2, column=1, sticky='nsew')
        ttk.Label(confirm_information_frame,
                  textvariable=self.job_position_variable
                  ).grid(row=3, column=1, sticky='nsew')
        ttk.Label(confirm_information_frame,
                  textvariable=self.manager_information_variable
                  ).grid(row=4, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            confirm_information_frame,
            text="Confirm",
            command=self.confirm_info_button
        ).grid(row=6, columnspan=2, column=0, sticky='nsew')
        tk.Button(
            confirm_information_frame,
            text="Cancel",
            command=self.cancel_create_button
        ).grid(row=6, column=3, sticky='nsew')

        self.current_frame = confirm_information_frame
        return confirm_information_frame

    # Employees
    ##########################################################
    # Button Functions

    def next_to_assign_schedule_button(self):
        """First Frame 'Next' Button"""
        self.current_frame.pack_forget()
        self.assign_schedule_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def next_to_confirm_info_button(self):
        """Second Frame 'Next' Button"""
        self.fullname_variable.set(f'{self.firstname_variable.get()} {self.lastname_variable.get()}')

        # Gets the manager name and detail
        self.manager_id.set(self.get_employee_id_from_dictionary(self.manager_combo.current()))
        manager_id = self.manager_id.get()
        manager_details = self.get_employee_from_id(manager_id)
        manager_name = f'{manager_details["firstname"]} {manager_details["lastname"]}'
        self.manager_information_variable.set(manager_name)

        print(self.job_position_variable.get())

        self.current_frame.pack_forget()
        self.confirm_employee_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def confirm_info_button(self):
        """Fourth Frame 'Submit' Button"""
        self.job_id_variable.set(self.get_job_id())
        confirm = askyesno(title="Confirm Guest?", message="Confirm employee?")
        if confirm:
            self.employee_sql.create_an_employee(self.firstname_variable.get(),
                                                 self.lastname_variable.get(),
                                                 self.email_variable.get(),
                                                 self.phone_number_variable.get(),
                                                 self.job_id_variable.get(),
                                                 self.manager_id.get())
            self.destroy()

    def cancel_create_button(self):
        """Button to cancel employee creation window"""
        self.destroy()

    # Button Functions
    ##########################################################
    # Logics

    def populate_manager_list(self):
        """Fills up list for Manager"""
        retrieved_employees = self.employee_sql.retrieve_all_employees()
        managers_for_list = []

        for employees in retrieved_employees:
            if employees[5] == 4:
                manager_details = {"id": employees[0],
                                   "firstname": employees[1],
                                   "lastname": employees[2]
                                   }
                self.managers.append(manager_details)
                managers_for_list.append(f'{employees[1]} {employees[2]}')

        self.manager_combo['values'] = managers_for_list

    def populate_job_list(self):
        retrieved_jobs = self.employee_sql.retrieve_jobs()
        jobs_for_list = []

        for jobs in retrieved_jobs:
            job_details = {"id": jobs[0], "job_title": jobs[1], "job_department": jobs[2]}
            self.jobs.append(job_details)
            jobs_for_list.append(jobs[1])

        self.job_combo['values'] = jobs_for_list

    def get_employee_id_from_dictionary(self, index):
        if index >= 0:
            selected_manager = self.managers[index]
            manager_id = selected_manager['id']
            return manager_id

    def get_employee_from_id(self, id_index):
        for employee in self.managers:
            if employee['id'] == id_index:
                return employee

    def get_job_id(self):
        job_name = self.job_combo.get()
        for jobs in self.jobs:
            if jobs['job_title'] == job_name:
                return jobs['id']


class EmployeeModificationWindow(tk.Toplevel):
    def __init__(self, root, selected_employee_id):
        super().__init__(root)

        self.geometry('500x200')
        self.minsize(400, 200)
        self.title("New Employee")

        self.selected_employee_id = tk.IntVar()
        self.selected_employee_id.set(selected_employee_id)

        # Basic Employee Information Variables
        self.firstname_variable = tk.StringVar()
        self.lastname_variable = tk.StringVar()
        self.email_variable = tk.StringVar()
        self.phone_number_variable = tk.StringVar()
        self.job_position_variable = tk.StringVar()
        self.manager_information_variable = tk.StringVar()
        self.fullname_variable = tk.StringVar()
        self.manager_id = tk.IntVar()
        self.job_id_variable = tk.IntVar()
        self.current_job_id_var = tk.IntVar()

        self.schedules = []
        self.managers = []
        self.jobs = []

        self.assign_schedule_variable = tk.StringVar()
        self.schedules_combo = ttk.Combobox()
        self.manager_variable = tk.StringVar()
        self.manager_combo = ttk.Combobox()
        self.job_combo = ttk.Combobox

        self.sched_sql = ScheduleTabSQL()
        self.employee_sql = EmployeeTabSQL()

        self.retrieve_employee_information()

        self.current_frame = ttk.Frame()
        self.modify_basic_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

        self.grab_set()

    def modify_basic_information_frame(self):
        """First Frame, entry fields for simple information"""
        modify_employee_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        modify_employee_frame.columnconfigure((0, 1), weight=1, uniform='a')
        modify_employee_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        ttk.Label(modify_employee_frame, text="Employee ID:").grid(row=0, column=0, sticky='nsew')
        ttk.Label(modify_employee_frame, text="* First Name:").grid(row=1, column=0, sticky='nsew')
        ttk.Label(modify_employee_frame, text="* Last Name:").grid(row=2, column=0, sticky='nsew')
        ttk.Label(modify_employee_frame, text="* Email:").grid(row=3, column=0, sticky='nsew')
        ttk.Label(modify_employee_frame, text="* Phone Number:").grid(row=4, column=0, sticky='nsew')
        ttk.Label(modify_employee_frame, text="* Job:").grid(row=5, column=0, sticky='nsew')

        # Entries
        ttk.Label(
            modify_employee_frame,
            textvariable=self.selected_employee_id
        ).grid(row=0, column=1, sticky='ew')

        ttk.Entry(
            modify_employee_frame,
            textvariable=self.firstname_variable
        ).grid(row=1, column=1, sticky='ew')

        ttk.Entry(
            modify_employee_frame,
            textvariable=self.lastname_variable
        ).grid(row=2, column=1, sticky='ew')

        ttk.Entry(
            modify_employee_frame,
            textvariable=self.email_variable
        ).grid(row=3, column=1, sticky='ew')

        ttk.Entry(
            modify_employee_frame,
            textvariable=self.phone_number_variable
        ).grid(row=4, column=1, sticky='ew')

        self.job_combo = ttk.Combobox(
            modify_employee_frame,
            textvariable=self.job_position_variable,
            state='readonly'
        )
        self.populate_job_list()
        self.job_combo.current(self.current_job_id_var.get() - 1)
        self.job_combo.grid(row=4, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            modify_employee_frame,
            text="Next",
            command=self.next_to_assign_schedule_button
        ).grid(row=8, columnspan=2, column=0, sticky='nsew')
        tk.Button(
            modify_employee_frame,
            text="Cancel",
            command=self.cancel_create_button
        ).grid(row=8, column=2, sticky='nsew')

        self.current_frame = modify_employee_frame
        return modify_employee_frame

    def assigns_manager_frame(self):
        """Second Frame, manager to employee"""
        reassign_manager_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        reassign_manager_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        reassign_manager_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        ttk.Label(reassign_manager_frame, text="Manager: ").grid(row=0, column=0, sticky='nsew')

        self.manager_combo = ttk.Combobox(reassign_manager_frame,
                                          textvariable=self.manager_variable,
                                          state='readonly')

        if self.is_employee_a_manager():
            self.manager_combo.configure(state='disabled')
            ttk.Label(reassign_manager_frame,
                      text="Employee is a manager").grid(row=1, columnspan=2, column=1, sticky='ew')
        self.manager_combo.grid(row=0, columnspan=2, column=1, sticky='nsew')
        self.populate_manager_list()

        # Buttons
        tk.Button(
            reassign_manager_frame,
            text="Next",
            command=self.next_to_confirm_info_button
        ).grid(row=8, columnspan=2, column=0, sticky='nsew')
        tk.Button(
            reassign_manager_frame,
            text="Cancel",
            command=self.cancel_create_button
        ).grid(row=8, column=2, sticky='nsew')

        self.current_frame = reassign_manager_frame
        return reassign_manager_frame

    def confirm_employee_information_frame(self):
        """Third Frame, visualize whether the information entered are correct"""
        confirm_information_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        confirm_information_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        confirm_information_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        ttk.Label(confirm_information_frame, text="Name:").grid(row=0, column=0, sticky='nsew')
        ttk.Label(confirm_information_frame, text="Email:").grid(row=1, column=0, sticky='nsew')
        ttk.Label(confirm_information_frame, text="Phone Number:").grid(row=2, column=0, sticky='nsew')
        ttk.Label(confirm_information_frame, text="Job:").grid(row=3, column=0, sticky='nsew')
        ttk.Label(confirm_information_frame, text="Manager:").grid(row=4, column=0, sticky='nsew')

        ttk.Label(confirm_information_frame,
                  textvariable=self.fullname_variable
                  ).grid(row=0, column=1, sticky='nsew')
        ttk.Label(confirm_information_frame,
                  textvariable=self.email_variable
                  ).grid(row=1, column=1, sticky='nsew')
        ttk.Label(confirm_information_frame,
                  textvariable=self.phone_number_variable
                  ).grid(row=2, column=1, sticky='nsew')
        ttk.Label(confirm_information_frame,
                  textvariable=self.job_position_variable
                  ).grid(row=3, column=1, sticky='nsew')
        ttk.Label(confirm_information_frame,
                  textvariable=self.manager_information_variable
                  ).grid(row=4, column=1, sticky='nsew')

        # Buttons
        tk.Button(
            confirm_information_frame,
            text="Confirm",
            command=self.confirm_info_button
        ).grid(row=6, columnspan=2, column=0, sticky='nsew')
        tk.Button(
            confirm_information_frame,
            text="Cancel",
            command=self.cancel_create_button
        ).grid(row=6, column=3, sticky='nsew')

        self.current_frame = confirm_information_frame
        return confirm_information_frame

    # Employees
    ##########################################################
    # Button Functions

    def next_to_assign_schedule_button(self):
        """First Frame 'Next' Button"""
        a = self.firstname_variable.get()
        b = self.lastname_variable.get()
        c = self.email_variable.get()
        d = self.phone_number_variable.get()
        e = self.job_position_variable.get()

        if [x for x in (a, b, c, d, e) if x == ""]:
            showwarning(title="Error!", message="Please fill all the entries!")
        else:
            self.current_frame.pack_forget()
            self.assigns_manager_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def next_to_confirm_info_button(self):
        """Second Frame 'Next' Button"""
        self.fullname_variable.set(f'{self.firstname_variable.get()} {self.lastname_variable.get()}')
        if not self.is_employee_a_manager():
            if not self.manager_variable.get():
                showwarning(title="Error!", message="Please select a manager!")
            else:
                # Gets the manager name and detail
                self.manager_id.set(self.get_employee_id_from_dictionary(self.manager_combo.current()))
                manager_id = self.manager_id.get()
                manager_details = self.get_employee_from_id(manager_id)
                manager_name = f'{manager_details["firstname"]} {manager_details["lastname"]}'
                self.manager_information_variable.set(manager_name)
                self.current_frame.pack_forget()
                self.confirm_employee_information_frame().pack(expand=True, fill='both', padx=5, pady=5)
        else:
            self.current_frame.pack_forget()
            self.confirm_employee_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

    def confirm_info_button(self):
        """Fourth Frame 'Submit' Button"""
        self.job_id_variable.set(self.get_job_id())
        confirm = askyesno(title="Confirm Guest?", message="Confirm update?")
        if confirm:
            self.employee_sql.update_an_employee(self.firstname_variable.get(),
                                                 self.lastname_variable.get(),
                                                 self.email_variable.get(),
                                                 self.phone_number_variable.get(),
                                                 self.job_id_variable.get(),
                                                 self.manager_id.get(),
                                                 self.selected_employee_id.get()
                                                 )
            if self.is_employee_a_manager():
                self.employee_sql.update_manager_id_if_updated(self.selected_employee_id.get())
            self.destroy()

    def cancel_create_button(self):
        """Button to cancel employee creation window"""
        self.destroy()

    # Button Functions
    ##########################################################
    # Logics

    def is_employee_a_manager(self):
        """If job chosen is manager, return True"""
        if self.get_job_id() == 4:
            return True
        else:
            return False

    def retrieve_employee_information(self):
        retrieved_employee = self.employee_sql.retrieve_a_specific_employee(self.selected_employee_id.get())

        self.firstname_variable.set(retrieved_employee[1])
        self.lastname_variable.set(retrieved_employee[2])
        self.email_variable.set(retrieved_employee[3])
        self.phone_number_variable.set(retrieved_employee[4])
        self.current_job_id_var.set(retrieved_employee[5])

    def populate_manager_list(self):
        """Fills up list for Manager"""
        retrieved_employees = self.employee_sql.retrieve_all_employees()
        managers_for_list = []

        for employees in retrieved_employees:
            if employees[5] == 4:
                if employees[0] is not self.selected_employee_id.get():
                    manager_details = {"id": employees[0],
                                       "firstname": employees[1],
                                       "lastname": employees[2]
                                       }
                    self.managers.append(manager_details)
                    managers_for_list.append(f'{employees[1]} {employees[2]}')

        self.manager_combo['values'] = managers_for_list

    def populate_job_list(self):
        retrieved_jobs = self.employee_sql.retrieve_jobs()
        jobs_for_list = []

        for jobs in retrieved_jobs:
            job_details = {"id": jobs[0], "job_title": jobs[1], "job_department": jobs[2]}
            self.jobs.append(job_details)
            jobs_for_list.append(jobs[1])

        self.job_combo['values'] = jobs_for_list

    def get_employee_id_from_dictionary(self, index):
        if index >= 0:
            selected_manager = self.managers[index]
            manager_id = selected_manager['id']
            return manager_id

    def get_employee_from_id(self, id_index):
        for employee in self.managers:
            if employee['id'] == id_index:
                return employee

    def get_job_id(self):
        job_name = self.job_combo.get()
        for jobs in self.jobs:
            if jobs['job_title'] == job_name:
                return jobs['id']


class JobsCreationWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        self.geometry('500x200')
        self.minsize(400, 200)
        self.title("New Job")

        self.jobs_title_variable = tk.StringVar()
        self.jobs_depart_variable = tk.StringVar()

        self.jobs_sql = JobsTabSQL()

        self.current_frame = ttk.Frame()
        self.create_basic_information_frame().pack(expand=True, fill='both', padx=5, pady=5)

        self.grab_set()

    def create_basic_information_frame(self):
        new_job_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        new_job_frame.columnconfigure((0, 1), weight=1, uniform='a')
        new_job_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        ttk.Label(new_job_frame, text="Jobs Title").grid(row=0, column=0, sticky='nsew')
        ttk.Label(new_job_frame, text="Jobs Department").grid(row=1, column=0, sticky='nsew')

        ttk.Entry(new_job_frame, textvariable=self.jobs_title_variable).grid(row=0, column=1, sticky='ew')
        ttk.Entry(new_job_frame, textvariable=self.jobs_depart_variable).grid(row=1, column=1, sticky='ew')

        tk.Button(new_job_frame, text="Confirm", command=self.confirm_job_button).grid(row=4, column=0, sticky='ew')
        tk.Button(new_job_frame, text="Cancel", command=self.cancel_button).grid(row=4, column=1, sticky='ew')

        return new_job_frame

    # Frames
    ##########################################################
    # Button Functions

    def confirm_job_button(self):
        a = self.jobs_title_variable.get()
        b = self.jobs_depart_variable.get()
        if [x for x in (a, b) if x == ""]:
            showwarning(title="Error!", message="Please fill in the entries!")
        else:
            confirm_create = askyesno(title="Create job?", message="You are about to create a job.\nConfirm?")
            if confirm_create:
                if self.jobs_sql.create_a_job(self.jobs_title_variable.get(),
                                              self.jobs_depart_variable.get()):
                    showinfo(title="Task Successful!", message="Job created successfully!")
                    self.destroy()
                else:
                    showerror(title="Task Unsuccessful!", message="Something went wrong!")

    def cancel_button(self):
        self.destroy()


class AssignEmployeeToBill(tk.Toplevel):
    def __init__(self, root, bill_id_index):
        super().__init__(root)

        self.geometry('500x200')
        self.minsize(400, 200)
        self.title("New Job")

        self.bills_id_variable = tk.IntVar()
        self.employee_id_variable = tk.IntVar()
        self.employees = []
        self.employee_combo = ttk.Combobox()
        self.employee_combo_variable = tk.StringVar()

        self.bills_id_variable.set(bill_id_index)
        self.bills_sql = BillTabSQL()
        self.employee_sql = EmployeeTabSQL

        self.current_frame = ttk.Frame()
        self.assign_employee_frame().pack(expand=True, fill='both', padx=5, pady=5)
        self.grab_set()

    def assign_employee_frame(self):
        emp_combo_frame = ttk.Frame(self, borderwidth=10, relief='groove')
        emp_combo_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
        emp_combo_frame.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')

        ttk.Label(emp_combo_frame, text="Bill ID:").grid(row=0, column=0, sticky='nsew')
        ttk.Label(emp_combo_frame, text="Employee:").grid(row=1, column=0, sticky='nsew')

        tk.Entry(
            emp_combo_frame,
            textvariable=self.bills_id_variable,
            state='readonly'
        ).grid(row=0, column=1, sticky='ew')

        self.employee_combo = ttk.Combobox(
            emp_combo_frame,
            textvariable=self.employee_combo_variable,
            state='readonly'
        )

        self.employee_combo.grid(row=1, columnspan=2, column=1, sticky='ew')

        tk.Button(
            emp_combo_frame,
            text="Confirm",
            command=self.bills_confirm_button).grid(row=3, columnspan=2, column=0, sticky='ew')
        tk.Button(
            emp_combo_frame,
            text="Cancel",
            command=self.bills_cancel_button).grid(row=3, column=2, sticky='ew')

        self.populate_employee_combo()

        return emp_combo_frame

    # Frames
    ##########################################################
    # Button Functions

    def bills_confirm_button(self):
        self.retrieve_employee_id_from_selected_combo()
        confirm_assign = askyesno(title="Employee Assignment?",
                                  message=f"You will assign an employee to bill ID: {self.bills_id_variable.get()}\n"
                                          f"Confirm?")
        if confirm_assign:
            self.bills_sql.update_bill_record_employee(self.bills_id_variable.get(),
                                                       self.employee_id_variable.get()
                                                       )
            self.destroy()

    def bills_cancel_button(self):
        self.destroy()

    # Button Functions
    ##########################################################
    # Logic

    def populate_employee_combo(self):
        retrieved_employees = self.employee_sql.retrieve_employees_to_populate_list(self)
        employees_for_list = []
        for employees in retrieved_employees:
            employees_details = {"id": employees[0],
                                 "fullname": employees[1],
                                 "job_title": employees[2]
                                 }
            self.employees.append(employees_details)
            employees_for_list.append(f'{employees[1]}: {employees[2]}')

        self.employee_combo['values'] = employees_for_list

    def retrieve_employee_id_from_selected_combo(self):
        selected_employee = (self.employee_combo.get()).split(":")
        selected_emp_name = selected_employee[0]

        for item in self.employees:
            if item['fullname'] == selected_emp_name:
                self.employee_id_variable.set(item['id'])

        return selected_emp_name


App()
