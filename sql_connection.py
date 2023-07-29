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
    all_guests = None

    try:
        retrieve_names_query = "SELECT * FROM Guest"
        c.execute(retrieve_names_query)
        all_guests = c.fetchall()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return all_guests


def retrieve_a_guest(index):
    """SQL Query for retrieving a specific guest information"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    guest_details = None

    try:
        c.execute("""SELECT guest_id,first_name,last_name,email,
                phone_number,payment_info FROM GUEST WHERE guest_id = ?""", (index,))
        guest_details = c.fetchone()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return guest_details


def retrieve_guest_room(guest_id_index):
    """SQL Query for retrieving a specific guest room number"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    guest_room_number = None

    try:
        retrieve_a_guest_room_query = ("""SELECT room_number FROM(  
            SELECT Guest.guest_id, Room.room_number
            FROM Guest
            INNER JOIN Visit 
            ON Guest.guest_id = Visit.guest_id
            INNER JOIN Room 
            ON Visit.room_id = Room.room_id
            ) WHERE guest_id = ?""")
        c.execute(retrieve_a_guest_room_query, (guest_id_index,))

        guest_room_number = c.fetchall()
        rowCount = len(guest_room_number)
        if rowCount == 0:
            return "No Room Assigned"
        else:
            guest_room_number = guest_room_number[0]

    except Exception as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return guest_room_number[0]


def retrieve_employee_list():
    """SQL Query for retrieving all the employee"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    all_employees = None

    try:
        retrieve_employees_query = "SELECT * FROM EMPLOYEE"
        c.execute(retrieve_employees_query)
        all_employees = c.fetchall()

    except sqlite3 as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return all_employees


def retrieve_an_employee(id_index):
    """SQL Query for retrieving a specific employee"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    the_employee = None

    try:
        c.execute("""SELECT employee_id,first_name,last_name,email,
                        phone_number,job_position,manager_id FROM EMPLOYEE WHERE employee_id = ?""", (id_index,))
        the_employee = c.fetchone()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return the_employee


def retrieve_manager(manager_id):
    """SQL Query for retrieving the manager of an employee"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    the_manager = None

    try:
        c.execute("""SELECT first_name,last_name FROM EMPLOYEE WHERE employee_id = ?""", (manager_id,))
        the_manager = c.fetchone()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return the_manager


def retrieve_rooms_list():
    """SQL Query for retrieving all the rooms """
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    all_rooms = None

    try:
        retrieve_rooms_query = "SELECT * FROM ROOM"
        c.execute(retrieve_rooms_query)
        all_rooms = c.fetchall()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return all_rooms


def retrieve_a_room(room_index):
    """SQL Query for retrieving a specific room """

    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    the_room_result = None

    try:
        c.execute("""SELECT room_id, room_number, room_type, price FROM ROOM WHERE room_number = ?""", (room_index,))
        the_room_result = c.fetchone()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return the_room_result


def create_a_guest(first_name,
                   last_name,
                   email,
                   phone_number,
                   payment_info,
                   check_in,
                   check_out,
                   total_price,
                   room_id):
    """
    SQL Query for creating a guest,
    having their bill created,
    room assigned, and visit established
    """
    # Establish Connection and Cursor
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()

    # Variables to be used
    guest_id = None
    billing_id = None

    # Creates a guest in the table
    try:
        create_a_guest_query = """INSERT INTO 
        Guest(first_name, last_name, email, phone_number, payment_info, is_deleted) VALUES (?,?,?,?,?,?)"""
        c.execute(create_a_guest_query, (first_name, last_name, email, phone_number, payment_info, 0))
        conn.commit()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()

    # Re-establish Cursor
    c = conn.cursor()

    # Gets the latest guest record's ID
    try:
        get_latest_guest_id_query = """SELECT guest_id FROM Guest ORDER BY rowid DESC LIMIT 1"""
        c.execute(get_latest_guest_id_query)
        guest_id = c.fetchone()[0]

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()

    # Re-establish Cursor
    c = conn.cursor()

    # Creates billing record according to guest's room choice and night.
    try:
        create_billing_query = """INSERT INTO 
            Billing(total_charge, payment_info, availability) 
            VALUES (?, ?, ?)"""
        c.execute(create_billing_query, (total_price, payment_info, 1))
        conn.commit()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()

    # Re-establish Cursor
    c = conn.cursor()

    # Gets the latest billing record's ID
    try:
        get_latest_billing_id_query = "SELECT billing_id FROM Billing ORDER BY rowid DESC LIMIT 1"
        c.execute(get_latest_billing_id_query)
        billing_id = c.fetchone()[0]

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()

    # Re-establish Cursor
    c = conn.cursor()

    # Creates the visit record.
    try:
        create_visit_query = """INSERT INTO 
        Visit(visit_type, number_of_guest, check_in_date, check_out_date, guest_id, room_id, billing_id) 
        VALUES(?,?,?,?,?,?,?)"""
        c.execute(create_visit_query, ('walk_in', 3, check_in, check_out, guest_id, room_id, billing_id))
        conn.commit()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()

    # Re-establish Cursor
    c = conn.cursor()

    # Creates the visit record.
    try:
        modify_rooms_availability = """
        UPDATE Room
        SET Availability = 0
        WHERE room_id = ?
        """
        c.execute(modify_rooms_availability, (room_id,))
        conn.commit()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()


def soft_delete_guest(guest_id):
    """SQL Query for soft deleting a guest"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    the_room = None

    try:
        c.execute("""UPDATE Guest 
        SET is_deleted = 1
        WHERE guest_id = ?""", (guest_id,))
        conn.commit()
    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()


def check_if_guest_has_bill(guest_id):
    """SQL Query for checking if guest has ongoing payment"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    the_result = None

    try:
        retrieve_guest_bill = """
        SELECT availability FROM(  
            SELECT Guest.guest_id, Billing.availability 
            FROM Guest
            INNER JOIN Visit
            ON Guest.guest_id = Visit.guest_id
            INNER JOIN Billing
            ON Visit.billing_id = Billing.billing_id
        ) WHERE guest_id = ?"""
        c.execute(retrieve_guest_bill, (guest_id,))

        the_result = c.fetchall()
        rowCount = len(the_result)
        if rowCount == 0:
            return "No Room Assigned"
        else:
            the_result = the_result[0]

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return the_result[0]


def set_room_availability_after_guest_delete(room_id):
    """SQL Query for setting room availability to true after guest deletion"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()

    try:
        set_room_availability = """
        UPDATE Room
        Set availability = 1
        WHERE room_id = ?
        """
        c.execute(set_room_availability, (room_id,))
        conn.commit()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()


def retrieve_bills_and_guest():
    """SQL Query for retrieving bills"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    all_bills = None
    try:
        get_bills_query = """
        SELECT 
            Billing.billing_id, 
            (Guest.first_name||' '||Guest.last_name) as "Full name",
            Billing.total_charge,
            Guest.payment_info,
            Billing.availability
            FROM Guest
            INNER JOIN Visit
            ON Guest.guest_id = Visit.guest_id
            INNER JOIN Billing
            ON Visit.billing_id = Billing.billing_id
        """
        c.execute(get_bills_query)
        all_bills = c.fetchall()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return all_bills


def retrieve_a_bill_and_guest(bill_id_index):
    """SQL Query for retrieving a specific bill"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    a_bills = None
    try:
        get_a_bill_query = """
            SELECT * FROM(
                SELECT 
                Billing.billing_id, 
                (Guest.first_name||' '||Guest.last_name) as "Full name",
                Billing.total_charge,
                Guest.payment_info,
                Billing.availability
                FROM Guest
                INNER JOIN Visit
                ON Guest.guest_id = Visit.guest_id
                INNER JOIN Billing
                ON Visit.billing_id = Billing.billing_id
        ) WHERE billing_id = ?
        """
        c.execute(get_a_bill_query, (bill_id_index,))
        a_bills = c.fetchall()[0]

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return a_bills


def pay_bills(bill_id_index):
    """SQL Query for paying a specific bill"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()

    try:
        pay_a_bill_query = """
            UPDATE Billing
            SET availability = 0
            WHERE billing_id = ?
            """
        c.execute(pay_a_bill_query, (bill_id_index,))
        conn.commit()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()


def get_details_to_modify(guest_id_index):
    """SQL Query for the guest modify feature"""
    conn = sqlite3.connect('database/hotelDB.db')
    c = conn.cursor()
    to_modify_details = None

    try:
        get_all_details_query = """
                SELECT * FROM(
                    SELECT
                        Guest.guest_id,
                        Guest.first_name,
                        Guest.last_name, 
                        Guest.email, 
                        Guest.phone_number, 
                        Guest.payment_info,
                        Visit.visit_id,
                        Visit.visit_type,
                        Visit.number_of_guest,
                        Visit.check_in_date,
                        Visit.check_out_date,
                        Room.room_id,
                        Room.room_number,
                        Room.room_type,
                        Room.price,
                        Billing.billing_id
                    FROM Guest
                    INNER JOIN Visit
                    ON Guest.guest_id = Visit.guest_id
                    INNER JOIN Billing
                    ON Visit.billing_id = Billing.billing_id
                    INNER JOIN Room
                    ON Visit.room_id = Room.room_id
                )WHERE guest_id=?
                """
        c.execute(get_all_details_query, (guest_id_index,))

        to_modify_details = c.fetchall()[0]

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return to_modify_details


class ModifyGuestSQL:
    def __init__(self):

        self.conn = None

    def update_guest_information(self, guest_id, first_name, last_name, email, phone_number, payment_info):
        """Updates a guest in the table"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        try:
            update_guest_query = """
            UPDATE Guest
            SET first_name = ?, 
            last_name = ?, 
            email = ?, 
            phone_number = ?, 
            payment_info = ? 
            WHERE guest_id = ?"""
            c.execute(update_guest_query, (first_name, last_name, email, phone_number, payment_info, guest_id))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def update_visit_information(self, visit_type,
                                 number_of_guest, check_in_date,
                                 check_out_date, billing_id,
                                 guest_id, visit_id
                                 ):
        """Updates visit information (Does not update room ID)"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        try:

            update_visit_query = """
                UPDATE Visit
                SET visit_type = ?, 
                number_of_guest = ?, 
                check_in_date = ?, 
                check_out_date = ?, 
                billing_id = ?,
                guest_id = ?
                WHERE visit_id = ?"""

            c.execute(update_visit_query, (
                visit_type,
                number_of_guest,
                check_in_date,
                check_out_date,
                billing_id,
                guest_id,
                visit_id))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def update_room_information(self, guest_id, new_room_id, old_room_id):
        """Updates room information if there is an update"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            update_old_room = """
               UPDATE Room
               SET availability = 1
               WHERE room_id = ?
               """

            update_visit_room = """
                UPDATE Visit
                SET room_id = ?
                WHERE guesT_id = ?
            """

            update_new_room = """
                            UPDATE Room
                            SET availability = 0
                            WHERE room_id = ?
                        """

            c.execute(update_old_room, (old_room_id,))
            c.execute(update_visit_room, (new_room_id, guest_id,))
            c.execute(update_new_room, (new_room_id,))

            self.conn.commit()
        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def update_bill_information(self, billing_id, total_price, payment_info):
        """Updates the billing table"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        try:
            update_billing_query = """
                    UPDATE Billing
                    SET payment_info = ?, total_charge = ?
                    WHERE billing_id = ?"""
            c.execute(update_billing_query, (payment_info, total_price, billing_id))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()


class RoomTabSQL:
    def __init__(self):
        self.conn = None

    def retrieve_a_specific_room(self, room_id):
        """SQL Query for retrieving a room """
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        room_result = None

        try:
            retrieve_a_room_query = """
            SELECT 
                room_id,
                room_number, 
                room_type, 
                price, 
                    CASE
                        WHEN availability = 0 THEN 'Unavailable'
                        WHEN availability = 1 THEN 'Available'
                        ELSE 'Unknown'
                    END AS availability,
                employee_id
            FROM Room
            WHERE room_id = ?
            """
            c.execute(retrieve_a_room_query, (room_id,))
            room_result = c.fetchall()[0]

        except sqlite3.Error as e:
            print("Something went wrong! Error", e)

        finally:
            c.close()
            self.conn.close()
            return room_result

    def soft_delete_room(self, room_id):
        """SQL Query for soft-deleting a room """
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            soft_delete_room_query = """
                UPDATE Room
                SET is_deleted = 1
                WHERE room_id = ?
            """
            c.execute(soft_delete_room_query, (room_id,))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error", e)

        finally:
            c.close()
            self.conn.close()
