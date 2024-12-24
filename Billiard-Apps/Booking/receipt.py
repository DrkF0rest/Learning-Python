import os
from tabulate import tabulate
from Admin.database import cur
from index import clear_command

# Function to show receipt
def show_receipt(booking_date, email):
    from booking import booking_menu
    from index import menu

    while True:
        try:
            cur.execute("SELECT * FROM bookings WHERE booking_date = ?", (booking_date,))
            booking = cur.fetchone()
            header = ["Payment Receipt"]
            data = [[f"Booking ID: {booking[0]}"],
                [f"Name: {booking[1]}"],
                [""],
                [f"Booking Time: {booking[2]}"],
                [f"Duration: {booking[3]} Hours"],
                [f"Table Number: {booking[4]}"],
                [f"Table Name: {booking[5]}"],
                [f"Price: Rp.{booking[6]}"],
                [f"Payment Method: {booking[7]}"],
                [""],
                [f"Booking Date: {booking[8]}"]]
            print(tabulate(data, header, tablefmt="rounded_outline"))

            while True:
                try:
                    receipt = input("Return to Booking Menu? (Y/N): ")
                    if receipt.lower() == "y":
                        os.system(clear_command)
                        booking_menu(email)
                        break
                    else:
                        os.system(clear_command)
                        menu(email)
                        break
                except ValueError:
                    print("Input cannot be empty!")

        except Exception as e:
            print(f"An error occurred: {e}")