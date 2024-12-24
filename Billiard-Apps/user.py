import os, re, sqlite3
from getpass import getpass
from tabulate import tabulate
from Admin.database import conn, cur
from index import clear_command

# Function to register a new user
def usr_register():
    from index import main

    while True:
        try:
            while True:
                email = input("Enter Email Address: ")
                if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    break
                else:
                    print("Invalid email address. Try again.")

            while True:
                password = getpass("Enter Password: ")
                if len(password) < 8:
                    print("Password must be at least 8 characters.")
                else:
                    break

            username = input("Enter Username: ")

            while True:
                phone = input("Enter Phone Number: ")

                if phone.isdigit():
                    break
                else:
                    print("Phone number must be numeric.")
                
            while True:
                gender = input("Enter Gender (M/F): ")
                if gender in ["M", "F"]:
                    break
                else:
                    print("Invalid input. Please enter 'M' for Male or 'F' for Female.")

        except ValueError:
            print("Input cannot be empty!")
        
        try:
            cur.execute("INSERT INTO users (username, email, password, phone, gender) VALUES (?, ?, ?, ?, UPPER(?))",
                      (username, email, password, phone, gender))
            conn.commit()
            os.system(clear_command)
            print("Registration Successful! Please Login!")
            main()
            break
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")

# Function to login a user
def usr_login():
    from Admin.admin import admin_menu
    from index import main, menu

    while True:
        try:
            email = input("Enter Email Address: ")
            password = getpass("Enter Password: ")
            if email == "admin" and password == "admin":
                print("Welcome, Admin!")
                os.system(clear_command)
                admin_menu()
                break
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                os.system(clear_command)
                print("Invalid email address. Try again.")
                main()
                

            cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cur.fetchone()
            if user:
                print(f"Welcome, {user[1]}!")
                menu(email)
                break
            else:
                os.system(clear_command)
                print("Incorrect email or password. Try again.")
                main()
                

        
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Function to display user menu
def usr_menu(email):
    from index import menu

    os.system(clear_command)
    while True:
        header = ["About Your Account."]
        data = [["1. Account Information"], ["2. Edit Account"], ["3. Delete Account"], ["4. Main Menu"]]
        print(tabulate(data, header, tablefmt="rounded_outline"))
        
        try:
            u_menu = int(input("Choose Option: "))
            if u_menu == 1:
                usr_view(email)
                break
            elif u_menu == 2:
                usr_edit(email)
                break
            elif u_menu == 3:
                usr_delete(email)
            elif u_menu == 4:
                menu(email)
                break
            else:
                print("Option not available!")
        except ValueError:
            print("Input must be numeric and cannot be empty!")

# Function to view user information
def usr_view(email):
    os.system(clear_command)
    while True:
        cur.execute("SELECT email, username, phone, gender FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        
        if user:
            headers = ["This is Your Account Information."]
            data = [
                [f"Email Address: {user[0]}"],
                [f"Username: {user[1]}"], 
                [f"Phone Number: 0{user[2]}"], 
                ["Gender: Male" if user[3] == 'M' else "Gender: Female"]]

            print(tabulate(data, headers, tablefmt="rounded_outline"))
            while True:
                try:
                    edit_account = input("Edit Account? (Y/N): ")
                    if edit_account == "Y" or edit_account == "y":
                        usr_edit(email)
                        break
                    else: 
                        usr_menu(email)
                        break
                except ValueError:
                    print("Input cannot be empty!")
        else:
            print("Account not found.")

# Function to edit user information
def usr_edit(email):
    header =  ["Want to Change Personalization?"]
    data = [["1. Edit Account Information"], ["2. Change Password"], ["3. Back"]]
    print(tabulate(data, header, tablefmt="rounded_outline"))

    while True:
            try:
                edit = int(input("Choose Option: "))
                if edit == 1:
                    usr_edit_info(email)
                    break
                elif edit == 2:
                    usr_change_password(email) 
                    break
                elif edit == 3:
                    usr_menu(email)
                else:
                    print("Option not available!")
            except ValueError:
                print("Input must be numeric and cannot be empty!")

# Function to edit user information details
def usr_edit_info(email):
    while True:
        try:
            username = input("Enter Username: ")

            while True:
                phone = input("Enter Phone Number: ")

                if phone.isdigit():
                    break
                else:
                    print("Phone number must be numeric.")
                
            while True:
                gender = input("Enter Gender (M/F): ")
                if gender in ["M", "F"]:
                    break
                else:
                    print("Invalid input. Please enter 'M' for Male or 'F' for Female.")

            cur.execute("""UPDATE users SET
                        username = ?,
                        phone = ?,
                        gender = ?
                        WHERE email = ?""",(username, phone, gender, email,))
            conn.commit()
            print("Data Successfully Updated!")
            break
        except ValueError:
            print("Input cannot be empty!")

# Function to change user password
def usr_change_password(email):
    from index import main

    while True:
        try:
            password = getpass("Enter Password: ")

            cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cur.fetchone()

            if user:
                while True:
                    try:
                        new_password = getpass("Enter New Password: ")
                        if len(new_password) < 8:
                            print("Password must be at least 8 characters.")

                        cur.execute("""UPDATE users SET
                            password = ?
                            WHERE email = ?""",(new_password, email,))
                        conn.commit()
                        print("Data Successfully Updated!")
                        main()
                    except ValueError:
                        print("Input cannot be empty!")

        except ValueError:
            print("Input cannot be empty!")

# Function to delete user account
def usr_delete(email):
    from index import main
    
    while True:
        try:
            delete_account = input("Delete Account? (Y/N): ")
            if delete_account == "Y" or delete_account == "y":
                cur.execute("DELETE FROM users WHERE email = ?", (email,))
                conn.commit()
                cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name = 'users'")
                conn.commit()
                print("Your Account Has Been Deleted!")
                os.system(clear_command)
                main()
                break
            else: 
                usr_menu()
                break
        except ValueError:
            print("Input cannot be empty!")