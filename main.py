import mysql.connector
from tkinter import *
from tkinter import messagebox

# Function to connect to the MySQL database


def connect_to_database():
    try:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Anshuman@06",
        database="finance_project_dbms",
        auth_plugin="caching_sha2_password")
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Connection Error", f"Error: {err}")
        return None

# Function to fetch and display users from the User table
def show_users():
    conn = connect_to_database()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User")
    rows = cursor.fetchall()

    for row in rows:
        users_listbox.insert(END, f"ID: {row[0]} | Name: {row[1]} | Email: {row[3]} | Age: {row[2]}")

    conn.close()

# Function to add a user to the database
def add_user():
    name = entry_name.get()
    age = entry_age.get()
    email = entry_email.get()
    password = entry_password.get()

    if name == "" or age == "" or email == "" or password == "":
        messagebox.showerror("Input Error", "All fields are required!")
        return

    conn = connect_to_database()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("INSERT INTO User (Name, Age, Email, Password) VALUES (%s, %s, %s, %s)", 
                   (name, age, email, password))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "User added successfully!")
    show_users()  # Refresh the user list'''

# Create the main window
root = Tk()
root.title("Finance Project")
root.geometry("600x400")

# Display users section
users_listbox = Listbox(root, width=80, height=10)
users_listbox.pack(pady=20)

# Display users when the window is opened
show_users()

# Form to add a user
frame_add_user = Frame(root)
frame_add_user.pack(pady=20)

label_name = Label(frame_add_user, text="Name:")
label_name.grid(row=0, column=0, padx=10, pady=5)
entry_name = Entry(frame_add_user)
entry_name.grid(row=0, column=1, padx=10, pady=5)

label_age = Label(frame_add_user, text="Age:")
label_age.grid(row=1, column=0, padx=10, pady=5)
entry_age = Entry(frame_add_user)
entry_age.grid(row=1, column=1, padx=10, pady=5)

label_email = Label(frame_add_user, text="Email:")
label_email.grid(row=2, column=0, padx=10, pady=5)
entry_email = Entry(frame_add_user)
entry_email.grid(row=2, column=1, padx=10, pady=5)

label_password = Label(frame_add_user, text="Password:")
label_password.grid(row=3, column=0, padx=10, pady=5)
entry_password = Entry(frame_add_user, show="*")
entry_password.grid(row=3, column=1, padx=10, pady=5)

btn_add_user = Button(root, text="Add User", command=add_user)
btn_add_user.pack(pady=10)

# Start the GUI event loop
root.mainloop()