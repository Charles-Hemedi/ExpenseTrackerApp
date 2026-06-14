# Expense Tracker - SQL Relational Database Project

# How to Run the Project (3 Steps)

### Step 1: Install Python
- Check: Open terminal and run  python --version
- Download from: https://www.python.org

### Step 2: Navigate to the project folder
### Step 3: Run the application
	python expense_tracker.py
	A GUI window will open where you can manage your expenses

## Project Overview
This Expense Tracker is a complete SQL relational database application built with Python and SQLite.It demonstrates full CRUD operations, aggregate functions, date filtering, user authentication, and real-time financial tracking.

## Key Features
- User Registration & Authentication: Secure login and registration system with password hashing
- Add Expenses	: Track purchases with title, amount, category, and date
- Update Expenses: Modify existing expenses easily
- Delete Expenses: Remove unwanted entries
- View Stats: See total and average spending in real-time
- Date Filtering: Filter expenses by any date range
- Income & Balance Tracking	: Set your initial income and watch your balance update as you spend
- User-Friendly GUI: Clean, intuitive interface with visual feedback


## Tech Stack
- Language: Python 3
- Database: SQLite (built-in)
- GUI Framework: Tkinter (built-in)
- No External Dependencies


## How to Use the Application

### 1. Registration & Login
1. When you start the application, you'll see the login screen
2. Register: Enter a username and password, then click "Register"
3. Login: Enter your username and password, then click "Login"

### 2. Setting Up Your Income
1. After logging in, you'll see the main screen
2. In the "Finances" section, enter your total income
3. Click "Set Income" - this will also reset your balance to match this income
4. You can reset your balance to match your income at any time by clicking "Reset Balance"

### 3. Adding an Expense
1. Fill in the title (required), amount (required), category (optional), and date (required)
2. Click Add Expense - the expense will be saved and your balance will update automatically!

### 4. Updating an Expense
1. Select an expense from the table
2. Modify the details in the input fields
3. Click Update Selected - your balance will be adjusted to reflect the change

### 5. Deleting an Expense
1. Select an expense from the table
2. Click Delete Selected
3. Confirm the deletion - the expense amount will be added back to your balance

### 6. Filtering by Date
1. Enter a start and end date in the filter section
2. Click Filter
3. To see all expenses again, click Show All


