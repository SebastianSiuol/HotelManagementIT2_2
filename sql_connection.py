import sqlite3

"""Template for establishing connection and closing it"""
# conn = sqlite3.connect('database/hotelDB.db')
# c = conn.cursor()
#
# c.close()
# conn.close()


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
