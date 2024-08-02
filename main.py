import sqlite3
from tkinter import *
from tkinter import messagebox
import config
import tracker

# Global variable to store the current user's expense file path
current_user_expense_file = None

def setup_database():
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    # Check if the users table has an 'expense_file' column
    c.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in c.fetchall()]
    if "expense_file" not in columns:
        # If the 'expense_file' column does not exist, add it to the table
        c.execute("ALTER TABLE users ADD COLUMN expense_file TEXT")
    # Ensure the users table exists with appropriate columns
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    expense_file TEXT)''')
    conn.commit()
    conn.close()

def register_user():
    username = entry_username.get()
    password = entry_password.get()
    # Set a unique file name for each user's expenses
    expense_file = f'expenses_{username}.csv'
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    try:
        # Insert new user with a designated expense file into the database
        c.execute('INSERT INTO users (username, password, expense_file) VALUES (?, ?, ?)', (username, password, expense_file))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        conn.close()

def login_user():
    global current_user_expense_file
    username = entry_username.get()
    password = entry_password.get()
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    # Fetch the expense file path for the logged-in user
    c.execute('SELECT expense_file FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        current_user_expense_file = user[0]
        root.destroy()  # Close the login window
        # Open the expense tracker with the user-specific expense file
        tracker.open_expense_tracker(current_user_expense_file)
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# GUI setup for user registration and login
def open_login_window():
    # Declare global variables to make them accessible outside this function
    global entry_username, entry_password, root
    
    # Initialize the main window of the application
    root = Tk()
    # Set the title of the main window
    root.title("User Database Management System")
    # Define the dimensions of the main window using settings from the config module
    root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
    # Set the background color of the main window using settings from the config module
    root.configure(bg=config.BACKGROUND_COLOR)

    # Create a frame widget which will contain other widgets like labels, entries, and buttons
    frame = Frame(root, bg=config.BACKGROUND_COLOR)
    frame.pack(expand=True)

    # Create and configure a label for the username input
    label_username = Label(frame, text="Username", font=("Arial", config.FONT_SIZE_LABEL), fg=config.TEXT_COLOR, bg=config.BACKGROUND_COLOR)
    # Positioning the username label 
    label_username.grid(row=0, column=0, padx=10, pady=10, sticky=E)
    # Create an entry widget for the username
    entry_username = Entry(frame, font=("Arial", config.FONT_SIZE_ENTRY))
    # Positioning the username entry 
    entry_username.grid(row=0, column=1, padx=10, pady=10, sticky=W)

    # Create and configure a label for the password input
    label_password = Label(frame, text="Password", font=("Arial", config.FONT_SIZE_LABEL), fg=config.TEXT_COLOR, bg=config.BACKGROUND_COLOR)
    # Positioning the password label
    label_password.grid(row=1, column=0, padx=10, pady=10, sticky=E)
    # Create an entry widget for the password, enable password hiding, set its font, and add it to the frame
    entry_password = Entry(frame, show='*', font=("Arial", config.FONT_SIZE_ENTRY))
    # Positioning the password entry 
    entry_password.grid(row=1, column=1, padx=10, pady=10, sticky=W)

    # Create a button for user registration and configure it with a command, background color, and font
    button_register = Button(frame, text="Register", command=register_user, bg=config.BUTTON_COLOR, font=("Arial", config.FONT_SIZE_BUTTON))
    # Positioning the register button 
    button_register.grid(row=2, column=0, padx=10, pady=10)

    # Create a button for user login and configure it with a command, background color, and font
    button_login = Button(frame, text="Login", command=login_user, bg=config.BUTTON_COLOR, font=("Arial", config.FONT_SIZE_BUTTON))
    # Positioning the login button 
    button_login.grid(row=2, column=1, padx=10, pady=10)

    # Create an exit button and configure it with a command, background color, and font
    button_exit = Button(frame, text="Exit", command=root.quit, bg=config.BUTTON_COLOR, font=("Arial", config.FONT_SIZE_BUTTON))
    # Positioning the exit button 
    button_exit.grid(row=3, column=0, columnspan=2, pady=20)

    setup_database()
    root.mainloop()


if __name__ == "__main__":
    open_login_window()
