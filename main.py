import tkinter as tk
from tkinter import ttk
import sql_connection


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
        self.add(self.guest_tab, text='Guests')
        self.add(self.room_tab, text='Rooms')
        self.add(self.employee_tab, text='Employees')
        self.add(self.schedule_tab, text='Schedules')

        self.pack(expand=True, fill="both")


class GuestTab(ttk.Frame):
    def __init__(self, root):
        super().__init__(master=root)

        # Variables Initialization
        self.guest_lists = None
        self.guest_room_number = None
        self.guest_phone_number = None
        self.guest_email = None
        self.guest_last_name = None
        self.guest_id_variable = None
        self.guest_first_name = None

        self.id_entry = None
        self.first_name_entry = None
        self.last_name_entry = None

        self.email_entry = None
        self.phone_entry = None
        self.room_entry = None

        self.guests_list().pack(side='left', fill='y', padx=5, pady=5)
        self.guests_widgets().pack(side='left', expand=True, fill='both', padx=5, pady=5)
        self.pack()

    def guests_list(self):
        guest_list_frame = ttk.Frame(master=self)
        guest_list_frame.configure(borderwidth=10, relief='groove')
        guest_items = tk.Variable()
        ttk.Label(guest_list_frame,
                  text="Guests List",
                  font="Arial").pack()
        self.guest_lists = tk.Listbox(guest_list_frame,
                                      listvariable=guest_items
                                      )

        # Retrieves Guests
        self.populate_lists()
        self.guest_lists.pack(expand=True, fill='y')

        # Scrollbar
        x_list_scrollbar = tk.Scrollbar(guest_list_frame, orient=tk.HORIZONTAL)
        self.guest_lists.config(xscrollcommand=x_list_scrollbar.set)
        x_list_scrollbar.config(command=self.guest_lists.xview)
        x_list_scrollbar.pack(fill='x')

        return guest_list_frame

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
        tk.Button(tools_frame,
                  text='Open',
                  command=self.open_guest_button
                  ).pack(side='left', expand=True, fill='both', padx=2)
        # tk.Button(tools_frame, text='Modify', command=functionality.modify_button_guest).pack(
        #     side='left', expand=True, fill='both', padx=2
        # )
        # tk.Button(tools_frame, text='Delete', command=functionality.delete_button_guest).pack(
        #     side='left', expand=True, fill='both', padx=2
        # )

        tools_frame.pack(fill='x')
        return tools_frame

    def guest_details(self, frame):
        details_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')
        details_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        details_frame.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')

        self.guest_id_variable = tk.StringVar()
        self.guest_first_name = tk.StringVar()
        self.guest_last_name = tk.StringVar()
        self.guest_email = tk.StringVar()
        self.guest_phone_number = tk.StringVar()
        self.guest_room_number = tk.StringVar()

        tk.Label(details_frame, text='Guest ID:').grid(row=0, columnspan=2, column=0, sticky='nsew')
        self.id_entry = tk.Entry(details_frame, textvariable=self.guest_id_variable, state='disabled')
        self.id_entry.grid(row=0, column=2, sticky='ew')

        tk.Label(details_frame, text='First Name:').grid(row=1, column=0, sticky='nsew')
        self.first_name_entry = tk.Entry(details_frame, textvariable=self.guest_first_name)
        self.first_name_entry.grid(row=1, column=1, sticky='ew')

        tk.Label(details_frame, text='Last Name:').grid(row=1, column=2, sticky='nsew')
        self.last_name_entry = tk.Entry(details_frame, textvariable=self.guest_last_name)
        self.last_name_entry.grid(row=1, column=3, sticky='ew')

        tk.Label(details_frame, text='Email:').grid(row=2, column=0, sticky='nsew')
        self.email_entry = tk.Entry(details_frame, textvariable=self.guest_email)
        self.email_entry.grid(row=2, column=1, sticky='ew')

        tk.Label(details_frame, text='Phone Number:').grid(row=2, column=2, sticky='nsew')
        self.phone_entry = tk.Entry(details_frame, textvariable=self.guest_phone_number)
        self.phone_entry.grid(row=2, column=3, sticky='ew')

        tk.Label(details_frame, text='Room Number:').grid(row=3, column=0, sticky='nsew')
        self.room_entry = tk.Entry(details_frame, textvariable=self.guest_room_number)
        self.room_entry.grid(row=3, column=1, sticky='ew')

        details_frame.pack(expand=True, fill='both')
        return details_frame

    def populate_lists(self):
        guest_names = sql_connection.retrieve_guest_lists()
        list_size = self.guest_lists.size()
        index_count = list_size
        for i in guest_names:
            self.guest_lists.insert(index_count, f'{i[1]} {i[2]} ID:{i[0]}')
            index_count = index_count + 1

    def new_guest_button(self):
        self.guest_id_variable = self.id_entry.get()
        self.guest_lists.insert(1, self.guest_id_variable)

    def open_guest_button(self):
        guest_id = self.guest_lists.get(self.guest_lists.curselection())
        guest_id = guest_id.split(":")
        retrieved_guest_details = sql_connection.retrieve_a_guest(guest_id[1])
        self.guest_id_variable.set(retrieved_guest_details[0])
        self.guest_first_name.set(retrieved_guest_details[1])
        self.guest_last_name.set(retrieved_guest_details[2])
        self.guest_email.set(retrieved_guest_details[3])
        self.guest_phone_number.set(retrieved_guest_details[4])

        del retrieved_guest_details


class RoomTab(ttk.Frame):
    def __init__(self, root):
        super().__init__(master=root)

        self.room_id_entry = None
        self.room_type_entry = None
        self.room_price_entry = None
        self.room_availability_entry = None
        self.room_managed_by_entry = None

        self.room_id_variable = None
        self.room_number_variable = None
        self.room_type_variable = None
        self.room_price_variable = None
        self.room_availability_variable = None
        self.room_managed_by_variable = None

        self.rooms_treeview = None
        self.rooms_list(self).pack(side='left', expand=True, fill='both')
        self.rooms_widgets(self).pack(side='left', expand=True, fill='both')
        self.pack()

    def rooms_widgets(self, frame):
        rooms_widgets_frame = ttk.Frame(master=frame)
        rooms_widgets_frame.configure(borderwidth=10, relief='groove')

        self.rooms_buttons(rooms_widgets_frame).pack()
        self.rooms_details(rooms_widgets_frame).pack(expand=True, fill='both')

        return rooms_widgets_frame

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
        self.rooms_treeview.pack(expand=True, fill='both')

        self.populate_room_table()

        return rooms_table_frame

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

        # tk.Button(
        #     room_buttons_frame,
        #     text='Assign Schedule',
        #     command=self.assign_schedule_button
        # ).pack(side='left', expand=True, fill='both', padx=2)

        room_buttons_frame.pack(fill='x')
        return room_buttons_frame
        pass

    def rooms_details(self, frame):
        room_details_frame = ttk.Frame(master=frame, borderwidth=10, relief='groove')
        room_details_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        room_details_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')

        self.room_id_variable = tk.StringVar()
        self.room_number_variable = tk.StringVar()
        self.room_type_variable = tk.StringVar()
        self.room_price_variable = tk.StringVar()
        self.room_availability_variable = tk.StringVar()
        self.room_managed_by_variable = tk.StringVar()

        # Entry for Room ID
        tk.Label(room_details_frame, text='Room ID:').grid(row=0, columnspan=2, column=0, sticky='nsew')
        self.room_id_entry = tk.Entry(
            room_details_frame,
            textvariable=self.room_id_variable,
            state='disabled'
        )
        self.room_id_entry.grid(row=0, column=2, sticky='ew')

        # Entry for Room Number
        tk.Label(room_details_frame, text='Room Name:').grid(row=1, column=0, sticky='nsew')
        self.room_number_entry = tk.Entry(
            room_details_frame,
            textvariable=self.room_number_variable
        )
        self.room_number_entry.grid(row=1, columnspan=2, column=2, sticky='ew')

        # Entry for Room Type
        tk.Label(room_details_frame, text='Last Name:').grid(row=2, column=0, sticky='nsew')
        self.room_type_entry = tk.Entry(
            room_details_frame,
            textvariable=self.room_type_variable
        )
        self.room_type_entry.grid(row=2, columnspan=2, column=2, sticky='ew')

        # Entry for Room Price
        tk.Label(room_details_frame, text='Email:').grid(row=3, column=0, sticky='nsew')
        self.room_price_entry = tk.Entry(
            room_details_frame,
            textvariable=self.room_price_variable
        )
        self.room_price_entry.grid(row=3, columnspan=2, column=2, sticky='ew')

        # Entry for Availability
        tk.Label(room_details_frame, text='Phone Number:').grid(row=4, column=0, sticky='nsew')
        self.room_availability_entry = tk.Entry(
            room_details_frame,
            textvariable=self.room_availability_variable
        )
        self.room_availability_entry.grid(row=4, columnspan=2, column=2, sticky='ew')

        # Entry for Maintenance
        tk.Label(room_details_frame, text='Managed by: ').grid(row=5, column=0, sticky='nsew')
        self.room_managed_by_entry = tk.Label(
            room_details_frame,
            textvariable=self.room_managed_by_variable
        )
        self.room_managed_by_entry.grid(row=5, columnspan=2, column=2, sticky='ew')

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
        pass

    def new_room_button(self):
        pass

    def open_room_button(self):
        pass

    def modify_room_button(self):
        pass

    def delete_room_button(self):
        pass


class ScheduleTab(ttk.Frame):
    def __init__(self, root):
        super().__init__(master=root)

        self.schedule_id_variable = tk.StringVar()
        self.schedule_start_date_variable = tk.StringVar()
        self.schedule_end_date_variable = tk.StringVar()
        self.schedule_availability_variable = tk.StringVar()

        self.schedule_id_entry = None
        self.schedule_start_date_entry = None
        self.schedule_end_date_entry = None
        self.schedule_availability_entry = None

        self.schedules_list = None
        self.schedule_list(self).pack(side='left', fill='both')
        self.schedule_widgets(self).pack(side='left', expand=True, fill='both')
        self.pack()

    def schedule_widgets(self, frame):
        schedule_widgets_frame = ttk.Frame(master=frame)
        schedule_widgets_frame.configure(borderwidth=10, relief='groove')

        self.schedule_buttons(schedule_widgets_frame).pack(fill='x')
        self.schedule_details(schedule_widgets_frame).pack(expand=True, fill='both')
        return schedule_widgets_frame

    def schedule_list(self, frame):
        schedule_list_frame = ttk.Frame(master=frame)
        schedule_list_frame.configure(borderwidth=10, relief='groove')
        ttk.Label(
            schedule_list_frame,
            text='Schedules',
            font='Arial'
        ).pack(fill='x')

        schedule_list_items = tk.StringVar()
        self.schedules_list = tk.Listbox(
            schedule_list_frame,
            listvariable=schedule_list_items
        )

        self.schedules_list.pack(expand=True,fill='both')
        return schedule_list_frame

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
        self.schedule_id_entry = ttk.Entry(
            schedule_details_frame,
            textvariable=self.schedule_id_variable
        )
        self.schedule_start_date_entry = ttk.Entry(
            schedule_details_frame,
            textvariable=self.schedule_start_date_variable
        )
        self.schedule_end_date_entry = ttk.Entry(
            schedule_details_frame,
            textvariable=self.schedule_end_date_variable
        )
        self.schedule_availability_entry = ttk.Entry(
            schedule_details_frame,
            textvariable=self.schedule_availability_variable
        )

        # Packing the Entries
        self.schedule_id_entry.grid(row=0, column=1, sticky='ew')
        self.schedule_start_date_entry.grid(row=1, column=1, sticky='ew')
        self.schedule_end_date_entry.grid(row=2, column=1, sticky='ew')
        self.schedule_availability_entry.grid(row=3, column=1, sticky='ew')

        return schedule_details_frame

    def new_schedule_button(self):
        pass

    def open_schedule_button(self):
        pass

    def modify_schedule_button(self):
        pass

    def delete_schedule_button(self):
        pass


class EmployeeTab(ttk.Frame):
    def __init__(self, root):
        super().__init__(master=root)

        self.manager_name = None
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
        self.employee_job_position_variable = tk.StringVar()
        self.employee_manager_variable = tk.StringVar()
        self.employee_phone_number_variable = tk.StringVar()
        self.employee_email_variable = tk.StringVar()
        self.employee_lastname_variable = tk.StringVar()
        self.employee_firstname_variable = tk.StringVar()
        self.employee_id_variable = tk.StringVar()

        self.employee_table(self).pack(side='left', expand=True, fill='both')
        self.employee_widgets(self).pack(side='left', expand=True, fill='both')
        self.pack()

    def employee_table(self, frame):
        employee_table_frame = ttk.Frame(master=frame)
        employee_table_frame.configure(borderwidth=10, relief='groove')
        self.employee_treeview = ttk.Treeview(
            master=employee_table_frame,
            columns=('employee_id', 'first_name', 'last_name'),
            show='headings',
            selectmode='browse'
        )

        self.employee_treeview.heading('employee_id', text='Employee ID')
        self.employee_treeview.heading('first_name', text='First Name')
        self.employee_treeview.heading('last_name', text='Last Name')

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
        self.manager_name = tk.Label(
            employee_details_frame,
            textvariable=self.employee_manager_variable
        )

        # Placing the Entries/Texts
        self.employee_id_entry.grid(row=0, column=2, sticky='ew')
        self.employee_first_name_entry.grid(row=1, columnspan=2, column=2, sticky='ew')
        self.employee_last_name_entry.grid(row=2, columnspan=2, column=2, sticky='ew')
        self.employee_email_entry.grid(row=3, columnspan=2, column=2, sticky='ew')
        self.employee_phone_entry.grid(row=4, columnspan=2, column=2, sticky='ew')
        self.job_position.grid(row=5, columnspan=2, column=2, sticky='ew')
        self.manager_name.grid(row=6, columnspan=2, column=2, sticky='ew')

        return employee_details_frame

    def populate_employee_list(self):
        employees = sql_connection.retrieve_employee_list()
        for i in employees:
            if i[-1] == 0:
                self.employee_treeview.insert(
                    parent='',
                    index=tk.END,
                    iid=None,
                    values=(i[0], i[1], i[2])
                )

    def new_employee_button(self):
        pass

    def open_employee_button(self):
        employee_index = self.employee_treeview.focus()
        selected_employee = self.employee_treeview.item(employee_index)
        retrieved_employee = sql_connection.retrieve_an_employee(selected_employee.get('values')[0])

        self.employee_id_variable.set(retrieved_employee[0])
        self.employee_firstname_variable.set(retrieved_employee[1])
        self.employee_lastname_variable.set(retrieved_employee[2])
        self.employee_email_variable.set(retrieved_employee[3])
        self.employee_phone_number_variable.set(retrieved_employee[4])
        self.employee_job_position_variable.set(retrieved_employee[5])

        if retrieved_employee[6] is None:
            self.employee_manager_variable.set('No Manager')
        else:
            manager_details = sql_connection.retrieve_manager(retrieved_employee[6])
            manager_name = f'{manager_details[0]} {manager_details[1]}'
            self.employee_manager_variable.set(manager_name)

    def modify_employee_button(self):
        pass

    def delete_employee_button(self):
        pass

    def assign_schedule_button(self):
        pass


App()
