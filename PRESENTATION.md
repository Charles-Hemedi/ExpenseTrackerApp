# 📊 Expense Tracker - Presentation Guide
*By Charles Hemedi | CSE 310*

---

## 🎬 Presentation Outline (Timed for ~4-5 Minutes)

---

### Slide 1: Title Slide (0:00 - 0:30)
**What to say**:
"Hi everyone! My name is Charles Hemedi, and today I'm going to show you my Expense Tracker - a complete SQL relational database application built with Python and SQLite."

**What to show**:
- Project folder
- README.md file
- Application running

---

### Slide 2: Project Overview (0:30 - 1:00)
**What to say**:
"The Expense Tracker is a full-featured application that lets users manage their personal finances easily and expenses. It includes everything from user authentication to real-time financial tracking!"

**Key Features to mention**:
- User login/registration with password hashing
- Full CRUD operations for expenses
- Income and balance tracking
- Real-time statistics
- Date filtering

---

### Slide 3: Demo - Registration & Login (1:00 - 1:30)
**What to do**:
1. Show the login screen
2. Click "Register" and create a new account
3. Then login with your new account
4. Explain what's happening in the database as you do this

**What to say**:
"First, let's create a new user. I'll click Register, enter a username and password. Now, let's login. Great! The password is securely hashed using SHA-256, so we never store plain text passwords."

---

### Slide 4: Demo - Setting Up Income & Adding Expenses (1:30 - 2:15)
**What to do**:
1. Show the "Finances" section at the top
2. Set an initial income (e.g., $2000)
3. Add a few expenses:
   - "Groceries: $150.00
   - "Coffee": $4.50
   - "Gas": $45.00
   - "Dinner": $35.00

**What to say**:
"Now let's set up our income. I'll enter $2000 and click 'Set Income'. Watch how the balance updates automatically as we add expenses!"

---

### Slide 5: Demo - Viewing & Updating Expenses (2:15 - 2:45)
**What to do**:
1. Select one of your expenses from the table
2. Show how the fields populate in the input fields
3. Make a change and click "Update Selected"
4. Show how the balance adjusts

**What to say**:
"See how easy it is to update an expense! Just select it, make your changes, and update!"

---

### Slide 6: Demo - Date Filtering & Stats (2:45 - 3:20)
**What to do**:
1. Show the total spent and average labels
2. Filter expenses by a date range
3. Reset to show all expenses

**What to say**:
"We can also see our total spending and average expense! And we can filter expenses by date range too!"

---

### Slide 7: Demo - Deleting Expenses (3:20 - 3:45)
**What to do**:
1. Select an expense to delete
2. Click "Delete Selected"
3. Confirm the deletion
4. Show how the amount is added back to your balance

**What to say**:
"If we made a mistake, we can delete expenses too - and our balance gets the money back!"

---

### Slide 8: Technical Overview (3:45 - 4:15)
**What to show/say**:
"Let's take a quick look at how it works:
- It's all built in Python, with no external dependencies
- We use SQLite for the database
- Tkinter for the GUI
- Passwords are hashed for security
- We use foreign keys to link users and expenses
- And when we even handle database migrations automatically!"

---

### Slide 9: Wrap Up (4:15 - 4:30)
**What to say**:
"That's my Expense Tracker! Thanks for watching! Any questions?"

---

## 🎯 Live Demo Cheat Sheet

### Expenses to add during demo:
1. "Groceries", 150.00, "Food", "2026-06-01"
2. "Coffee", 4.50, "Food", "2026-06-02"
3. "Gas", 45.00, "Transport", "2026-06-03"
4. "Dinner", 35.00, "Food", "2026-06-04"

---

## 💡 Presentation Tips

1. **Practice makes perfect! Run through the demo a couple of times before presenting
2. **Speak clearly and at a steady pace
3. **Explain what you're doing as you do it
4. **Don't worry if something doesn't go as planned - just keep going!
5. **Remember to mention that the project demonstrates all the requirements are met!

---

## 🎥 Video Recording Tips
- Use a screen recorder like OBS, QuickTime, or even built-in tools
- Record audio separately if possible
- Do a quick test recording first
- Remember to smile! 😊

---

Good luck with your presentation! You've got this! 🚀
