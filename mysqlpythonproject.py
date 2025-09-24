import mysql.connector
import getpass

# ====== Database Connection ======
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  
        database="bank_system"
    )

# ====== USER FUNCTIONS ======
def register_user():
    name = input("Enter your name: ")
    pin = getpass.getpass("Set your PIN: ")
    acc_type = input("Enter account type (Savings/Current): ")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, pin, account_type, balance) VALUES (%s, %s, %s, %s)",
                (name, pin, acc_type, 0.0))
    conn.commit()
    print("Account created successfully!")
    conn.close()

def user_login():
    acc_no = input("Enter account number: ")
    pin = getpass.getpass("Enter PIN: ")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE account_no=%s AND pin=%s", (acc_no, pin))
    user = cur.fetchone()
    conn.close()

    if user:
        print("Login successful!")
        user_menu(acc_no)
    else:
        print("Invalid account number or PIN.")

def view_account(acc_no):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE account_no=%s", (acc_no,))
    data = cur.fetchone()
    conn.close()
    print("\n--- Account Details ---")
    print(f"Account No: {data[0]}\nName: {data[1]}\nType: {data[3]}\nBalance: {data[4]}")

def debit_amount(acc_no):
    amount = float(input("Enter amount to debit: "))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE account_no=%s", (acc_no,))
    balance = cur.fetchone()[0]

    if balance >= amount:
        cur.execute("UPDATE users SET balance = balance - %s WHERE account_no=%s", (amount, acc_no))
        cur.execute("INSERT INTO transactions (account_no, txn_type, amount) VALUES (%s, %s, %s)",
                    (acc_no, "Debit", amount))
        conn.commit()
        print("Amount debited successfully.")
    else:
        print("Insufficient funds.")
    conn.close()

def credit_amount(acc_no):
    amount = float(input("Enter amount to credit: "))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance = balance + %s WHERE account_no=%s", (amount, acc_no))
    cur.execute("INSERT INTO transactions (account_no, txn_type, amount) VALUES (%s, %s, %s)",
                (acc_no, "Credit", amount))
    conn.commit()
    print("Amount credited successfully.")
    conn.close()

def change_pin(acc_no):
    new_pin = getpass.getpass("Enter new PIN: ")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET pin=%s WHERE account_no=%s", (new_pin, acc_no))
    conn.commit()
    print("PIN changed successfully.")
    conn.close()

# ====== ADMIN FUNCTIONS ======
def admin_login():
    username = input("Enter admin username: ")
    password = getpass.getpass("Enter admin password: ")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
    admin = cur.fetchone()
    conn.close()

    if admin:
        print("Admin login successful!")
        admin_menu()
    else:
        print("Invalid admin credentials.")

def view_all_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    for row in cur.fetchall():
        print(row)
    conn.close()

def view_user_details():
    acc_no = input("Enter account number: ")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE account_no=%s", (acc_no,))
    print(cur.fetchone())
    conn.close()

def view_user_transactions():
    acc_no = input("Enter account number: ")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions WHERE account_no=%s", (acc_no,))
    for row in cur.fetchall():
        print(row)
    conn.close()

def view_transactions_by_day():
    date = input("Enter date (YYYY-MM-DD): ")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions WHERE DATE(txn_date)=%s", (date,))
    for row in cur.fetchall():
        print(row)
    conn.close()

# ====== USER MENU ======
def user_menu(acc_no):
    while True:
        print("\n--- User Menu ---")
        print("1. View Account")
        print("2. Debit Amount")
        print("3. Credit Amount")
        print("4. Change PIN")
        print("5. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            view_account(acc_no)
        elif choice == "2":
            debit_amount(acc_no)
        elif choice == "3":
            credit_amount(acc_no)
        elif choice == "4":
            change_pin(acc_no)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. View All Users")
        print("2. View User Details")
        print("3. View User Transactions")
        print("4. View Transactions by Day")
        print("5. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            view_all_users()
        elif choice == "2":
            view_user_details()
        elif choice == "3":
            view_user_transactions()
        elif choice == "4":
            view_transactions_by_day()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

# ====== MAIN MENU ======
def main():
    while True:
        print("\n--- Bank Management System ---")
        print("1. Register User")
        print("2. User Login")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            user_login()
        elif choice == "3":
            admin_login()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
