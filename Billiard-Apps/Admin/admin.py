import os
from tabulate import tabulate
from getpass import getpass
from database import conn, cur
from index import main, clear_command
from table import table_menu

# Function to display admin menu
def admin_menu():
    while True:
        header = [f"Hi Admin!, Welcome :)"]
        data = [["1. Account Data"], ["2. Table Data"], ["3. Booking Logs"], ["4. Back to Menu"]]

        print(tabulate(data, header, tablefmt="rounded_outline"))
        
        try:
            a_menu = int(input("Choose Option: "))
            if a_menu == 1:
                os.system(clear_command)
                admin_usr()
                break
            elif a_menu == 2:
                os.system(clear_command)
                table_menu()
                break
            elif a_menu == 3:
                os.system(clear_command)
                log_booking()
            elif a_menu == 4:
                os.system(clear_command)
                main()
            else:
                print("Option not available!")
        except ValueError:
            print("Input must be numeric and cannot be empty!")

# Function to manage user accounts in admin menu
def admin_usr():
    while True:
        header = ["Account Data"]
        data = [["1. View Account Data"], ["2. Edit Account Data"], ["3. Delete Account Data"], ["4. Back to Menu"]]

        print(tabulate(data, header, tablefmt="rounded_outline"))
        try:
            a_usr = int(input("Choose Option: "))
            if a_usr == 1:
                view_usr()
            elif a_usr == 2:
                edit_usr()
            elif a_usr == 3:
                delete_usr()
            elif a_usr == 4:
                os.system(clear_command)
                admin_menu()
                break
            else:
                print("Option not available!")
        except ValueError:
            print("Input must be numeric and cannot be empty!")
    
# Function to view user accounts
def view_usr():
    os.system(clear_command)
    try:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        
        if users:
            header = ["ID", "Username", "Email", "Password", "Phone", "Gender"]
            print(tabulate(users, header, tablefmt="rounded_outline"))
        else:
            os.system(clear_command)
            print("No user data available!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Function to edit user accounts
def edit_usr():
    while True:
        view_usr()
        try:
            id_user = int(input("Enter User ID: "))
            cur.execute("SELECT * FROM users WHERE id = ?", (id_user,))
            user = cur.fetchone()
            if user:
                username = input("Enter New Username: ")
                email = input("Enter New Email: ")
                while True:
                    passwd = getpass("Enter Password: ")
                    if len(passwd) < 8:
                        print("Password must be at least 8 characters.")
                    else:
                        break
                phone = int(input("Enter New Phone: "))
                gender = input("Enter New Gender (M/F): ")

                cur.execute("UPDATE users SET username = ?, email = ?, password = ?, phone = ?, gender = ? WHERE id = ?", (username, email, passwd, phone, gender, id_user))
                conn.commit()
                os.system(clear_command)
                print("Data successfully updated!")
                break
            else:
                os.system(clear_command)
                print("Data not found!")
                break
        except ValueError:
            print("Input cannot be empty!")
        except Exception as e:
            print(f"An error occurred: {e}")

# Function to delete user accounts
def delete_usr():
    while True:
        view_usr()
        try:
            id_user = int(input("Enter User ID: "))
            cur.execute("SELECT * FROM users WHERE id = ?", (id_user,))
            user = cur.fetchone()
            if user:
                cur.execute("DELETE FROM users WHERE id = ?", (id_user,))
                conn.commit()
                os.system(clear_command)
                print("Data successfully deleted!")
                break
            else:
                os.system(clear_command)
                print("Data not found!")
                break
        except ValueError:
            print("Input cannot be empty!")
        except Exception as e:
            print(f"An error occurred: {e}")

# Function to view booking logs
def log_booking():
    try:
        cur.execute("SELECT * FROM bookings")
        bookings = cur.fetchall()
        
        if bookings:
            header = ["ID", "Username", "Booking Time", "Duration (Hrs)", "Table Number", "Table Name", "Price", "Payment Method", "Booking Date"]
            print(tabulate(bookings, header, tablefmt="rounded_outline"))
        else:
            print("No data available.")

    except Exception as e:
        print(f"An error occurred: {e}")