from tkinter import *
from random import shuffle, choice
from tkinter import messagebox
import json

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                     'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                     'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                     'z']

UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                     'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                     'Z']

SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
           '*', '(', ')', '<']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    global DIGITS, LOCASE_CHARACTERS, UPCASE_CHARACTERS, SYMBOLS
    pwd = []
    digits = [choice(DIGITS) for _ in range(3)]
    lower_letters = [choice(LOCASE_CHARACTERS) for _ in range(3)]
    upper_letters = [choice(UPCASE_CHARACTERS) for _ in range(3)]
    symbols = [choice(SYMBOLS) for _ in range(3)]
    pwd = digits + lower_letters + upper_letters + symbols
    shuffle(pwd)
    new_pwd = "".join(pwd)
    password_gen.delete(0, END)
    password_gen.insert(0, new_pwd)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    pwd = password_gen.get()
    username = user_name.get()
    website_n = website_name.get()
    new_data = {
        website_n: {
            "email": username,
            "password": pwd
        }
    }
    if len(username) == 0 or len(pwd) == 0:
        messagebox.showinfo(title="Error", message="Oops!! Looks like you have missed some information")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            password_gen.delete(0, END)
            website_name.delete(0, END)


# Search
def find_password():
    with open("data.json", mode="r") as data_file:
        website = website_name.get()
        try:
            data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(title="ERROR", message="No file found")
        else:
            if website in data:
                username = data[website]["email"]
                pwd = data[website]["password"]
                messagebox.showinfo(title="Details", message=f"Email: {username}\nPassword: {pwd}")
            else:
                messagebox.showerror(title="NOT FOUND", message=f"No details for {website} found")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager App")
window.config(padx=50, pady=50)

my_image = PhotoImage(file="logo.png")
canvas = Canvas(height=200, width=200)
canvas.create_image(100, 100, image=my_image)
canvas.grid(row=0, column=1)

website_l = Label(text="Website:", font=("Courier", 15, "bold"))
website_l.grid(row=1, column=0)

website_name = Entry(width=21)
website_name.grid(row=1, column=1)
website_name.focus()

user = Label(text="Username/Email:", font=("Courier", 15, "bold"))
user.grid(row=2, column=0)

user_name = Entry(width=35)
user_name.grid(row=2, column=1, columnspan=2)
user_name.insert(0, "madhav75gupta@gmail.com")

password = Label(text="Password: ", font=("Courier", 15, "bold"))
password.grid(row=3, column=0)

password_gen = Entry(width=21)
password_gen.grid(row=3, column=1)

gen_password = Button(text="Generate", command=generate)
gen_password.grid(row=3, column=2)

save = Button(text="Add", width=35, command=save, highlightthickness=0)
save.grid(row=4, column=1, columnspan=2)

search = Button(text="Search", command=find_password)
search.grid(row=1, column=2)
window.mainloop()
