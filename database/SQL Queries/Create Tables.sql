CREATE TABLE IF NOT EXISTS Guest (
            [guest_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
            [first_name] [varchar](50) NOT NULL,
            [last_name] [varchar](50) NOT NULL,
            [email] [varchar](50) NOT NULL,
            [phone_number] [varchar](15) NOT NULL,
			[payment_info] [varchar](30) NOT NULL
            [is_deleted] [bit] NOT NULL
            );
            
CREATE TABLE IF NOT EXISTS Visit (
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
            );
            
CREATE TABLE IF NOT EXISTS Room (
        [room_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
        [room_number] [text](15) NOT NULL,
        [room_type] [text] CHECK(room_type IN ('Single', 'Double', 'Triple', 'Family', 'Suite')) NOT NULL,
        [price] [decimal] NOT NULL,
        [availability] [bit] NOT NULL,
        [employee_id] int UNIQUE NULL,
        [is_deleted] [bit] NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES [Employee]([employee_id])
            )
        
CREATE TABLE IF NOT EXISTS Employee (
            [employee_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
            [first_name] [varchar](50) NOT NULL,
            [last_name] [varchar](50) NOT NULL,
            [email] [nvarchar](62) NOT NULL,
            [phone_number] [varchar](15) NOT NULL,
            [job_position] [varchar](20) NOT NULL,
            [manager_id] int NULL,
            [is_deleted] [bit] NOT NULL,
                FOREIGN KEY (manager_id) REFERENCES [Employee]([employee_id])
        );
        
CREATE TABLE IF NOT EXISTS AssignedSchedule (
            [employee_id] [integer] NULL,
            [schedule_id] [integer] NULL,
            [status] [varchar](20) CHECK(status IN ('Active','Completed','Leave')) NOT NULL,
			UNIQUE (employee_id, schedule_id),
                FOREIGN KEY (employee_id) REFERENCES [Employee]([employee_id])
                FOREIGN KEY (schedule_id) REFERENCES [Schedule]([schedule_id])
        );
        
CREATE TABLE IF NOT EXISTS Schedule (
            [schedule_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
            [start_date] [date] NOT NULL,
            [end_date] [date] NOT NULL,
            [availability] [bit] NOT NULL
        );
        
CREATE TABLE IF NOT EXISTS Billing (
            [billing_id] [integer] NOT NULL PRIMARY KEY AUTOINCREMENT,
            [total_charge] [decimal] NOT NULL,
            [payment_method] [varchar](50) NOT NULL,
            [availability] [bit] NOT NULL,
            [employee_id] [integer] NULL,
                FOREIGN KEY (employee_id) REFERENCES [Employee]([employee_id])
        );