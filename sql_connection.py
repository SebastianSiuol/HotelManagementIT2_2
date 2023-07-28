import sqlite3


# conn = sqlite3.connect('database/hotelDB.db')
# c = conn.cursor()
#
# c.close()
# conn.close()

def retrieve_guest_lists():
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    retrieve_names_query = "SELECT * FROM GUEST"
    c.execute(retrieve_names_query)

    lists_items = c.fetchall()
    c.close()
    conn.close()

    return lists_items


def retrieve_guest(index):
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

    lists_items = c.fetchall()
    c.close()
    conn.close()

    return lists_items


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
