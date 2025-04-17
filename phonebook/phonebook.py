import psycopg2
import csv


def connect():
    return psycopg2.connect(
        dbname="phonebook",
        user="postgres",
        password="Zhasminchik6",
        host="localhost",
        port="5432"
    )

def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)",
                            (row['first_name'], row['phone']))
        conn.commit()
        print("CSV data inserted successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def insert_manual():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def update_data():
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone number: ")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE PhoneBook SET phone = %s WHERE first_name = %s", (new_phone, name))
        conn.commit()
        if cur.rowcount > 0:
            print("Data updated successfully.")
        else:
            print("No user found with that name.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def query_data():
    keyword = input("Enter name or part of name to search: ")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM PhoneBook WHERE first_name ILIKE %s", ('%' + keyword + '%',))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def delete_data():
    choice = input("Delete by (1) name or (2) phone? ")
    conn = connect()
    cur = conn.cursor()
    try:
        if choice == '1':
            name = input("Enter name: ")
            cur.execute("DELETE FROM PhoneBook WHERE first_name = %s", (name,))
        elif choice == '2':
            phone = input("Enter phone: ")
            cur.execute("DELETE FROM PhoneBook WHERE phone = %s", (phone,))
        else:
            print("Invalid choice.")
            return
        conn.commit()
        if cur.rowcount > 0:
            print("Data deleted successfully.")
        else:
            print("No matching record found.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def menu():
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from CSV")
        print("2. Insert manually")
        print("3. Update data")
        print("4. Query data")
        print("5. Delete data")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            filename = input("Enter CSV filename (e.g. contacts.csv): ")
            insert_from_csv(filename)
        elif choice == '2':
            insert_manual()
        elif choice == '3':
            update_data()
        elif choice == '4':
            query_data()
        elif choice == '5':
            delete_data()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    menu()
