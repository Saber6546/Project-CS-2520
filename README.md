# Expense Tracker with Visualization

![Expense Tracker]((https://github.com/Saber6546/Project-CS-2520/blob/main/image1.PNG?raw=true))


## Introduction

The **Expense Tracker** is a Python-based application designed to simplify personal finance management. It allows users to efficiently record and categorize their daily expenditures, enabling them to monitor spending patterns and maintain a clear view of their financial status. This tool addresses the common challenge of managing personal finances, which often leads to overspending, by providing a straightforward platform for tracking and analyzing expenses.

## Features

- **User Authentication:** Secure login and registration using SQLite3.
- **Data Entry Interface:** Easy input for expenses, including date, category, and amount.
- **Data Visualization:** Generate insightful visualizations using Matplotlib and Seaborn.
- **Expense Categorization:** Organize expenses by category for better budgeting.
- **Trend Analysis:** Track monthly spending patterns over time.

## Technologies Used

- **Python:** Core programming language for the application.
- **SQLite3:** Used for user authentication and data storage.
- **Tkinter:** Provides a graphical user interface (GUI) for easy interaction.
- **Pandas:** Manages and manipulates expense data.
- **Matplotlib and Seaborn:** Libraries for creating visualizations.

## Usage

### Login Interface

**Registration:**

- **Username:** Enter a unique username.
- **Password:** Enter a password.
- **Register Button:** Click to create a new user account. If the username is already taken, an error message will appear.

**Login:**

- **Username:** Enter your registered username.
- **Password:** Enter your password.
- **Login Button:** Click to access the expense tracker. If the credentials are incorrect, an error message will appear.

### Data Entry Interface

**Adding Expenses:**

- **Date:** Enter the date of the expense (YYYY-MM-DD).
- **Category:** Enter a category for the expense (e.g., groceries, utilities).
- **Amount:** Enter the amount spent (numerical value).
- **Add Expense Button:** Click to record the expense. A confirmation message will appear if the expense is added successfully.

### Visualization

- **Visualize Button:** Click to display a visual representation of expenses.
  - **Bar Graph:** Categorizes total expenses by category.
  - **Line Graph:** Depicts monthly expenses over time to track spending patterns.

### Data Storage

The expense data is stored in a CSV file with the following structure:

- **Date:** Date of the expense in the format YYYY-MM-DD.
- **Category:** Category of the expense (e.g., "Food," "Utilities").
- **Amount:** Monetary value of each expense.

Here's how the data might be structured in the CSV file:

| Date       | Category     | Amount |
|------------|--------------|--------|
| 2024-07-01 | Groceries    | 50.00  |
| 2024-07-02 | Utilities    | 75.00  |
| 2024-07-03 | Entertainment| 30.00  |
