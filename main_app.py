from tkinter import *
from cryptography.fernet import Fernet
import sqlite3
my_fernet = ''

root = Tk()
root.geometry("300x300")
root.title("Password manager/generator")

main_frame = Frame(root, padx=5, pady=5)
secondary_frame = Frame(root, padx=5, pady=5)
rbutton_frame = Frame(root, padx=5, pady=5)
output_frame = Frame(root, padx=5, pady=5)
bottom_bar = Frame(root, padx=5, pady=5)

main_frame.pack(padx=20, pady=0)
secondary_frame.pack(padx=20, pady=0)
rbutton_frame.pack(padx=20, pady=0)
output_frame.pack(padx=20, pady=0)
bottom_bar.pack(side=BOTTOM)

title = Label(main_frame, text="Password Generator")
title.pack(padx=20, pady=0)

length = Label(secondary_frame, text="password length (8-20)")
length.grid(row=0, column=0)

length_entry = Entry(secondary_frame)
length_entry.grid(row=0, column=1)

#encrypting and decrypting db file

def encrypt_db():
    with open('pw.db', 'rb') as to_encrypt:
        data = to_encrypt.read()
        data = my_fernet.encrypt(data)
        with open('pw.db', 'wb') as encrypt:
            encrypt.write(data)


def decrypt_db():
    with open('pw.db', "rb") as to_decrypt:
        data = to_decrypt.read()
        data = my_fernet.decrypt(data)
        with open('pw.db', 'wb') as decrypt:
            decrypt.write(data)


#saving master password

def save_master():
    with open('key.key', 'wb') as f:
        key = Fernet.generate_key()
        global my_fernet
        my_fernet = Fernet(key)
        f.seek(0)
        f.write(key)


    with open('pw.txt', 'wb') as f:
        f.seek(0)
        global m_password
        m_password = masterpassword.get()
        m_password = m_password.encode('utf-8')
        m_password = my_fernet.encrypt(m_password)
        f.write(m_password)
    First_time.destroy()
    root.deiconify()
    encrypt_db()

#cheking if it's first time run

with open('firstrun.txt', 'a+') as f:
    f.seek(0)
    f_contents = f.read()
    if f_contents == '1':
        with open('key.key' ,'rb') as kf:
            kf.seek(0)
            key = kf.read()
            my_fernet= Fernet(key)


        #getting master pw
        with open('pw.txt', 'rb') as pf:
            pf.seek(0)
            pf_contents = pf.read()
            pf_contents = my_fernet.decrypt(pf_contents)
            pf_contents = pf_contents.decode('utf-8')
            m_password = pf_contents

    else:
        root.withdraw()
        f.seek(0)
        f.wrie('1')
        db = sqlite3.connect('pw.db')
        cursor = db.cursor()
        db.execute("""
            CREATE TABLE Passwords(
                   URL VARCHAR(255),
                   username VARCHAR(255),
                   password VARCHAR(255))
                   """)
        db.commit()
        db.close()

        #setting up first-time pop-up
        First_time = Toplevel()
        First_time.title('first-use')
        First_time.geometry('250x250')
        First_time.iconbitmap('padlock.ico')

        #setting up the label for first time
        labelframe = LabelFrame(
            First_time, text="Set a master password for all your passwords.")
        labelframe.pack(fill="both", expand="yes")
        button_frame = Frame(First_time)
        button_frame.pack()

        masterpassword = Entry(labelframe, width=25)
        masterpassword.pack(padx=10, pady=0)

        AddButton = Button(
            button_frame, text='Set Master Password', command=save_master)
        AddButton.pack()

def Pw_Notebook():
    notebook = Toplevel()
    notebook.title('Password Notebook')
    notebook.geometry('390x700')
    notebook.iconbitmap('pdlock.ico')

    def Pw_Notebook_reload():
        notebook.destroy()
        Pw_Notebook()


    def add_pass():

        def save_pw():
            decrypt_db()
            db = sqlite3.connect()
            cursor = db.cursor()
            db.execute('INSERT INTO passwords VALUES (:App, :Username, :Password)',
                        {'App':app_id_e.get(),
                         'Username':username_e.get(),
                         'Password':password.get()
                         })
            db.commit()
            db.close()
            encrypt_db()
            a_pass.destroy()
            Pw_Notebook_reload()
            alert('information','Pw saved to notebook ')

        a_pass=Toplevel()
        a_pass.title("add Password")
        a_pass.geometry


        







root.mainloop()
