
import tkinter as tk
from tkinter import messagebox

# Mock database and account management
users = {"user1": {"password": "pass1", "balance": 1000.0, "transactions": []}}
current_user = None

# Functions for backend logic
def login(username, password):
    global current_user
    if username in users and users[username]["password"] == password:
        current_user = username
        return True
    return False

def logout():
    global current_user
    current_user = None

def create_account(username, password):
    if username in users:
        return False
    users[username] = {"password": password, "balance": 0.0, "transactions": []}
    return True

def deposit(amount):
    if current_user:
        users[current_user]["balance"] += amount
        users[current_user]["transactions"].append(f"Deposited: ${amount}")
        return True
    return False

def withdraw(amount):
    if current_user and users[current_user]["balance"] >= amount:
        users[current_user]["balance"] -= amount
        users[current_user]["transactions"].append(f"Withdrew: ${amount}")
        return True
    return False

def balance():
    if current_user:
        return users[current_user]["balance"]
    return None

def send_money(recipient, amount):
    if current_user and recipient in users and users[current_user]["balance"] >= amount:
        users[current_user]["balance"] -= amount
        users[current_user]["transactions"].append(f"Sent ${amount} to {recipient}")
        users[recipient]["balance"] += amount
        users[recipient]["transactions"].append(f"Received ${amount} from {current_user}")
        return True
    return False

def transactions():
    if current_user:
        return users[current_user]["transactions"]
    return None

# GUI Functions
def update_user_label():
    if current_user:
        user_label.config(text=f"Logged in as: {current_user}")
    else:
        user_label.config(text="No user logged in")

def login_gui():
    def submit_login():
        username = username_entry.get()
        password = password_entry.get()
        if login(username, password):
            update_user_label()
            messagebox.showinfo("Success", "Logged in successfully!")
            login_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=submit_login).pack(pady=10)

def create_account_gui():
    def submit_account_creation():
        username = username_entry.get()
        password = password_entry.get()
        if create_account(username, password):
            messagebox.showinfo("Success", "Account created successfully!")
            account_window.destroy()
        else:
            messagebox.showerror("Error", "Username already exists!")

    account_window = tk.Toplevel(root)
    account_window.title("Create Account")
    account_window.geometry("300x200")

    tk.Label(account_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(account_window)
    username_entry.pack(pady=5)

    tk.Label(account_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(account_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(account_window, text="Create", command=submit_account_creation).pack(pady=10)

def logout_gui():
    logout()
    update_user_label()
    messagebox.showinfo("Success", "Logged out successfully!")

def deposit_gui():
    def submit_deposit():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive!")
            if deposit(amount):
                messagebox.showinfo("Success", f"Deposited ${amount} successfully!")
                deposit_window.destroy()
            else:
                raise ValueError("Deposit failed!")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    deposit_window = tk.Toplevel(root)
    deposit_window.title("Deposit")
    deposit_window.geometry("300x150")

    tk.Label(deposit_window, text="Amount to deposit:").pack(pady=5)
    amount_entry = tk.Entry(deposit_window)
    amount_entry.pack(pady=5)
    tk.Button(deposit_window, text="Deposit", command=submit_deposit).pack(pady=10)

def withdraw_gui():
    def submit_withdraw():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive!")
            if withdraw(amount):
                messagebox.showinfo("Success", f"Withdrew ${amount} successfully!")
                withdraw_window.destroy()
            else:
                raise ValueError("Insufficient balance!")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    withdraw_window = tk.Toplevel(root)
    withdraw_window.title("Withdraw")
    withdraw_window.geometry("300x150")

    tk.Label(withdraw_window, text="Amount to withdraw:").pack(pady=5)
    amount_entry = tk.Entry(withdraw_window)
    amount_entry.pack(pady=5)
    tk.Button(withdraw_window, text="Withdraw", command=submit_withdraw).pack(pady=10)

def show_balance_gui():
    user_balance = balance()
    if user_balance is not None:
        messagebox.showinfo("Balance", f"Your current balance is: ${user_balance}")
    else:
        messagebox.showerror("Error", "Failed to retrieve balance!")

def send_money_gui():
    def submit_transfer():
        try:
            recipient = recipient_entry.get()
            amount = float(amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive!")
            if send_money(recipient, amount):
                messagebox.showinfo("Success", f"Sent ${amount} to {recipient} successfully!")
                send_window.destroy()
            else:
                raise ValueError("Transfer failed!")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    send_window = tk.Toplevel(root)
    send_window.title("Send Money")
    send_window.geometry("300x200")

    tk.Label(send_window, text="Recipient:").pack(pady=5)
    recipient_entry = tk.Entry(send_window)
    recipient_entry.pack(pady=5)

    tk.Label(send_window, text="Amount:").pack(pady=5)
    amount_entry = tk.Entry(send_window)
    amount_entry.pack(pady=5)
    tk.Button(send_window, text="Send", command=submit_transfer).pack(pady=10)

def view_transactions_gui():
    transaction_history = transactions()
    if transaction_history:
        transactions_str = "\n".join(transaction_history)
        messagebox.showinfo("Transactions", transactions_str)
    else:
        messagebox.showinfo("Transactions", "No transactions found!")

# Main GUI Setup
def main():
    global root, user_label
    root = tk.Tk()
    root.title("Banking App")
    root.geometry("400x500")

    user_label = tk.Label(root, text="No user logged in", font=("Arial", 12))
    user_label.pack(pady=10)

    tk.Button(root, text="Login", command=login_gui).pack(pady=5)
    tk.Button(root, text="Create Account", command=create_account_gui).pack(pady=5)
    tk.Button(root, text="Logout", command=logout_gui).pack(pady=5)
    tk.Button(root, text="Deposit", command=deposit_gui).pack(pady=5)
    tk.Button(root, text="Withdraw", command=withdraw_gui).pack(pady=5)
    tk.Button(root, text="Show Balance", command=show_balance_gui).pack(pady=5)
    tk.Button(root, text="Send Money", command=send_money_gui).pack(pady=5)
    tk.Button(root, text="View Transactions", command=view_transactions_gui).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit, bg="red", fg="white").pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
