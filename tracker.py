import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import *
from tkinter import messagebox
import os
import config
import main  

def load_data(expense_file):
    # Check if the expense file exists and if not, initialize a new DataFrame with required columns.
    if expense_file and os.path.exists(expense_file):
        try:
            # Load the expense data from the file.
            df = pd.read_csv(expense_file)
            # Initialize a new DataFrame if the loaded data is empty.
            if df.empty:
                df = pd.DataFrame(columns=['Date', 'Category', 'Amount'])
        except pd.errors.EmptyDataError:
            # Handle empty or corrupt files by initializing a new DataFrame.
            df = pd.DataFrame(columns=['Date', 'Category', 'Amount'])
    else:
        # Create a new DataFrame if the file does not exist.
        df = pd.DataFrame(columns=['Date', 'Category', 'Amount'])
    return df

def save_data(expense_file, date, category, amount):
    # Load existing data or initialize a new DataFrame.
    df = load_data(expense_file)
    # Create a new DataFrame for the new expense record.
    new_expense = pd.DataFrame([[date, category, amount]], columns=['Date', 'Category', 'Amount'])
    # Append the new record to the existing DataFrame.
    df = pd.concat([df, new_expense], ignore_index=True, sort=False)
    # Save the updated DataFrame back to the CSV file.
    df.to_csv(expense_file, index=False)

def clear_expenses(expense_file):
    # Function to clear all expenses by truncating the expense file.
    if expense_file:
        open(expense_file, 'w').close()

def add_expense(expense_file, date, category, amount):
    # Save the new expense data to the file.
    save_data(expense_file, date, category, amount)
    # Print confirmation message to the console.
    print("Expense added successfully!")

def visualize_expenses(expense_file):
    # Load the data and check if it is empty.
    df = load_data(expense_file)
    if df.empty:
        messagebox.showinfo("Info", "No expenses to visualize.")
        return
    # Prepare the data for visualization.
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df = df.dropna(subset=['Amount'])
    
    # Set up the plot.
    plt.figure(figsize=(12, 6))
    # Plot total expenses by category.
    plt.subplot(1, 2, 1)
    sns.barplot(data=df, x='Category', y='Amount', estimator=sum)
    plt.title('Total Expenses by Category')
    plt.xticks(rotation=45)
    
    # Plot monthly expenses over time.
    plt.subplot(1, 2, 2)
    monthly_expenses = df.groupby('Month')['Amount'].sum().reset_index()
    monthly_expenses['Month'] = monthly_expenses['Month'].astype(str)
    
    sns.lineplot(data=monthly_expenses, x='Month', y='Amount')
    plt.title('Monthly Expenses')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()

def open_expense_tracker(expense_file):
    # Initialize the main GUI window for the expense tracker.
    tracker_window = Tk()
    tracker_window.title("Expense Tracker")
    tracker_window.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
    tracker_window.configure(bg=config.BACKGROUND_COLOR)

    # Define GUI callbacks and elements.
    def add_expense_gui():
        # Fetch values from GUI inputs.
        date = entry_date.get()
        category = entry_category.get()
        amount_str = entry_amount.get()
        
        try:
            # Validate and convert the amount input.
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid positive number.")
            return
        
        # Add the expense to the file and display a success message.
        add_expense(expense_file, date, category, amount)
        messagebox.showinfo("Success", "Expense added successfully!")
        clear_fields()

    def clear_fields():
        # Clear input fields after submitting an expense.
        entry_date.delete(0, END)
        entry_category.delete(0, END)
        entry_amount.delete(0, END)

    def clear_expenses_gui():
        # Clear all expense records from the file.
        clear_expenses(expense_file)
        messagebox.showinfo("Success", "All expenses cleared.")

    def visualize_expenses_gui():
        # Display visualizations of expenses.
        visualize_expenses(expense_file)

    def logout():
        # Destroy the tracker window and open the login window.
        tracker_window.destroy()
        main.open_login_window()

    # Create the main frame that fills the entire window, with background color set from config
    frame = Frame(tracker_window, bg=config.BACKGROUND_COLOR)
    frame.pack(expand=True, fill=BOTH)

    # Create an inner frame that will hold all user input fields and buttons, centered within the main frame
    inner_frame = Frame(frame, bg=config.BACKGROUND_COLOR)
    inner_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Create and place a label for the 'Date'
    label_date = Label(inner_frame, text="Date (YYYY-MM-DD): ", font=("Arial", config.FONT_SIZE_LABEL), fg=config.TEXT_COLOR, bg=config.BACKGROUND_COLOR)
    # Positioning the label
    label_date.grid(row=0, column=0, pady=5, sticky=E)
    # Create an entry field for entering the date of the expense
    entry_date = Entry(inner_frame, font=("Arial", config.FONT_SIZE_ENTRY))
    entry_date.grid(row=0, column=1, pady=5, sticky=W)

    # Create and place a label for the 'Category'
    label_category = Label(inner_frame, text="Category: ", font=("Arial", config.FONT_SIZE_LABEL), fg=config.TEXT_COLOR, bg=config.BACKGROUND_COLOR)
    # Positioning the label
    label_category.grid(row=1, column=0, pady=5, sticky=E)
    # Create an entry field for entering the category of the expense
    entry_category = Entry(inner_frame, font=("Arial", config.FONT_SIZE_ENTRY))
    entry_category.grid(row=1, column=1, pady=5, sticky=W)

    # Create and place a label for the 'Amount'
    label_amount = Label(inner_frame, text="Amount: ", font=("Arial", config.FONT_SIZE_LABEL), fg=config.TEXT_COLOR, bg=config.BACKGROUND_COLOR)
    # Positioning the label
    label_amount.grid(row=2, column=0, pady=5, sticky=E)
    # Create an entry field for entering the amount of the expense
    entry_amount = Entry(inner_frame, font=("Arial", config.FONT_SIZE_ENTRY))
    entry_amount.grid(row=2, column=1, pady=5, sticky=W)

    # Create a button for adding the expense to the system
    button_add_expense = Button(inner_frame, text="Add Expense", command=add_expense_gui, bg=config.BUTTON_COLOR, font=("Arial", config.FONT_SIZE_BUTTON))
    # Positioning the button
    button_add_expense.grid(row=3, column=0, pady=10, columnspan=2)

    # Create a button for clearing all expenses from the system
    button_clear = Button(inner_frame, text="Clear All Expenses", command=clear_expenses_gui, bg=config.BUTTON_COLOR, font=("Arial", config.FONT_SIZE_BUTTON))
    # Positioning the button
    button_clear.grid(row=4, column=0, pady=10, columnspan=2)

    # Create a button to visualize the recorded expenses in graphical form
    button_visualize = Button(inner_frame, text="Visualize Expenses", command=visualize_expenses_gui, bg=config.BUTTON_COLOR, font=("Arial", config.FONT_SIZE_BUTTON))
    # Positioning the button
    button_visualize.grid(row=5, column=0, pady=10, columnspan=2)

    # Create a logout button
    button_logout = Button(inner_frame, text="Logout", command=logout, bg=config.BUTTON_COLOR, font=("Arial", config.FONT_SIZE_BUTTON))
    # Positioning the button
    button_logout.grid(row=6, column=0, pady=10, columnspan=2)
    
    # Create an exit button
    button_exit = Button(inner_frame, text="Exit", command=tracker_window.quit, bg=config.BUTTON_COLOR, font=("Arial", config.FONT_SIZE_BUTTON))
    # Positioning the button
    button_exit.grid(row=7, column=0, pady=10, columnspan=2)

    tracker_window.mainloop()
