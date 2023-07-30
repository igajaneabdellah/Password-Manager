# Password-Manager/Generator

The Password Manager is a simple yet secure application that helps users manage their passwords effectively. It allows users to generate strong and unique passwords, store them securely, and retrieve them when needed. The application provides an easy-to-use graphical user interface (GUI) built using the Tkinter library in Python.

# Features
*Password Generation: Users can generate strong and random passwords with a specified length.
*Password Storage: Encrypted passwords are stored in a local database file for added security.
*Master Password Authentication: Users must enter a master password to access the password manager.
*Password Retrieval: Users can retrieve stored passwords by providing the relevant account or website name.
*Show/Hide Password: Users can toggle password visibility for added convenience.
*Journalization and Reporting: All activities and events are logged and sent to a local log file for monitoring and reporting.

# usage
*Launch the application by running password_manager.py.

*Authenticate: Upon launching, the application will prompt you to enter the master password. If it's your first time using the manager, you'll be asked to set a master password.

*Main Window: Once authenticated, the main window will appear, providing options to generate passwords, store passwords, and retrieve passwords.

*Generate Password: Click on the "Generate Password" button to create a strong password with the desired length.

*Store Password: To store a password, click on the "Store Password" button and provide the account/website name and the corresponding password.

*Retrieve Password: Click on the "Retrieve Password" button, and a prompt will ask you to enter the account/website name whose password you want to retrieve.

*Show/Hide Password: To toggle password visibility, check the "Show Password" box before entering a master password or storing/retrieving a password.


# security
The application uses Fernet encryption to securely store passwords in a local database file.

Failed authentication attempts are limited to three, after which the master password entry is disabled for five minutes.

All log activities are sent to a syslog server for centralized logging and monitoring.


# Journalization and Reporting

All activities and events in the password manager, such as password generation, storage, and retrieval, are logged.

The logging is implemented using the Python logging library.

Log messages are sent to a centralized log server using the SysLogHandler from the syslog-rfc5424-logging-handler package.


# Reporting

A report summarizing the password manager's usage and activities can be generated automatically.

The report includes information such as the number of passwords generated, passwords stored, and passwords retrieved.

The report is automatically generated and saved to a local file in the current working directory.





