import sqlite3

"""Template for establishing connection and closing it"""


# conn = sqlite3.connect('database/hotelDB.db')
# c = conn.cursor()
#
# c.close()
# conn.close()


def initialize_database():
    """Initializes the database and creates table if no tables exists"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()

    create_guest_table = """CREATE TABLE IF NOT EXISTS Guest (
            [guest_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
            [first_name] [varchar](50) NOT NULL,
            [last_name] [varchar](50) NOT NULL,
            [email] [varchar](62) NOT NULL,
            [phone_number] [varchar](15) NULL,
            [payment_info] [varchar](50) NOT NULL,
            [is_deleted] [bit] NOT NULL
            )"""

    create_visit_table = """CREATE TABLE IF NOT EXISTS Visit (
            [visit_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
            [visit_type] [varchar] CHECK(visit_type IN ('walk_in', 'reservation')) NOT NULL,
            [number_of_guest] [integer] NOT NULL,
            [check_in_date] [date] NOT NULL,
            [check_out_date] [date] NOT NULL,
            [guest_id] int NULL,
            [room_id] int NULL,
            [billing_id] int NULL,
                FOREIGN KEY (guest_id) REFERENCES [Guest] ([guest_id]),
                FOREIGN KEY (room_id) REFERENCES [Room]([room_id]),
                FOREIGN KEY (billing_id) REFERENCES [Billing]([billing_id])
            )"""

    create_room_table = """CREATE TABLE IF NOT EXISTS Room (
        [room_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
        [room_number] [varchar](15) NOT NULL,
        [room_type] [varchar](20) NOT NULL,
        [price] [decimal] NOT NULL,
        [availability] [bit] NOT NULL,
        [employee_id] int NULL,
        [is_deleted] [bit] NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES [Employee]([employee_id])
        )"""

    create_employee_table = """CREATE TABLE IF NOT EXISTS Employee (
            [employee_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
            [first_name] [varchar](50) NOT NULL,
            [last_name] [varchar](50) NOT NULL,
            [email] [nvarchar](62) NOT NULL,
            [phone_number] [varchar](15) NOT NULL,
            [job_position] [varchar](20) NOT NULL,
            [manager_id] int NULL,
            [is_deleted] [bit] NOT NULL,
                FOREIGN KEY (manager_id) REFERENCES [Employee]([employee_id])
        )"""

    create_assigned_schedule_table = """CREATE TABLE IF NOT EXISTS AssignedSchedule (
            [employee_id] [integer] NULL,
            [schedule_id] [integer] NULL,
            [status] [varchar](20) NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES [Employee]([employee_id])
                FOREIGN KEY (schedule_id) REFERENCES [Schedule]([schedule_id])
        )"""

    create_schedule_table = """CREATE TABLE IF NOT EXISTS Schedule (
            [schedule_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
            [start_date] [date] NOT NULL,
            [end_date] [date] NOT NULL,
            [availability] [bit] NOT NULL
        )"""

    create_billing_table = """CREATE TABLE IF NOT EXISTS Billing (
            [billing_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
            [total_charge] [decimal] NOT NULL,
            [payment_info] [varchar](50) NOT NULL,
            [availability] [bit] NOT NULL,
            [employee_id] int NULL,
                FOREIGN KEY (employee_id) REFERENCES [Employee]([employee_id])
        )"""

    c.execute(create_billing_table)
    c.execute(create_schedule_table)
    c.execute(create_assigned_schedule_table)
    c.execute(create_employee_table)
    c.execute(create_room_table)
    c.execute(create_visit_table)
    c.execute(create_guest_table)

    conn.commit()

    c.close()
    conn.close()


def retrieve_guest_lists():
    """SQL Query for retrieving all guest information"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    retrieve_names_query = "SELECT * FROM GUEST"
    c.execute(retrieve_names_query)

    all_guests = c.fetchall()
    c.close()
    conn.close()

    return all_guests


def retrieve_a_guest(index):
    """SQL Query for retrieving a specific guest information"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()

    c.execute("""SELECT guest_id,first_name,last_name,email,
                phone_number,payment_info FROM GUEST WHERE guest_id = ?""", (index,))
    guest_details = c.fetchone()
    c.close()
    conn.close()

    return guest_details


def retrieve_employee_list():
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    retrieve_employees_query = "SELECT * FROM EMPLOYEE"
    c.execute(retrieve_employees_query)

    all_employees = c.fetchall()
    c.close()
    conn.close()

    return all_employees


def retrieve_an_employee(id_index):
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    c.execute("""SELECT employee_id,first_name,last_name,email,
                    phone_number,job_position,manager_id FROM EMPLOYEE WHERE employee_id = ?""", (id_index,))

    the_employee = c.fetchone()
    c.close()
    conn.close()

    return the_employee


def retrieve_manager(manager_id):
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    c.execute("""SELECT first_name,last_name FROM EMPLOYEE WHERE employee_id = ?""", (manager_id,))

    the_manager = c.fetchone()
    c.close()
    conn.close()

    return the_manager


def retrieve_rooms_list():
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    retrieve_rooms_query = "SELECT * FROM ROOM"
    c.execute(retrieve_rooms_query)

    all_rooms = c.fetchall()
    c.close()
    conn.close()

    return all_rooms


def create_a_guest(first_name, last_name, email, phone_number, payment_info):
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    create_a_guest_query = """INSERT INTO 
    Guest(first_name, last_name, email, phone_number, payment_info, is_deleted) VALUES (?,?,?,?,?,?)"""
    c.execute(create_a_guest_query, (first_name, last_name, email, phone_number, payment_info, 0))

    conn.commit()
    c.close()
    conn.close()

