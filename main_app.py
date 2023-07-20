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
            db.execute('INSERT INTO passwords VALUES (:URL, :Username, :Password)',
                        {'URL':URL_e.get(),
                         'Username':username_e.get(),
                         'Password':password_e.get()
                         })
            db.commit()
            db.close()
            encrypt_db()
            a_pass.destroy()
            Pw_Notebook_reload()
            alert('information','Pw saved to notebook ')

        a_pass=Toplevel()
        a_pass.title("add Password")
        a_pass.geometry("300x200")
        a_pass.iconbitmap("pdlock.ico")

        pw_add_frame = LabelFrame(
            a_pass, text='Add Password', padx=10, pady=10)
        pw_add_frame.pack(padx=0,pady=15)

        another_button_frame = Frame(a_pass, padx=10, pady=10)
        another_button_frame.pack(padx=0, pady=10)

        URL=Label(pw_add_frame, text='URL')
        URL.grid(row=0, column=0)
        URL_e = Entry(pw_add_frame)
        URL_e.grid(row=0, column=1)

        username = Label(pw_add_frame,text = 'username/email')
        username.grid(row=1, column=0)
        username_e = Entry(pw_add_frame)
        username_e.grid(row=1, column=1)

        password = Label(pw_add_frame, text='password')
        password.grid(row=2, column=0)
        password_e=Entry(pw_add_frame)
        password_e.grid(row=2, column=1)

        submit_bttn = Button(another_button_frame, text='SUBMIT', command=save_pw)
        submit_bttn.pack()


    def delete_pass():
        def delete_pw():
            decrypt_db()
            db = sqlite3.connect('pw.db')
            cursor = db.cursor()
            cursor.execute("DELETE FROM passwords WHERE URL_id = :URL", {
                'URL': URL_delete.get()
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
        a_pass.iconbitmap('pdlock.ico')

        pw_add_frame = LabelFrame(
            a_pass, text='Add Password', padx=10, pady=10)
        pw_add_frame.pack(padx=5, pady=5)

        another_buttn_frame = Frame(a_pass, padx=10, pady=10)
        another_buttn_frame.pack(padx=0, pady=15)

        URL_id = Label(pw_add_frame, text="URL to delete: ")
        URL_id.grid(row=0, column=0)
        URL_delete = Entry(pw_add_frame)
        URL_delete.grid(row=0, column=1)

        # Submit Button
        Add_record_bttn = Button(
            another_buttn_frame, text="Delete", command=delete_pw)
        Add_record_bttn.pack()


    db_frame = Frame(notebook, text="Passwords:")
    db_frame.pack(fill="both", expand="yes")


    buttn_frame = Frame(notebook, padx=10,pady=0)
    buttn_frame.pack(padx=5, pady=25)

    URL_label = Label(db_frame, text="URL")
    URL_label.grid(row=0, column=1)

    username_label = Label(db_frame, text="username")
    username_label.grid(row=0, column=2)

    password_label = Label(db_frame, text="password")
    password_label.grid(row=0, column=3)

    decrypt_db()
    db = sqlite3.connect('pw.db')
    cursor=db.cursor()
    cursor.execute("SELECT * FROM passwords")

    i=1
    for password_line in cursor:
        for j in password_line :
            line = str(i)
            line_label=Label(db_frame, text=line+'.')
            line_label.grid(row=i, column=0)
            e=Entry(db_frame, width=20, fg=blue)
            e.grid(row=i, column=j+1)
            e.insert(END, password_line[j])
        i+=1
    encrypt_db()

    #creating buttons for add and delete
    add_record = Button(buttn_frame, text='Add Password', command=add_pass)
    add_record.grid(row=0, column=0)

    delete_record = Button(
        buttn_frame, text='Delete Password', command=delete_pass)
    delete_record.grid(row=0, column=1)

    def Settings():
        settings=Toplevel()
        settings.title("Settings")
        settings.geometry("300x300")
        settings.iconbitmap('pdlock.ico')

        change_m_frame = LabelFrame(settings, text='Change Master Password', padx=10, pady=10 )
        change_m_frame.pack(padx=10, pady=10)

        settings_buttn_frame=Frame(settings)
        settings_buttn_frame.pack(padx=10, pady=20)

        def change_m():
            with open('pw.txt','wb') as f:
                f.seek(0)
                global m_password
                m_password = masterpassword_new.get()
                password_write = m_password.encode('utf-8')
                password_write = my_fernet.encrypt(password_write)
                f.write(password_write)
                alert('info', 'Master password changed successfully')


        masterpassword_new = Entry(change_m_frame)
        masterpassword_new.pack()

        change_m_buttn = Button(change_m_frame, text='change master password', command= change_m)
        change_m_buttn.pack()

    def Authenticate1():

        Authenticate = Toplevel()
        Authenticate.title("Authenticate")
        Authenticate.geometry("150x150")
        Authenticate.iconbitmap("padlock.ico")

        auth_frame = LabelFrame(Authenticate, text='Enter Master Password')
        auth_frame.pack(fill="both", expand="yes")

        button_frame1 = Frame(auth_frame)
        button_frame1.pack()

        m_password_entry=Entry(auth_frame, width=30)
        m_password_entry.pack()

        def main_authentication1():

            m_entry=m_password_entry.get()
            if m_entry == m_password: 
                Authenticate.destroy()
                Pw_Notebook()

            else:
                alert("wrong password", kind="Warning")
        Auth_Button = Button(button_frame1, text='Authenticate', command=main_authentication1)
        Auth_Button.pack()

        def Authenticate2():

            Authenticate = Toplevel()
            Authenticate.title("Authenticate")
            Authenticate.geometry("150x150")
            Authenticate.iconbitmap("padlock.ico")

            auth_frame = LabelFrame(Authenticate, text='Enter Master Password')
            auth_frame.pack(fill="both", expand="yes")

            button_frame1 = Frame(auth_frame)
            button_frame1.pack()

            m_password_entry=Entry(auth_frame, width=30)
            m_password_entry.pack()

            def main_authentication2():

                m_entry=m_password_entry.get()
                if m_entry == m_password: 
                    Authenticate.destroy()
                    Settings()

                else:
                    alert("wrong password", kind="Warning")
            Auth_Button = Button(button_frame1, text='Authenticate', command=main_authentication2)
            Auth_Button.pack()
            


                















root.mainloop()
