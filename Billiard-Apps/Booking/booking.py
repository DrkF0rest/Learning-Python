import os, sqlite3
from datetime import datetime
from getpass import getpass
from tabulate import tabulate
from Admin.database import conn, cur
from index import clear_command

# Function to display booking menu
def booking_menu(email):
    from index import menu

    while True:
        header = ["Billiard Apps"]
        data = [["1. Book Schedule"], ["2. View Schedule"], ["3. Edit Schedule"], ["4. Cancel Booking"], ["5. Main Menu"]]

        print(tabulate(data, header, tablefmt="rounded_outline"))
        try:
            option = int(input("Choose Option: "))
            if option == 1:
                os.system(clear_command)
                book_schedule(email)
            elif option == 2:
                os.system(clear_command)
                view_schedule(email)
            elif option == 3:
                os.system(clear_command)
                edit_schedule(email)
            elif option == 4:
                os.system(clear_command)
                cancel_booking(email)
            elif option == 5:
                menu(email)
                break
            else:
                print("Option not available!")

        except ValueError:
            print("Input must be numeric and cannot be empty!")

# Function to book a schedule
def book_schedule(email):
    from receipt import show_receipt
    from Admin.table import view_tables

    while True:
        view_tables()
        try:
            cur.execute("SELECT username FROM users WHERE email = ?", (email,))
            username = cur.fetchone()[0]
            
            booking_time = input("Enter Time (HH:MM): ")
            duration = int(input("Enter Duration (hours): "))
            table_number = int(input("Enter Table Number: "))
            payment_method = choose_payment_method()
            cur.execute("SELECT * FROM tables WHERE table_number = ?", (table_number,))
            table = cur.fetchone()
            booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not table:
                print("Table number not found!")
                continue
            price = table[3] * duration

            cur.execute("""INSERT INTO bookings (username, 
                        booking_time,
                        duration, 
                        table_number, 
                        table_name, 
                        price, 
                        payment_method, 
                        booking_date) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                        (username, booking_time, duration, table[1], table[2], price, payment_method, booking_date))
            conn.commit()
            os.system(clear_command)
            print("Your schedule has been successfully created!")
            
            while True:
                try:
                    receipt = input("Show Receipt? (Y/N): ")
                    if receipt.lower() == "y":
                        os.system(clear_command)
                        show_receipt(booking_date, email)
                        break
                    else: 
                        booking_menu(email)
                        break
                except ValueError:
                    print("Input cannot be empty!")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

        except ValueError:
            print("Invalid input, please enter valid data.")

# Function to validate debit payment
def validate_debit(pin):
    return len(pin) == 4

# Function to validate e-wallet payment
def validate_ewallet(ewallet):
    return len(ewallet) == 11

# Function to choose payment method
def choose_payment_method():

    while True:
        header = ["Payment Method"]
        data = [["1. Debit"], ["2. E-Wallet"]]
        print(tabulate(data, header, tablefmt="rounded_outline"))

        try:
            method = int(input("Choose Payment Method: "))
            if method == 1:
                pin = getpass("Enter 4 Digit Pin: ")

                if validate_debit(pin):
                    print("Payment Successful!")
                    return "Debit"
                else:
                    print("Payment Failed!")

            elif method == 2:
                ewallet = getpass("Enter Phone Number/ID E-Wallet: ")
                print("Validating E-Wallet...")

                if validate_ewallet(ewallet):
                    print("Payment Successful!")
                    return "E-Wallet"
                else:
                    print("Payment Failed!")
            else:
                print("Option not available!")
        except ValueError:
            print("Input must be numeric and cannot be empty!")

# Function to view schedule
def view_schedule(email):
    try:
        cur.execute("SELECT username FROM users WHERE email = ?", (email,))
        username = cur.fetchone()[0]
        
        cur.execute("""SELECT id, 
                    booking_time, 
                    duration, 
                    table_number, 
                    table_name, 
                    price, 
                    payment_method,  
                    booking_date FROM bookings WHERE username = ?""", (username,))
        bookings = cur.fetchall()
        if bookings:
            header = ["ID", "Booking Time", "Duration (Hrs)", "Table Number", "Table Name", "Price", "Payment Method", "Booking Date"]
            os.system(clear_command)
            print(tabulate(bookings, header, tablefmt="rounded_outline"))
        else:
            os.system(clear_command)
            print("No data available.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to edit schedule
def edit_schedule(email):
    from receipt import show_receipt
    from Admin.table import view_tables

    while True:
        view_schedule(email)
        try:
            booking_id = int(input("Enter Booking ID: "))
            cur.execute("SELECT username FROM users WHERE email = ?", (email,))
            username = cur.fetchone()[0]
            cur.execute("SELECT * FROM bookings WHERE id = ? AND username = ?", (booking_id, username,))
            booking = cur.fetchone()
            if booking:
                booking_time = input("Enter Time (HH:MM): ")
                view_tables()
                table_number = int(input("Enter Table Number: "))
                booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                cur.execute("SELECT * FROM tables WHERE table_number = ?", (table_number,))
                table = cur.fetchone()
                if not table:
                    print("Table number not found!")
                    continue

                price = table[3] * booking[3]

                if price > booking[6]:
                    payment_method = choose_payment_method()
                else:
                    payment_method = booking[7]

                cur.execute("""
                UPDATE bookings SET booking_time = ?, table_number = ?, table_name = ?, price = ?, payment_method = ?, booking_date = ?
                WHERE id = ?
                """, (booking_time, table[1], table[2], price, payment_method, booking_date, booking_id))
                conn.commit()

                os.system(clear_command)
                print("Your schedule has been successfully updated!")

                while True:
                    try:
                        receipt = input("Show Receipt? (Y/N): ")
                        if receipt.lower() == "y":
                            os.system(clear_command)
                            show_receipt(booking_date, email)
                            break
                        else: 
                            booking_menu(email)
                    except ValueError:
                        print("Input cannot be empty!")

            else:
                print("Booking ID not found!")
                break
        except Exception as e:
            print(f"An error occurred: {e}")

# Function to cancel booking
def cancel_booking(email):
    while True:
        view_schedule(email)
        try:
            booking_id = int(input("Enter Booking ID: "))
            cur.execute("SELECT username FROM users WHERE email = ?", (email,))
            username = cur.fetchone()[0]
            cur.execute("SELECT * FROM bookings WHERE id = ? AND username = ?", (booking_id, username,))
            booking = cur.fetchone()
            if booking:
                cur.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
                conn.commit()
                cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name = 'bookings'")
                conn.commit()

                os.system(clear_command)
                print("Your booking has been successfully canceled!")
                break
            else:
                print("Booking ID not found!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")