import os
from tabulate import tabulate
from Admin.database import conn, cur

# Function to clear the screen
clear_command = "cls" if os.name == "nt" else "clear"

# Function to display the main menu
def main():
    from user import usr_login, usr_register
    header = ["Welcome to Billiard Apps"]
    data = [["1. Login"], ["2. Register"]]
    print(tabulate(data, header, tablefmt="rounded_outline"))
    
    while True:
        try:
            login = int(input("Choose Option: "))
            if login == 1:
                usr_login()
                break
            elif login == 2:
                usr_register()
                break
            else:
                print("Option not available!")

        except ValueError:
            print("Input must be numeric and cannot be empty!")

# Function to display the user menu
def menu(email):
    from Booking.booking import booking_menu
    from user import usr_menu
    os.system(clear_command)
    cur.execute("SELECT username FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
        
    header = [f"Hi {user[0].capitalize()}, Welcome :)"]
    data = [["1. Book Table"], ["2. About Account"], ["3. Logout"]]
    print(tabulate(data, header, tablefmt="rounded_outline"))
    
    while True:
        try:
            choose_menu = int(input("Choose Option: "))
            if choose_menu == 1:
                booking_menu(email)
                break
            elif choose_menu == 2:
                usr_menu(email)
            elif choose_menu == 3:
                os.system(clear_command)
                conn.close()
                exit()
            else:
                print("Option not available!")

        except ValueError:
            print("Input must be numeric and cannot be empty!")

if __name__ == "__main__":
    main()