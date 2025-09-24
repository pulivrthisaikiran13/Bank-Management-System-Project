# Bank Management System (Python + MySQL)

A simple command-line banking system built with Python and MySQL.  
Users can manage their accounts, and admins can monitor all users and transactions.

## Features
- **User:**  
  - Register with name, PIN, and account type  
  - Login using account number and PIN  
  - View account details  
  - Debit and credit money  
  - Change PIN  

- **Admin:**  
  - Login with admin credentials  
  - View all users  
  - Check individual user details  
  - View user transactions  
  - Filter transactions by date  

## How to Run
1. Set up a MySQL database named `bank_system` with `users`, `admins`, and `transactions` tables.  
2. Update the database connection details in the script if needed.  
3. Run:
   ```bash
   python mysqlpythonproject.py
