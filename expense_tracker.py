import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import hashlib


class ExpenseTracker:
    def __init__(self, root):
        """
        Initialize the entire Expense Tracker application.
        
        This sets up the main window, connects to the database,
        and shows the login screen to get the user started.
        """
        # Configure the main window settings
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("1100x700")

        # Connect to our SQLite database 
        self.conn = sqlite3.connect("expenses.db")
        self.cursor = self.conn.cursor()

        # Store logged-in user info
        self.current_user_id = None
        self.current_username = None

        # Create tables and handle any database migrations first
        self.create_tables()
        # Then show the login screen
        self.show_login_screen()

    def create_tables(self):
        """
        Set up the database schema with our two main tables.
        
        Creates both a users table (for logins and finances)
        and an expenses table (for tracking expenses) if they don't already exist.
        """
        try:
            # Create the users table for authentication and financial data
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                income REAL DEFAULT 0,
                balance REAL DEFAULT 0
            )
            """)
            print("Users table created/already exists")

            # Create the expenses table with user association
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT,
                date TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """)
            print("Expenses table created/already exists")

            self.conn.commit()

            # Make sure database has all latest columns (migration)
            self.migrate_database()

        except Exception as e:
            print(f"Error creating tables: {e}")

    def migrate_database(self):
        """
        Check and add any missing columns to our existing tables.
        
        This ensures the app works with older versions of the database
        by adding income/balance and user_id columns if needed.
        """
        try:
            # First check the users table for income and balance columns
            self.cursor.execute("PRAGMA table_info(users)")
            user_columns = [column[1] for column in self.cursor.fetchall()]
            print(f"Current columns in users: {user_columns}")

            if "income" not in user_columns:
                self.cursor.execute("ALTER TABLE users ADD COLUMN income REAL DEFAULT 0")
                self.conn.commit()
                print("Added income column to users")

            if "balance" not in user_columns:
                self.cursor.execute("ALTER TABLE users ADD COLUMN balance REAL DEFAULT 0")
                self.conn.commit()
                print("Added balance column to users")

            # Now check the expenses table for user_id column
            self.cursor.execute("PRAGMA table_info(expenses)")
            expense_columns = [column[1] for column in self.cursor.fetchall()]
            print(f"Current columns in expenses: {expense_columns}")

            if "user_id" not in expense_columns:
                self.cursor.execute("ALTER TABLE expenses ADD COLUMN user_id INTEGER DEFAULT 1")
                self.conn.commit()
                print("Added user_id column to expenses")

        except Exception as e:
            print(f"Migration error: {e}")

    def hash_password(self, password):
        """
        Convert a plain text password into a secure hash using SHA-256.
        
        Never stores passwords in plain text for security purposes.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def show_login_screen(self):
        """
        Display the login and registration form to the user.
        
        Clears any previous widgets and builds a clean login interface.
        """
        # Clear all widgets from the window first
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a centered frame for our login form
        login_frame = tk.Frame(self.root, padx=50, pady=50)
        login_frame.pack(expand=True)

        # Add app title
        tk.Label(login_frame, text="Expense Tracker", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        # Username input field
        tk.Label(login_frame, text="Username:", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.E, pady=10)
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), width=25)
        self.username_entry.grid(row=1, column=1, pady=10)

        # Password input field (show asterisks instead of characters)
        tk.Label(login_frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.E, pady=10)
        self.password_entry = tk.Entry(login_frame, show="*", font=("Arial", 12), width=25)
        self.password_entry.grid(row=2, column=1, pady=10)

        # Add login and register buttons
        buttons_frame = tk.Frame(login_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=20)

        tk.Button(buttons_frame, text="Login", command=self.login, bg="#4CAF50", fg="white", padx=30, pady=8, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(buttons_frame, text="Register", command=self.register, bg="#2196F3", fg="white", padx=30, pady=8, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

    def login(self):
        """
        Authenticate the user's login credentials.
        
        Verifies that the username and hashed password match
        an existing record in the database.
        """
        print("Login button clicked!")
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # First make sure both fields are filled
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return

        # Hash the password for secure comparison
        hashed_password = self.hash_password(password)
        print(f"Attempting login for user: {username}")
        self.cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = self.cursor.fetchone()

        if user:
            # Login was successful!
            self.current_user_id = user[0]
            self.current_username = username
            print(f"User {username} logged in with ID: {self.current_user_id}")
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.show_main_app()
        else:
            # Invalid credentials
            messagebox.showerror("Error", "Invalid username or password!")

    def register(self):
        """
        Create a brand new user account.
        
        Checks for unique username and creates a new record
        with hashed password, 0 income and 0 balance.
        """
        print("Register button clicked!")
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return

        hashed_password = self.hash_password(password)

        try:
            self.cursor.execute("INSERT INTO users (username, password, income, balance) VALUES (?, ?, 0, 0)", (username, hashed_password))
            self.conn.commit()
            print(f"Registered user {username} successfully!")
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            self.password_entry.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

    def logout(self):
        """
        Log the current user out and return to login screen.
        
        Resets user info and re-shows the login form.
        """
        self.current_user_id = None
        self.current_username = None
        self.show_login_screen()

    def show_main_app(self):
        """
        Display the main expense management interface.
        
        This is the main GUI where users add, update, delete,
        and view their expenses, and manage their finances.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        # Header with user info and logout button
        header_frame = tk.Frame(self.root, padx=10, pady=10)
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text=f"Welcome, {self.current_username}!", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        tk.Button(header_frame, text="Logout", command=self.logout, bg="#f44336", fg="white", padx=20, pady=5).pack(side=tk.RIGHT)

        # Income and Balance management section
        finance_frame = tk.Frame(self.root, padx=10, pady=10, bg="#e8f5e9")
        finance_frame.pack(fill=tk.X)

        tk.Label(finance_frame, text="💰 Finances", font=("Arial", 14, "bold"), bg="#e8f5e9").grid(row=0, column=0, columnspan=4, pady=5, sticky="w")

        tk.Label(finance_frame, text="Income:", font=("Arial", 11), bg="#e8f5e9").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.income_entry = tk.Entry(finance_frame, width=15)
        self.income_entry.grid(row=1, column=1, pady=5)
        tk.Button(finance_frame, text="Set Income", command=self.set_income, bg="#4CAF50", fg="white", padx=10).grid(row=1, column=2, pady=5, padx=10)
        tk.Button(finance_frame, text="Reset Balance", command=self.reset_balance, bg="#FF9800", fg="white", padx=10).grid(row=1, column=3, pady=5)

        # Balance Display
        self.income_label = tk.Label(finance_frame, text="Total Income: $0.00", font=("Arial", 12, "bold"), fg="#2e7d32", bg="#e8f5e9")
        self.income_label.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")
        self.balance_label = tk.Label(finance_frame, text="Current Balance: $0.00", font=("Arial", 12, "bold"), fg="#1976d2", bg="#e8f5e9")
        self.balance_label.grid(row=2, column=2, columnspan=2, pady=5, sticky="w")

        # App Title Section
        title_frame = tk.Frame(self.root, padx=10, pady=10)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text="Expense Tracker", font=("Arial", 20, "bold")).pack()

        # Expense Input Section
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Amount:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.amount_entry = tk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.category_entry = tk.Entry(input_frame, width=30)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.date_entry = tk.Entry(input_frame, width=15)
        self.date_entry.grid(row=1, column=3, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Action Buttons
        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.pack(fill=tk.X)

        tk.Button(button_frame, text="Add Expense", command=self.add_expense, bg="#4CAF50", fg="white", padx=20, pady=5).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update Selected", command=self.update_expense, bg="#2196F3", fg="white", padx=20, pady=5).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Selected", command=self.delete_expense, bg="#f44336", fg="white", padx=20, pady=5).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Clear Fields", command=self.clear_fields, bg="#FF9800", fg="white", padx=20, pady=5).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Refresh", command=self.refresh_expenses, bg="#9C27B0", fg="white", padx=20, pady=5).grid(row=0, column=4, padx=5)

        # Date Filter Section
        filter_frame = tk.Frame(self.root, padx=10, pady=10)
        filter_frame.pack(fill=tk.X)

        tk.Label(filter_frame, text="Filter by Date Range:").pack(side=tk.LEFT, padx=5)
        tk.Label(filter_frame, text="From:").pack(side=tk.LEFT, padx=5)
        self.filter_start = tk.Entry(filter_frame, width=12)
        self.filter_start.pack(side=tk.LEFT, padx=5)
        tk.Label(filter_frame, text="To:").pack(side=tk.LEFT, padx=5)
        self.filter_end = tk.Entry(filter_frame, width=12)
        self.filter_end.pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Filter", command=self.filter_by_date, bg="#607D8B", fg="white", padx=15, pady=3).pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Show All", command=self.refresh_expenses, bg="#607D8B", fg="white", padx=15, pady=3).pack(side=tk.LEFT, padx=5)

        # Statistics Section
        stats_frame = tk.Frame(self.root, padx=10, pady=10)
        stats_frame.pack(fill=tk.X)

        self.total_label = tk.Label(stats_frame, text="Total Spent: $0.00", font=("Arial", 12, "bold"), fg="#c62828")
        self.total_label.pack(side=tk.LEFT, padx=20)

        self.average_label = tk.Label(stats_frame, text="Average Spent: $0.00", font=("Arial", 12, "bold"), fg="#1565c0")
        self.average_label.pack(side=tk.LEFT, padx=20)

        # Expense Table Section
        tree_frame = tk.Frame(self.root, padx=10, pady=10)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Title", "Amount", "Category", "Date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Amount", text="Amount ($)")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Title", width=250)
        self.tree.column("Amount", width=100, anchor=tk.E)
        self.tree.column("Category", width=150)
        self.tree.column("Date", width=120, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Load initial data
        self.refresh_expenses()
        self.refresh_finance()

    def set_income(self):
        """
        Update the user's income and reset balance to match this new income.
        
        Validates that income is a positive number before saving.
        """
        try:
            income = float(self.income_entry.get().strip())
            if income < 0:
                messagebox.showerror("Error", "Income cannot be negative!")
                return

            self.cursor.execute("UPDATE users SET income = ?, balance = ? WHERE id = ?", (income, income, self.current_user_id))
            self.conn.commit()

            messagebox.showinfo("Success", f"Income set to ${income:.2f}!")
            self.income_entry.delete(0, tk.END)
            self.refresh_finance()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for income!")

    def reset_balance(self):
        """
        Reset the current balance to match the user's set income.
        
        Asks for confirmation first before making changes.
        """
        self.cursor.execute("SELECT income FROM users WHERE id = ?", (self.current_user_id,))
        result = self.cursor.fetchone()
        if result:
            income = result[0]
            if messagebox.askyesno("Confirm", "Reset balance to your income amount?"):
                self.cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (income, self.current_user_id))
                self.conn.commit()
                messagebox.showinfo("Success", "Balance has been reset!")
                self.refresh_finance()

    def refresh_finance(self):
        """
        Update the income and balance labels on the main screen.
        
        Fetches latest data from database and changes balance color
        (green for positive, red for negative).
        """
        self.cursor.execute("SELECT income, balance FROM users WHERE id = ?", (self.current_user_id,))
        result = self.cursor.fetchone()
        if result:
            income, balance = result
            self.income_label.config(text=f"Total Income: ${income:.2f}")
            balance_color = "#2e7d32" if balance >= 0 else "#c62828"
            self.balance_label.config(text=f"Current Balance: ${balance:.2f}", fg=balance_color)

    def add_expense(self):
        """
        Add a brand new expense to the database and update balance.
        
        Validates inputs, inserts expense, subtracts from balance,
        and refreshes all displays.
        """
        print("Add Expense button clicked!")
        title = self.title_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        date = self.date_entry.get().strip()

        print(f"Inputs - Title: '{title}', Amount: '{amount_str}', Category: '{category}', Date: '{date}'")
        print(f"Current user ID: {self.current_user_id}")

        if not title or not amount_str or not date:
            messagebox.showerror("Error", "Title, Amount, and Date are required!")
            return

        try:
            amount = float(amount_str)
            print(f"Converted amount to: {amount}")
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number!")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
            print("Date is valid")
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format!")
            return

        try:
            # Insert expense
            self.cursor.execute("""
            INSERT INTO expenses (user_id, title, amount, category, date)
            VALUES (?, ?, ?, ?, ?)
            """, (self.current_user_id, title, amount, category, date))

            # Update balance (subtract expense amount)
            self.cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, self.current_user_id))

            self.conn.commit()
            print("Expense inserted successfully!")
            messagebox.showinfo("Success", f"Expense added! ${amount:.2f} deducted from balance.")
            self.clear_fields()
            self.refresh_expenses()
            self.refresh_finance()
        except Exception as e:
            print(f"Error adding expense: {e}")
            messagebox.showerror("Error", f"Failed to add expense: {e}")

    def update_expense(self):
        """
        Modify an existing expense record and adjust balance accordingly.
        
        Calculates the difference between old and new amount and
        updates the balance to reflect the change.
        """
        print("Update button clicked!")
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to update!")
            return

        item = self.tree.item(selected[0])
        expense_id = item["values"][0]
        old_amount = float(item["values"][2].replace("$", ""))

        title = self.title_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        date = self.date_entry.get().strip()

        if not title or not amount_str or not date:
            messagebox.showerror("Error", "Title, Amount, and Date are required!")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number!")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format!")
            return

        try:
            # Update expense record
            self.cursor.execute("""
            UPDATE expenses
            SET title = ?, amount = ?, category = ?, date = ?
            WHERE id = ? AND user_id = ?
            """, (title, amount, category, date, expense_id, self.current_user_id))

            # Adjust balance for the difference
            amount_diff = amount - old_amount
            self.cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount_diff, self.current_user_id))

            self.conn.commit()
            messagebox.showinfo("Success", "Expense updated!")
            self.clear_fields()
            self.refresh_expenses()
            self.refresh_finance()
        except Exception as e:
            print(f"Error updating expense: {e}")
            messagebox.showerror("Error", f"Failed to update expense: {e}")

    def delete_expense(self):
        """
        Remove an expense from the database and add its amount back to balance.
        
        Asks for confirmation before deleting to avoid mistakes.
        """
        print("Delete button clicked!")
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete!")
            return

        item = self.tree.item(selected[0])
        expense_id = item["values"][0]
        amount = float(item["values"][2].replace("$", ""))

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?"):
            try:
                self.cursor.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, self.current_user_id))
                self.cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, self.current_user_id))
                self.conn.commit()
                messagebox.showinfo("Success", f"Expense deleted! ${amount:.2f} returned to balance.")
                self.clear_fields()
                self.refresh_expenses()
                self.refresh_finance()
            except Exception as e:
                print(f"Error deleting expense: {e}")
                messagebox.showerror("Error", f"Failed to delete expense: {e}")

    def clear_fields(self):
        """
        Reset all input fields to empty and set date to today.
        
        Makes it easy to start entering a new expense.
        """
        self.title_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def refresh_expenses(self):
        """
        Reload all expenses from the database and update the table.
        
        Gets all expenses for the current user ordered by date (newest first).
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            self.cursor.execute("SELECT id, title, amount, category, date FROM expenses WHERE user_id = ? ORDER BY date DESC", (self.current_user_id,))
            rows = self.cursor.fetchall()
            print(f"Fetched {len(rows)} expenses for user {self.current_user_id}")

            for row in rows:
                self.tree.insert("", tk.END, values=(row[0], row[1], f"{row[2]:.2f}", row[3], row[4]))

            self.update_stats()
        except Exception as e:
            print(f"Error refreshing expenses: {e}")

    def filter_by_date(self):
        """
        Show only expenses within a specific date range.
        
        Validates date format and fetches matching records.
        """
        start_date = self.filter_start.get().strip()
        end_date = self.filter_end.get().strip()

        if not start_date or not end_date:
            messagebox.showerror("Error", "Please enter both start and end dates!")
            return

        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Dates must be in YYYY-MM-DD format!")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            self.cursor.execute("""
            SELECT id, title, amount, category, date FROM expenses
            WHERE user_id = ? AND date BETWEEN ? AND ?
            ORDER BY date DESC
            """, (self.current_user_id, start_date, end_date))
            rows = self.cursor.fetchall()

            if not rows:
                messagebox.showinfo("Info", "No expenses found in this date range!")

            for row in rows:
                self.tree.insert("", tk.END, values=(row[0], row[1], f"{row[2]:.2f}", row[3], row[4]))
        except Exception as e:
            print(f"Error filtering expenses: {e}")
            messagebox.showerror("Error", f"Failed to filter expenses: {e}")

    def update_stats(self):
        """
        Calculate and display total and average spending.
        
        Uses SQL aggregate functions (SUM, AVG) for efficiency.
        """
        try:
            self.cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (self.current_user_id,))
            total = self.cursor.fetchone()[0] or 0.0

            self.cursor.execute("SELECT AVG(amount) FROM expenses WHERE user_id = ?", (self.current_user_id,))
            average = self.cursor.fetchone()[0] or 0.0

            self.total_label.config(text=f"Total Spent: ${total:.2f}")
            self.average_label.config(text=f"Average Spent: ${average:.2f}")
        except Exception as e:
            print(f"Error updating stats: {e}")
    def on_select(self, event):
        """
        Handle expense selection from the table.
        
        Fills input fields with selected expense's details for easy editing.
        """
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item["values"]

            self.clear_fields()
            self.title_entry.insert(0, values[1])
            self.amount_entry.insert(0, values[2])
            self.category_entry.insert(0, values[3] if values[3] else "")
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, values[4])

    def __del__(self):
        """
        Clean up database connection when app closes.
        
        Always good practice to close connections properly!
        """
        try:
            self.conn.close()
        except:
            pass


def main():
    """
    Entry point for the application.
    
    Creates the Tkinter window and initializes the Expense Tracker.
    """
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
