import sqlite3

"""Template for establishing connection and closing it"""


# conn = sqlite3.connect('database/hotelDB.db')
# c = conn.cursor()
#
# c.close()
# conn.close()

class DatabaseInitialization:
    def __init__(self):
        self.conn = None

    def initialize_database(self):
        """Initializes the database and creates table if no tables exists"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        create_guest_table = """CREATE TABLE IF NOT EXISTS Guest (
            [guest_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
            [first_name] [varchar](50) NOT NULL,
            [last_name] [varchar](50) NOT NULL,
            [email] [varchar](50) NOT NULL,
            [phone_number] [varchar](15) NOT NULL,
            [payment_info] [varchar](30) NOT NULL,
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
            [room_type] [varchar] CHECK(room_type IN ('Single', 'Double', 'Triple', 'Family', 'Suite')) NOT NULL,
            [price] [decimal] NOT NULL,
            [availability] [bit] NOT NULL,
            [employee_id] int UNIQUE NULL,
            [is_deleted] [bit] NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES [Employee]([employee_id])
            )"""

        create_employee_table = """CREATE TABLE IF NOT EXISTS Employee (
            [employee_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
            [first_name] [varchar](50) NOT NULL,
            [last_name] [varchar](50) NOT NULL,
            [email] [nvarchar](62) NOT NULL,
            [phone_number] [varchar](15) NOT NULL,
            [job_id] [int] NOT NULL,
            [manager_id] int NULL,
            [is_deleted] [bit] NOT NULL,
                FOREIGN KEY (manager_id) REFERENCES [Employee]([employee_id])
                FOREIGN KEY (job_id) REFERENCES [Jobs]([job_id])
        )"""

        create_assigned_schedule_table = """CREATE TABLE IF NOT EXISTS AssignedSchedule (
            [employee_id] [integer] NULL,
            [schedule_id] [integer] NULL,
            [status] [varchar](20) CHECK(status IN ('Active','Completed','Leave')) NOT NULL,
			UNIQUE (employee_id, schedule_id),
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
            [payment_method] [varchar](50) NOT NULL,
            [availability] [bit] NOT NULL,
            [employee_id] [integer] NULL,
                FOREIGN KEY (employee_id) REFERENCES [Employee]([employee_id])
        )"""

        c.execute(create_billing_table)
        self.conn.commit()
        c.execute(create_schedule_table)
        self.conn.commit()
        c.execute(create_assigned_schedule_table)
        self.conn.commit()
        c.execute(create_employee_table)
        self.conn.commit()
        c.execute(create_room_table)
        self.conn.commit()
        c.execute(create_visit_table)
        self.conn.commit()
        c.execute(create_guest_table)
        self.conn.commit()

        c.close()
        self.conn.close()

    def initialize_default_jobs(self):
        """SQL Query to initialize default jobs"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            c.execute("SELECT * FROM Jobs")

        except sqlite3.OperationalError:

            create_jobs_table = """CREATE TABLE IF NOT EXISTS Jobs (
                        [job_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
                        [job_title] [varchar][50] NOT NULL,
                        [job_department] [text][50] NOT NULL
                    )"""
            c.execute(create_jobs_table)
            self.conn.commit()
            create_jobs_query = """INSERT OR IGNORE INTO Jobs(job_title, job_department)
                        VALUES ('Front Desk Clerk','Front Office'),
                        ('Housekeeper','Housekeeping'),
                        ('Maintenance Staff','Maintenance'),
                        ('Manager','Management'),
                        ('Security Guard','Security')
                        """
            c.execute(create_jobs_query)
            self.conn.commit()

        finally:
            c.close()
            self.conn.close()


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

    except sqlite3.Error as e:
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
                        phone_number,job_id,manager_id FROM EMPLOYEE WHERE employee_id = ?""", (id_index,))
        the_employee = c.fetchone()

    except sqlite3.Error as e:
        print("Something went wrong! Error: ", e)

    finally:
        c.close()
        conn.close()

    return the_employee


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


class CreateAGuest:
    def __init__(self):
        self.conn = None

    def create_a_guest(self, first_name, last_name, email, phone_number, payment_info):
        """First Step of Creating A Guest"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            create_a_guest_query = """
                INSERT INTO 
                Guest(first_name, last_name, email, phone_number, payment_info, is_deleted) 
                VALUES (?,?,?,?,?,?)
                """
            c.execute(create_a_guest_query, (first_name, last_name, email, phone_number, payment_info, 0))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def get_latest_guest_id(self):
        """Second Step of Creating A Guest, Returns the Guest ID"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        guest_id = []
        try:
            get_latest_guest_id_query = """SELECT guest_id FROM Guest ORDER BY rowid DESC LIMIT 1"""
            c.execute(get_latest_guest_id_query)
            guest_id = c.fetchall()[0]

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()
            return guest_id[0]

    def creates_billing_record(self, total_price, payment_info):
        """Third Step of Creating A Guest, Creates New Billing Record and returns its ID"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        latest_billing_id = []
        try:
            create_billing_query = """
                INSERT INTO 
                Billing(total_charge, payment_method, availability) 
                VALUES (?, ?, ?)"""
            c.execute(create_billing_query, (total_price, payment_info, 1))
            self.conn.commit()

            get_latest_billing_id_query = "SELECT billing_id FROM Billing ORDER BY rowid DESC LIMIT 1"
            c.execute(get_latest_billing_id_query)
            latest_billing_id = c.fetchall()[0]

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()
            return latest_billing_id[0]

    def creates_visit_record(self, visit_type,
                             number_of_guest, check_in,
                             check_out, guest_id,
                             room_id, billing_id):
        """Fourth Step of Creating A Guest, Create the visit ID"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        if visit_type == "Walk In":
            visit_type = 'walk_in'
        elif visit_type == 'Reservation':
            visit_type = 'reservation'

        try:
            create_visit_query = """
            INSERT INTO 
            Visit(visit_type, number_of_guest, check_in_date, check_out_date, guest_id, room_id, billing_id) 
            VALUES(?,?,?,?,?,?,?)"""
            c.execute(create_visit_query, (visit_type, number_of_guest,
                                           check_in, check_out,
                                           guest_id, room_id, billing_id))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def set_room_availability(self, room_id):
        """Final Step of Creating A Guest, Modify Room Availability"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        try:
            modify_rooms_availability = """
            UPDATE Room
            SET Availability = 0
            WHERE room_id = ?
            """
            c.execute(modify_rooms_availability, (room_id,))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()


class GuestTabSQL:
    def __init__(self):
        self.conn = None

    def retrieve_guest_list_to_populate_table(self):
        """SQL Query that retrieves guest id, names, and assigned room"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        all_guests = []

        try:
            retrieve_employee_query = """
                SELECT 
                    Guest.Guest_id,
                    (Guest.first_name||' '|| Guest.last_name) AS full_name,
                    Room.room_number,
                    (Visit.check_in_date||' : '|| Visit.check_out_date) AS 'check-in-out-date',
                    Guest.is_deleted     
                FROM Guest
                INNER JOIN Visit
                ON Guest.guest_id = Visit.guest_id
                INNER JOIN ROOM
                ON Room.room_id = Visit.room_id"""
            c.execute(retrieve_employee_query)
            all_guests = c.fetchall()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

        return all_guests


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
                    SET payment_method = ?, total_charge = ?
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

    def create_a_room(self, room_name, room_type, room_price, employee_id):
        """SQL Query for creating a room"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        bool_flag = True
        try:
            soft_delete_room_query = """
                        INSERT INTO Room(room_number, room_type, price, availability, employee_id, is_deleted) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    """
            c.execute(soft_delete_room_query, (room_name, room_type, room_price, 1, employee_id, 0,))
            self.conn.commit()

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                bool_flag = False

        finally:
            c.close()
            self.conn.close()
            return bool_flag

    def check_if_room_available(self, room_id):
        """SQL Query for creating a room"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        is_it_available = None

        try:
            room_availability = """
                                SELECT availability
                                FROM Room
                                WHERE room_id = ?
                            """
            c.execute(room_availability, (room_id,))

            is_it_available = c.fetchall()[0]

        except sqlite3.Error as e:
            print("Something went wrong! Error", e)

        finally:
            c.close()
            self.conn.close()
            return is_it_available[0]

    def update_room_information(self, room_id, room_number, room_type, room_price, employee_id):
        """SQL Query for updating a room """
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        bool_flag = True
        try:
            update_room_query = """
                        UPDATE Room
                        SET room_number = ?, 
                        room_type = ?, 
                        price = ?, 
                        employee_id = ?
                        WHERE room_id = ?
                    """
            c.execute(update_room_query, (room_number, room_type, room_price, employee_id, room_id,))
            self.conn.commit()

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                bool_flag = False

        finally:
            c.close()
            self.conn.close()
            return bool_flag


class ScheduleTabSQL:
    def __init__(self):
        self.conn = None

    def retrieve_all_schedule(self):
        """SQL Query for retrieving all the schedule"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        all_schedules = []

        try:
            retrieve_schedules_query = "SELECT * FROM SCHEDULE"
            c.execute(retrieve_schedules_query)
            all_schedules = c.fetchall()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

        return all_schedules

    def insert_a_schedule(self, start_date, end_date):
        """SQL Query for create a schedule"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            insert_a_schedules_query = """
                INSERT INTO Schedule(start_date, end_date, availability)
                VALUES(?, ?, 1)
                """
            c.execute(insert_a_schedules_query, (start_date, end_date,))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def hard_delete_a_schedule(self, schedule_id):
        """SQL Query for permanently deleting a schedule"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            delete_a_schedules_query = """
                DELETE FROM Schedule
                WHERE schedule_id = ?
                """
            c.execute(delete_a_schedules_query, (schedule_id,))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def retrieve_a_schedule(self, schedule_id):
        """SQL Query for retrieving a schedule"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        a_schedule = []

        try:
            retrieve_schedules_query = """
                SELECT *
                FROM SCHEDULE 
                WHERE schedule_id = ?
            """
            c.execute(retrieve_schedules_query, (schedule_id,))
            a_schedule = c.fetchall()[0]

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

        return a_schedule

    def update_a_schedule(self, schedule_id, start_date, end_date):
        """SQL Query for updating a schedule"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            update_a_schedules_query = """
                UPDATE Schedule
                Set start_date = ?, end_date = ?
                WHERE schedule_id = ?
                """
            c.execute(update_a_schedules_query, (start_date, end_date, schedule_id))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def assign_schedule_to_employee(self, employee_id, schedule_id):
        """"SQL Query for assigning a schedule to an employee"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        bool_flag = True
        try:
            assign_schedule_query = """
                            INSERT INTO AssignedSchedule(employee_id, schedule_id, status)
                            VALUES (?, ?, ?)
                            """
            c.execute(assign_schedule_query,(employee_id, schedule_id, 'Active'))
            self.conn.commit()

        except sqlite3.IntegrityError:
            print("Cannot have the same schedule for the same employee!")
            bool_flag = False

        finally:
            c.close()
            self.conn.close()
            return bool_flag

    def delete_an_assigned_schedule(self, employee_id, schedule_id):
        """"SQL Query for deleting an assigned schedule to an employee"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        bool_flag = False # Assume deletion failed
        try:
            assign_schedule_query = """
                DELETE FROM AssignedSchedule
                WHERE employee_id = ? and schedule_id = ?
                                    """
            c.execute(assign_schedule_query, (employee_id, schedule_id,))
            rows_affected = c.rowcount

            if rows_affected > 0:
                bool_flag = True

            self.conn.commit()

        except sqlite3.Error:
            print("Something went wrong!")

        finally:
            c.close()
            self.conn.close()
            return bool_flag

    def retrieve_assigned_employees_on_a_schedule(self, schedule_id):
        """SQL Query for deleting an assigned schedule to an employee"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        try:
            retrieve_assigned_employees_query = """
                        SELECT * FROM(
                        SELECT 
                        Employee.employee_id,
                        (Employee.first_name||' '||Employee.last_name) AS 'Full Name',
                        Schedule.schedule_id
                        FROM Employee
                        INNER JOIN AssignedSchedule
                        ON Employee.employee_id = AssignedSchedule.employee_id 
                        INNER JOIN Schedule
                        ON AssignedSchedule.schedule_id = Schedule.schedule_id
                        ) WHERE schedule_id = ?
                                            """
            c.execute(retrieve_assigned_employees_query, (schedule_id,))
            retrieved_employees = c.fetchall()

        except sqlite3.Error:
            print("Something went wrong!")

        finally:
            c.close()
            self.conn.close()
            return retrieved_employees

    def is_employee_is_on_selected_schedule(self, employee_id, schedule_id):
        """"SQL Query for checking if employee is assigned on the selected schedule"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        bool_flag = True # Assume employee is indeed still assigned on the selected sched
        try:
            assign_schedule_query = """
                        SELECT COUNT(*)
                        FROM AssignedSchedule
                        WHERE employee_id = ? and schedule_id = ?
                                            """
            c.execute(assign_schedule_query, (employee_id, schedule_id,))
            fetch_count = c.fetchall()[0]

            if fetch_count[0] == 0:
                bool_flag = False

        except sqlite3.Error:
            print("Something went wrong!")
            bool_flag = False

        finally:
            c.close()
            self.conn.close()
            return bool_flag


class EmployeeTabSQL:
    def __init__(self):
        self.conn = None

    def retrieve_all_employees(self):
        """SQL Query for retrieving all the employee"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        all_employees = []

        try:
            retrieve_employee_query = "SELECT * FROM Employee"
            c.execute(retrieve_employee_query)
            all_employees = c.fetchall()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

        return all_employees

    def create_an_employee(self, first_name, last_name, email, phone_number, job_id, manager_id):
        """SQL Query for creating an employee"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            create_an_employee_query = """
            INSERT INTO EMPLOYEE(
            first_name, last_name, email, phone_number, job_id, manager_id, is_deleted)
            VALUES(?, ?, ?, ?, ?, ?, ?)"""
            c.execute(create_an_employee_query, (first_name, last_name, email, phone_number, job_id, manager_id, 0,))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def retrieve_jobs(self):
        """SQL Query for retrieving all jobs"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        all_jobs = []

        try:
            retrieve_jobs_query = "SELECT * FROM Jobs"
            c.execute(retrieve_jobs_query)
            all_jobs = c.fetchall()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

        return all_jobs

    def retrieve_employees_to_populate_list(self):
        """SQL Query for retrieving all the employee with jobs"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        all_employees = []

        try:
            retrieve_employee_query = """
            SELECT 
                Employee.employee_id,
                (Employee.first_name||' '|| Employee.last_name) AS full_name,
                Jobs.job_title,
                Employee.is_deleted     
            FROM Employee
            INNER JOIN Jobs 
            ON Employee.job_id = Jobs.job_id"""
            c.execute(retrieve_employee_query)
            all_employees = c.fetchall()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

        return all_employees

    def retrieve_a_specific_employee_for_details(self, employee_id_index):
        """SQL Query for retrieving an employee"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        an_employees = []

        try:
            retrieve_an_employee_for_details_query = """
                    SELECT 
                    Employee.employee_id,
                    Employee.first_name,
                    Employee.last_name,
                    Employee.email,
                    Employee.phone_number,
                    Jobs.job_title,
                    Employee.manager_id,
                    Employee.is_deleted
                    From Employee
                    INNER JOIN Jobs ON Employee.job_id = Jobs.job_id
                    WHERE employee_id = ?
                    """
            c.execute(retrieve_an_employee_for_details_query, (employee_id_index,))
            an_employees = c.fetchall()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()
            return an_employees[0]

    def retrieve_a_specific_employee(self, employee_id_index):
        """SQL Query for retrieving an employee"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        an_employees = []

        try:
            retrieve_an_employee_for_details_query = """
                    SELECT * From Employee WHERE employee_id = ?
                    """
            c.execute(retrieve_an_employee_for_details_query, (employee_id_index,))
            an_employees = c.fetchall()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()
            return an_employees[0]

    def update_an_employee(self, first_name, last_name, email, phone_number, job_id, manager_id, employee_id):
        """SQL Query for creating an employee"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            create_an_employee_query = """
                    UPDATE EMPLOYEE
                    SET first_name = ?,
                        last_name = ?,
                        email = ?, 
                        phone_number = ?,
                        job_id = ?,
                        manager_id = ?,
                        is_deleted = ?
                    WHERE employee_id = ?"""
            c.execute(create_an_employee_query, (first_name,
                                                 last_name,
                                                 email,
                                                 phone_number,
                                                 job_id,
                                                 manager_id,
                                                 0,
                                                 employee_id,))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def retrieve_a_manager(self, manager_id):
        """SQL Query for retrieving the manager of an employee"""

        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        the_manager = []

        try:
            retrieve_manager_name_query = """
                        SELECT (Employee.first_name||' '|| Employee.last_name) AS full_name
                        FROM Employee
                        WHERE employee_id = ?
                        """
            c.execute(retrieve_manager_name_query, (manager_id,))
            the_manager = c.fetchall()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

            return the_manager[0]

    def update_manager_id_if_updated(self, employee_id):
        """SQL Query for setting manager ID to null if updated employee is now a manager"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            create_an_employee_query = """
                            UPDATE EMPLOYEE
                            SET manager_id = ?
                            WHERE employee_id = ?"""
            c.execute(create_an_employee_query, (None,
                                                 employee_id,))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def soft_delete_an_employee(self, employee_id):
        """SQL Query for soft deleting an employee"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            soft_delete_an_employee_query = """
                                    UPDATE EMPLOYEE
                                    SET is_deleted = ?,
                                        manager_id = ?
                                    WHERE employee_id = ?"""
            c.execute(soft_delete_an_employee_query, (1, None, employee_id,))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def check_if_employee_still_manages(self, manager_id):
        """SQL Query for soft deleting an employee"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        count = 0

        try:
            checks_if_employee_manages_query = """
                SELECT COUNT(*) AS Count
                FROM Employee
                WHERE manager_id = ?
                """
            c.execute(checks_if_employee_manages_query, (manager_id,))
            count = c.fetchall()[0]

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

            if count[0] == 0:
                return False
            else:
                return True

    def check_if_theres_a_manager(self):
        """SQL Query for checking if there's a manager"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        count = 0

        try:
            checks_if_employee_manages_query = """
            SELECT COUNT(*) FROM Employee
            WHERE job_id = 4
            """
            c.execute(checks_if_employee_manages_query)
            count = c.fetchall()[0]

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

            if count[0] == 0:
                return False
            else:
                return True




class JobsTabSQL:
    def __init__(self):
        self.conn = None

    def retrieve_all_jobs(self):
        """SQL Query for retrieving all the jobs"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        all_jobs = []

        try:
            retrieve_employee_query = "SELECT * FROM Jobs"
            c.execute(retrieve_employee_query)
            all_jobs = c.fetchall()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

        return all_jobs

    def create_a_job(self, job_title, job_department):
        """SQL Query for create a Job"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        flag = True

        try:
            insert_a_job_query = """
                INSERT INTO Jobs(job_title, job_department)
                VALUES(?, ?)
                """
            c.execute(insert_a_job_query, (job_title, job_department))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)
            flag = False

        finally:
            c.close()
            self.conn.close()

        return flag

    def check_if_job_is_referenced(self, job_id):
        """SQL Query for to find if job is used"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        bool_flag = True

        try:
            check_job_query = """
                SELECT COUNT(*) AS count_references
                FROM Employee
                WHERE job_id = ?
                        """
            c.execute(check_job_query, (job_id,))
            job_count = c.fetchall()[0]

            if job_count[0] == 0:
                bool_flag = False

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)
            bool_flag = False

        finally:
            c.close()
            self.conn.close()

        return bool_flag

    def hard_delete_job(self,job_id):
        """SQL Query for to permanently delete a job"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        bool_flag = True

        try:
            hard_delete_job = """
                DELETE FROM Jobs
                WHERE job_id = ?
                """
            c.execute(hard_delete_job, (job_id,))

            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)
            bool_flag = False

        finally:
            c.close()
            self.conn.close()

        return bool_flag

    def select_a_specific_job(self, job_id):
        """SQL Query for to retrieve a specific job"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        retrieved_job = []

        try:
            retrieve_a_job_query = """
                        SELECT * FROM Jobs WHERE job_id = ?
                        """
            c.execute(retrieve_a_job_query, (job_id,))

            retrieved_job = c.fetchall()[0]

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

            return retrieved_job



class BillTabSQL:
    def __init__(self):
        self.conn = None

    def update_bill_record_employee(self, billing_id, employee_id):
        """SQL Query for assigning an employee to a bill"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            update_bill_employee_query = """
                    UPDATE Billing
                    Set employee_id = ?
                    WHERE billing_id = ?"""
            c.execute(update_bill_employee_query, (employee_id, billing_id))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def pay_bills(self, bill_id_index):
        """SQL Query for paying a specific bill"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()

        try:
            pay_a_bill_query = """
                UPDATE Billing
                SET availability = 0
                WHERE billing_id = ?
                """
            c.execute(pay_a_bill_query, (bill_id_index,))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)

        finally:
            c.close()
            self.conn.close()

    def does_bill_have_employee(self,billing_id):
        """SQL Query for checking if bill has an employee"""
        self.conn = sqlite3.connect('database/hotelDB.db')
        c = self.conn.cursor()
        bool_flag = True

        try:
            check_if_bill_employee_query = """
                SELECT employee_id
                FROM Billing
                WHERE billing_id = ?"""
            c.execute(check_if_bill_employee_query, (billing_id,))

            does_it_have_employee = c.fetchall()[0]

            if does_it_have_employee[0] is None:
                bool_flag = False

        except sqlite3.Error as e:
            print("Something went wrong! Error: ", e)
            bool_flag = False

        finally:
            c.close()
            self.conn.close()

            return bool_flag
