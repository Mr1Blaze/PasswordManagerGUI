from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import sqlite3

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


def save():
    website = web_entry.get()
    email = username_entry.get()
    password = password_entry.get()

    if website and email and password:
        try:
            # Connect to the database
            conn = sqlite3.connect("passwords.db")
            cursor = conn.cursor()

            # Create the table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                                id INTEGER PRIMARY KEY,
                                website TEXT,
                                email TEXT,
                                password TEXT)''')

            # Insert data into the table
            cursor.execute("INSERT INTO passwords (website, email, password) VALUES (?, ?, ?)", (website, email, password))

            # Commit changes and close the connection
            conn.commit()
            conn.close()

            # Clear the entry fields
            web_entry.delete(0, END)
            password_entry.delete(0, END)

            messagebox.showinfo(title="Success", message="Password saved successfully!")
        except sqlite3.Error as e:
            messagebox.showerror(title="Error", message="An error occurred while saving the password.")
    else:
        messagebox.showwarning(title="Warning", message="Please fill in all the fields before saving.")

# Create the main window


window = Tk()
window.title("Password Manager GUI")
window.config(padx=50, pady=50)
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

web = Label(text="Website: ")
web.grid(row=1, column=0)
web_entry = Entry(width=35)
web_entry.grid(row=1, column=1, columnspan=2)
web_entry.focus()

username = Label(text="username: ")
username.grid(row=2, column=0)
username_entry = Entry(width=35)
username_entry.grid(row=2, column=1, columnspan=2)
username_entry.insert(0,'@gmail.com')

password_label = Label(text="password: ")
password_label.grid(row=3, column=0)
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)
password_button = Button(text='Generate Password' , command=generate_password)
password_button.grid(row=3, column=2)

add_button = Button(text='Add',width=36 , command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()