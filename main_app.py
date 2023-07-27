from cryptography.fernet import Fernet
import sqlite3
from tkinter import *
import random
from tkinter import messagebox
import shutil
import time


# Master Password
m_password = ""

# MyFernet (Later will be setted as Fernet(key))
my_fernet = ""

# Setting up Tkinter Window
root = Tk()
root.geometry("400x400")
root.title("Password Manager/Generator")
root.iconbitmap('icon_icon.ico')

# Invisible Frames for the program
main_frame = Frame(root, padx=5, pady=5)
secondary_frame = Frame(root, padx=5, pady=5)
rbutton_frame = Frame(root, padx=5, pady=5)
output_frame = Frame(root, padx=5, pady=5)
bottom_bar = Frame(root, padx=5, pady=5)

main_frame.pack(padx=20, pady=0)
secondary_frame.pack(padx=20, pady=20)
rbutton_frame.pack(padx=10, pady=0)
output_frame.pack(padx=15, pady=5)
bottom_bar.pack(side=BOTTOM)




def Authentication3():
    # Define a variable to store the last failed attempt time
    global last_failed_attempt_time
    now = time.time()
    
    if last_failed_attempt_time is not None and now - last_failed_attempt_time < 180:
        # If the user has failed authentication within the last 3 minutes, show a message
        # and do not create the authentication window again.
        alert('Too Many Attempts', 'You can retry after 3 minutes.')
        return
    
    last_failed_attempt_time = None  # Reset last_failed_attempt_time since the authentication window will be displayed

    # Creating Tkinter Window
    Authenticate = Toplevel()
    Authenticate.title('Authenticate')
    Authenticate.geometry('150x150')
    Authenticate.iconbitmap('icon_icon.ico')

    # Creating Components of the Window
    AuthenticateFrame = LabelFrame(
        Authenticate, text="Enter Master Password")
    AuthenticateFrame.pack(fill="both", expand="yes")
    button_frame1 = Frame(AuthenticateFrame)
    button_frame1.pack()
    
    def show_password():
        if m_password_entry.cget('show') == '*':
            m_password_entry.config(show='')
        else:
            m_password_entry.config(show='*')

    Check_button = Checkbutton(AuthenticateFrame, text='show password', command=show_password)
    Check_button.pack()

    # Entry Field for Password
    m_password_entry = Entry(AuthenticateFrame, width=25, show='*')
    m_password_entry.pack()

    # Where the real authentication code goes.
    # This one is for Password Notebook.:
    global failed_attempts
    failed_attempts = 0

    def RealAuthenticate3():
        global failed_attempts, last_failed_attempt_time
        m_entry = m_password_entry.get()
        if m_entry == m_password:
            Authenticate.destroy()
            store_pw()
        else:
            failed_attempts += 1
            if failed_attempts >= 3:
                m_password_entry.config(state="disabled")  # Disable the password entry
                last_failed_attempt_time = time.time()  # Set the last_failed_attempt_time to the current time
                m_password_entry.after(300000, reset_failed_attempts)
            alert('Wrong Password', 'Password is Incorrect', kind='warning')
            print(failed_attempts)

    def reset_failed_attempts():
        global failed_attempts
        failed_attempts = 0
        m_password_entry.config(state="normal")

    Auth_Button = Button(
        button_frame1, text='Authenticate', command=RealAuthenticate3)
    Auth_Button.pack()

# Initialize last_failed_attempt_time as None at the beginning of your code
last_failed_attempt_time = None




def store_pw():
    global path

    def copy_file():
        path = store_entry.get()
        shutil.copy("pw.txt", path)
        messagebox.showinfo("password saved")
        store_pw_frame.destroy()

    store_pw_frame = Toplevel(root, padx=5, pady=5)
    store_pw_frame.title("backup")
    store_pw_frame.geometry("300x200")

    store_label = LabelFrame(store_pw_frame, text="Enter storage path:")
    store_label.pack()

    store_entry = Entry(store_label)  # Removed "Text=" from Entry, as it's not valid for Entry widget
    store_entry.pack()

    store_bttn = Button(store_label, text="Store", command=copy_file)  # Moved this line inside store_pw()
    store_bttn.pack()

    

store_frame = Button(root, text="store password file", command= Authentication3 )
store_frame.pack()


# Lables
title = Label(main_frame, text="Password Generator")
title.pack(padx=20, pady=0)

length = Label(secondary_frame, text="Length of Password (10-20):")
length.grid(row=0, column=0)

length_entry = Entry(secondary_frame)
length_entry.grid(row=0, column=1)

def validate_length():
    length = int(length_entry.get())
    if length >= 10:
        generate_pass()
    else:
        messagebox.showerror("Error", "Please enter a number greater than 10")
        return False
    


# Creating a function for encrypting and decrypting the .db file.
def encrypt_db():
    with open('pw.db', 'rb') as to_encrypt:
        data = to_encrypt.read()
        data = my_fernet.encrypt(data)
        with open('pw.db', "wb") as encrypt:
            encrypt.write(data)


def decrypt_db():
    with open('pw.db', 'rb') as to_decrypt:
        data = to_decrypt.read()
        data = my_fernet.decrypt(data)
        with open('pw.db', 'wb') as decrypt:
            decrypt.write(data)


# Function for saving master password
def save_master():
    # Generate a master key for writing
    with open('key.key', 'wb') as f:
        key = Fernet.generate_key()
        global my_fernet
        my_fernet = Fernet(key)
        f.seek(0)
        f.write(key)

    # Writing Encoded Master Password
    with open('pw.txt', 'wb') as f:
        f.seek(0)
        global m_password
        m_password = masterpassword.get()
        password_write = m_password.encode('utf-8')
        password_write = my_fernet.encrypt(password_write)
        f.write(password_write)
    First_time.destroy()
    root.deiconify()
    encrypt_db()


# Checking if its a first-time run.
with open('firstrun.txt', 'a+') as f:
    f.seek(0)
    f_contents = f.read()
    if f_contents == '1':
        with open('key.key', 'rb') as kf:
            kf.seek(0)
            kf_contents = kf.read()
            key = kf_contents
            my_fernet = Fernet(key)

        # Get Master Password
        with open('pw.txt', 'rb') as pf:
            pf.seek(0)
            pf_contents = pf.read()
            pf_contents = my_fernet.decrypt(pf_contents)
            pf_contents = pf_contents.decode('utf-8')
            m_password = pf_contents
    else:
        root.withdraw()
        f.seek(0)
        f.write('1')
        db = sqlite3.connect('pw.db')
        cursor = db.cursor()
        cursor.execute('''
        CREATE TABLE passwords (
        app_id VARCHAR [255],
        username_email VARCHAR [255],
        password VARCHAR [255])
        ''')
        db.commit()
        db.close()

        # First Time run Popup
        First_time = Toplevel()
        First_time.title('Setup')
        First_time.geometry('250x140')
        First_time.iconbitmap('icon_icon.ico')

        # Setting up a label frame to house entry fields
        labelframe = LabelFrame(
            First_time, text="Set a master password for all your passwords.")
        labelframe.pack(fill="both", expand="yes")
        button_frame = Frame(First_time)
        button_frame.pack()

        # Entry field for master password
        masterpassword = Entry(labelframe, width=25, show='*')
        masterpassword.pack(padx=10, pady=0)
        def show_password():
            if masterpassword.cget('show')=='*':
                masterpassword.config(show='')
            else:
                masterpassword.config(show='*')

        Check_button = Checkbutton(labelframe, text='show password', command=show_password)
        Check_button.pack()



        # Submit Button
        AddButton = Button(
            button_frame, text='Set Master Password', command=save_master)
        AddButton.pack()




# Function for launching Password Notebook
def Pw_Notebook():
    notebook = Toplevel()
    notebook.title('Password Notebook')
    notebook.geometry('390x700')
    notebook.iconbitmap('icon_icon.ico')

    # Function for reloading a the Password Notebook.
    def Pw_Notebook_reload():
        notebook.destroy()
        Pw_Notebook()

    # Function for adding and deleting passwords
    def add_pass():

        def save_pw():
            decrypt_db()
            db = sqlite3.connect('pw.db')
            cursor = db.cursor()
            cursor.execute("INSERT INTO passwords VALUES (:App, :Username, :Password)",
                           {'App': app_id_e.get(),
                            'Username': username_e.get(),
                            'Password': password_e.get()
                            })
            db.commit()
            db.close()
            encrypt_db()
            a_pass.destroy()
            Pw_Notebook_reload()
            alert('Information', 'Password Saved to Password Notebook')

        global a
    
        
        def check():
            username = username_e.get()
            app_id = app_id_e.get()
            passw = password_e.get()
            if username=="" or  app_id =="" or passw=="" :
                a=0
            else:
                a=1
            
            if a==0:
                messagebox.showerror("Error", "Please fill in all the fields.")
                return False

            else:
                save_pw()

        a_pass = Toplevel()
        a_pass.title('Add Password')
        a_pass.geometry('300x200')
        a_pass.iconbitmap('icon_icon.ico')

        pw_add_frame = LabelFrame(
            a_pass, text='Add Password', padx=10, pady=10)
        pw_add_frame.pack(padx=5, pady=5)

        another_buttn_frame = Frame(a_pass, padx=10, pady=10)
        another_buttn_frame.pack(padx=0, pady=15)

        app_id = Label(pw_add_frame, text="URL: ")
        app_id.grid(row=0, column=0)
        app_id_e = Entry(pw_add_frame)
        app_id_e.grid(row=0, column=1)

        username = Label(pw_add_frame, text="Username/Email: ")
        username.grid(row=1, column=0)
        username_e = Entry(pw_add_frame)
        username_e.grid(row=1, column=1)

        password_label = Label(pw_add_frame, text='Password: ')
        password_label.grid(row=2, column=0)

        password_e = Entry(pw_add_frame)
        password_e.grid(row=2, column=1)

        # Submit Button
        Add_record_bttn = Button(
            another_buttn_frame, text="Add Password", command=check)
        Add_record_bttn.pack()

    def delete_pass():
        def delete_pw():
            decrypt_db()
            db = sqlite3.connect('pw.db')
            cursor = db.cursor()
            cursor.execute("DELETE FROM passwords WHERE app_id = :app", {
                'app': app_name_delete.get()
            })
            db.commit()
            db.close()
            encrypt_db()
            a_pass.destroy()
            Pw_Notebook_reload()
            alert('Information', 'Password Deleted')

        a_pass = Toplevel()
        a_pass.title('Delete Password')
        a_pass.geometry('300x200')
        a_pass.iconbitmap('icon_icon.ico')

        pw_add_frame = LabelFrame(
            a_pass, text='Add Password', padx=10, pady=10)
        pw_add_frame.pack(padx=5, pady=5)

        another_buttn_frame = Frame(a_pass, padx=10, pady=10)
        another_buttn_frame.pack(padx=0, pady=15)

        app_name = Label(pw_add_frame, text="URL to delete: ")
        app_name.grid(row=0, column=0)
        app_name_delete = Entry(pw_add_frame)
        app_name_delete.grid(row=0, column=1)

        # Submit Button
        Add_record_bttn = Button(
            another_buttn_frame, text="Delete", command=delete_pw)
        Add_record_bttn.pack()

    # Creating an Label Frame to House Stuff.
    db_frame = LabelFrame(
        notebook, text="Passwords:")
    db_frame.pack(fill="both", expand="yes")

    # Creating another frame for housing add record button and delete.
    buttn_frame = Frame(notebook, padx=10, pady=10)
    buttn_frame.pack(padx=5, pady=25)

    # Creating Labels for the row.
    Appid_label = Label(db_frame, text="URL")
    Appid_label.grid(row=0, column=1)

    username_label = Label(db_frame, text="Username/Email")
    username_label.grid(row=0, column=2)

    password_label = Label(db_frame, text="Passwords")
    password_label.grid(row=0, column=3)

    # Acessing Our Database
    decrypt_db()
    db = sqlite3.connect('pw.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM passwords")

    # Displaying the table from our db.
    # 'i' will be used for rows, while 'j' will be used for columns.
    i = 1
    for password_sql in cursor:
        for j in range(len(password_sql)):
            numberline = str(i)
            numberline = numberline + ". "
            l = Label(db_frame, text=numberline)
            l.grid(row=i, column=0)
            e = Entry(db_frame, width=20, fg='blue')
            u = j + 1
            e.grid(row=i, column=u)
            e.insert(END, password_sql[j])
        i = i+1
    encrypt_db()

    # Creating Buttons to add or delete
    add_record = Button(buttn_frame, text='Add Password', command=add_pass)
    add_record.grid(row=0, column=0)

    delete_record = Button(
        buttn_frame, text='Delete Password', command=delete_pass)
    delete_record.grid(row=0, column=1)


# Function for launching Settings Page
def Settings():
    settings = Toplevel()
    settings.title('Settings')
    settings.geometry('300x300')
    settings.iconbitmap('icon_icon.ico')

    change_m_frame = LabelFrame(
        settings, text="Change Master Password", padx=10, pady=10)
    change_m_frame.pack(padx=10, pady=10)

    settings_buttn_frame = Frame(settings)
    settings_buttn_frame.pack(padx=10, pady=20)

    def change_m():
        with open('pw.txt', 'wb') as f:
            f.seek(0)
            global m_password
            m_password = masterpassword_new.get()
            password_write = m_password.encode('utf-8')
            password_write = my_fernet.encrypt(password_write)
            f.write(password_write)
            alert('Info', 'Master Password has been changed')

    masterpassword_new = Entry(change_m_frame, show='*')
    masterpassword_new.pack()

    def show_password():
            if masterpassword_new.cget('show')=='*':
                masterpassword_new.config(show='')
            else:
                masterpassword.config(show='*')

    Check_button = Checkbutton(change_m_frame, text='show password', command=show_password)
    Check_button.pack()
    change_m_buttn = Button(settings_buttn_frame,
                            text="Change Master Password", command=change_m)
    change_m_buttn.pack()


# Creating the Authentication Function
import time

def Authentication1():
    # Define a variable to store the last failed attempt time
    global last_failed_attempt_time
    now = time.time()
    
    if last_failed_attempt_time is not None and now - last_failed_attempt_time < 180:
        # If the user has failed authentication within the last 3 minutes, show a message
        # and do not create the authentication window again.
        alert('Too Many Attempts', 'You can retry after 3 minutes.')
        return
    
    last_failed_attempt_time = None  # Reset last_failed_attempt_time since the authentication window will be displayed

    # Creating Tkinter Window
    Authenticate = Toplevel()
    Authenticate.title('Authenticate')
    Authenticate.geometry('150x150')
    Authenticate.iconbitmap('icon_icon.ico')

    # Creating Components of the Window
    AuthenticateFrame = LabelFrame(
        Authenticate, text="Enter Master Password")
    AuthenticateFrame.pack(fill="both", expand="yes")
    button_frame1 = Frame(AuthenticateFrame)
    button_frame1.pack()
    
    def show_password():
        if m_password_entry.cget('show') == '*':
            m_password_entry.config(show='')
        else:
            m_password_entry.config(show='*')

    Check_button = Checkbutton(AuthenticateFrame, text='show password', command=show_password)
    Check_button.pack()

    # Entry Field for Password
    m_password_entry = Entry(AuthenticateFrame, width=25, show='*')
    m_password_entry.pack()

    # Where the real authentication code goes.
    # This one is for Password Notebook.:
    global failed_attempts
    failed_attempts = 0

    def RealAuthenticate3():
        global failed_attempts, last_failed_attempt_time
        m_entry = m_password_entry.get()
        if m_entry == m_password:
            Authenticate.destroy()
            Pw_Notebook()
        else:
            failed_attempts += 1
            if failed_attempts >= 3:
                m_password_entry.config(state="disabled")  # Disable the password entry
                last_failed_attempt_time = time.time()  # Set the last_failed_attempt_time to the current time
                m_password_entry.after(300000, reset_failed_attempts)
            alert('Wrong Password', 'Password is Incorrect', kind='warning')
            print(failed_attempts)

    def reset_failed_attempts():
        global failed_attempts
        failed_attempts = 0
        m_password_entry.config(state="normal")

    Auth_Button = Button(
        button_frame1, text='Authenticate', command=RealAuthenticate3)
    Auth_Button.pack()

# Initialize last_failed_attempt_time as None at the beginning of your code
last_failed_attempt_time = None


import time

def Authentication2():
    # Define a variable to store the last failed attempt time
    global last_failed_attempt_time
    now = time.time()
    
    if last_failed_attempt_time is not None and now - last_failed_attempt_time < 180:
        # If the user has failed authentication within the last 3 minutes, show a message
        # and do not create the authentication window again.
        alert('Too Many Attempts', 'You can retry after 3 minutes.')
        return
    
    last_failed_attempt_time = None  # Reset last_failed_attempt_time since the authentication window will be displayed

    # Creating Tkinter Window
    Authenticate = Toplevel()
    Authenticate.title('Authenticate')
    Authenticate.geometry('150x150')
    Authenticate.iconbitmap('icon_icon.ico')

    # Creating Components of the Window
    AuthenticateFrame = LabelFrame(
        Authenticate, text="Enter Master Password")
    AuthenticateFrame.pack(fill="both", expand="yes")
    button_frame1 = Frame(AuthenticateFrame)
    button_frame1.pack()
    
    def show_password():
        if m_password_entry.cget('show') == '*':
            m_password_entry.config(show='')
        else:
            m_password_entry.config(show='*')

    Check_button = Checkbutton(AuthenticateFrame, text='show password', command=show_password)
    Check_button.pack()

    # Entry Field for Password
    m_password_entry = Entry(AuthenticateFrame, width=25, show='*')
    m_password_entry.pack()

    # Where the real authentication code goes.
    # This one is for Password Notebook.:
    global failed_attempts
    failed_attempts = 0

    def RealAuthenticate3():
        global failed_attempts, last_failed_attempt_time
        m_entry = m_password_entry.get()
        if m_entry == m_password:
            Authenticate.destroy()
            Settings()
        else:
            failed_attempts += 1
            if failed_attempts >= 3:
                m_password_entry.config(state="disabled")  # Disable the password entry
                last_failed_attempt_time = time.time()  # Set the last_failed_attempt_time to the current time
                m_password_entry.after(300000, reset_failed_attempts)
            alert('Wrong Password', 'Password is Incorrect', kind='warning')
            print(failed_attempts)

    def reset_failed_attempts():
        global failed_attempts
        failed_attempts = 0
        m_password_entry.config(state="normal")

    Auth_Button = Button(
        button_frame1, text='Authenticate', command=RealAuthenticate3)
    Auth_Button.pack()

# Initialize last_failed_attempt_time as None at the beginning of your code
last_failed_attempt_time = None


    

# Bottom Bar Buttons
Password_Notebook_Bttn = Button(
    bottom_bar, text="Password Notebook", command=Authentication1)
Password_Notebook_Bttn.grid(row=0, column=0)


# Settings Button
Settings_Bttn = Button(bottom_bar, text="Settings", command=Authentication2)
Settings_Bttn.grid(row=1, column=0)


def alert(title, message, kind='info', hidemain=True):
    if kind not in ('error', 'warning', 'info'):
        raise ValueError('Unsupported alert kind.')

    show_method = getattr(messagebox, 'show{}'.format(kind))
    show_method(title, message)


# Function for generating Password
def generate_pass():
    password_length = int(length_entry.get())
    C = "ABCDEFGHIJKLMNOPQRSTUVWXYZADEFKLMNOPQRSTUVWXYZ"
    c = "abcdefghijklmnopqrstuvwxyz"
    n = "0123456789"
    s = "&{([-_@)]}=+*$%!?"
    generated_password = ""
    while len(generated_password) != password_length:
        if len(generated_password) < password_length:
            generated_password += random.choice(C)
        if len(generated_password) < password_length:
            generated_password += random.choice(c)
        if len(generated_password) < password_length:
            generated_password += random.choice(n)
        if len(generated_password) < password_length:
            generated_password += random.choice(s)

    def save_main():
        decrypt_db()
        db = sqlite3.connect('pw.db')
        cursor = db.cursor()
        cursor.execute("INSERT INTO passwords VALUES (:App, :Username, :Password)",
                       {'App': app_id_entry.get(),
                        'Username': username_input.get(),
                        'Password': output_e.get()
                        })
        db.commit()
        db.close()
        encrypt_db()
        alert('Information', 'Password Saved to Password Notebook')

    

    app_id_label = Label(output_frame, text="URL(example.com): ")
    app_id_label.grid(row=1, column=0)
    app_id_entry = Entry(output_frame)
    app_id_entry.grid(row=1, column=1)

    username_label = Label(output_frame, text="Username/Email: ")
    username_label.grid(row=2, column=0)
    username_input = Entry(output_frame)
    username_input.grid(row=2, column=1)

    output_label = Label(output_frame, text='Generated Password: ')
    output_label.grid(row=0, column=0)

    output_e = Entry(output_frame)
    output_e.insert(END, generated_password)
    output_e.grid(row=0, column=1)


    # Auto Copying Generated Password
    root.clipboard_clear()
    root.clipboard_append(generated_password)
    global a
    
        
    def check():
        username = username_input.get()
        app_id = app_id_entry.get()
        if username=="" or  app_id =="":
            a=0
        else:
            a=1
        
        if a==0:
            messagebox.showerror("Error", "Please fill in all the fields.")
            return False

        else:
            save_main()

    # Creating the save button
    save_main_button = Button(
        output_frame, text="Save Password", command=check)
    save_main_button.grid(row=3, column=1)
    root.geometry("300x400")

def validate_type():
    length_value = length_entry.get()
    try:
        length = int(length_value)
        validate_length()
    
    except ValueError:
        # The input is not a valid integer
        messagebox.showerror("Error", "please enter a valid number")
       


# Button for Generating Password
generate_button = Button(
    rbutton_frame, text="Generate Password", command=validate_type)
generate_button.grid(row=0, column=0)

# Text Below Button for indicating
generate_text = Label(
    rbutton_frame, text="Text will automatically be copied to clipboard.")
generate_text.grid(row=1, column=0)


# Starting the Windows
root.mainloop()






