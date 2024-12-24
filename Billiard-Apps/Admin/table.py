import os
from tabulate import tabulate
from database import conn, cur
from index import clear_command

# Function to display table management menu
def table_menu():
    from admin import admin_menu

    while True:
        header = ["Table Information"]
        data = [["1. Add Table"], ["2. View Tables"], ["3. Edit Table"], ["4. Delete Table"], ["5. Back"]]
        print(tabulate(data, header, tablefmt="rounded_outline"))
        
        try:
            t_menu = int(input("Choose Option: "))
            if t_menu == 1:
                add_table()
            elif t_menu == 2:
                os.system(clear_command)
                view_tables()
            elif t_menu == 3:
                edit_table()
            elif t_menu == 4:
                delete_table()
            elif t_menu == 5:
                os.system(clear_command)
                print("Exiting the program.")
                admin_menu()
                break
            else:
                print("Option not available!")
                
        except ValueError:
            print("Input must be numeric and cannot be empty!")

# Function to add a new billiard table
def add_table():
    try:
        table_number = int(input("Enter Table Number: "))
        table_name = input("Enter Table Name: ")
        price = int(input("Enter Table Price: "))

        cur.execute("INSERT INTO tables (table_number, table_name, price) VALUES (?, ?, ?)", (table_number, table_name, price))
        conn.commit()
        os.system(clear_command)
        print("Data successfully added!")

    except ValueError:
        print("Input cannot be empty!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to view all billiard tables
def view_tables():
    try:
        cur.execute("SELECT * FROM tables")
        tables = cur.fetchall()
        
        if tables:
            header = ["ID", "Table Number", "Table Name", "Price"]
            print(tabulate(tables, header, tablefmt="rounded_outline"))
        else:
            os.system(clear_command)
            print("Oops, no table data available!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Function to edit existing table information
def edit_table():
    while True:
        view_tables()
        try:
            table_id = int(input("Enter the ID of the table to edit: "))
            
            table_number = int(input("Enter New Table Number: "))
            table_name = input("Enter New Table Name: ")
            price = int(input("Enter New Price: "))

            cur.execute("""UPDATE tables SET 
            table_number = ?, 
            table_name = ?, 
            price = ? WHERE id = ? """, (table_number, table_name, price, table_id))
            conn.commit()

            os.system(clear_command)
            print("Data successfully updated!")
            view_tables()
            break

        except ValueError:
            print("Input cannot be empty!")
        except Exception as e:
            print(f"An error occurred: {e}")

# Function to delete a table from the system
def delete_table():
    while True:
        os.system(clear_command)
        view_tables()
        try:
            table_id = int(input("Enter the ID of the table to delete: "))

            cur.execute("DELETE FROM tables WHERE id = ?", (table_id,))
            conn.commit()
            cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name = 'tables'")
            conn.commit()

            print("Data successfully deleted!")
            os.system(clear_command)
            view_tables()
            break

        except ValueError:
            print("Input cannot be empty!")
        except Exception as e:
            print(f"An error occurred: {e}")