
import pymysql

# Establish the database connection
connection = pymysql.connect(
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    db="defaultdb",
    host="bank-db-cse-350-bank-project-db.h.aivencloud.com",
    password="AVNS_0n4SZfpgJZYHapcwgPU",
    port=28782,
    user="avnadmin",
)

def deposit(user_id, amount):
    """
    Adds money to the user's account balance.
    """
    try:
        with connection.cursor() as cursor:
            if amount <= 0:
                return "Deposit amount must be greater than zero."
            
            # Update the user's balance
            sql = "UPDATE accounts SET balance = balance + %s WHERE user_id = %s"
            cursor.execute(sql, (amount, user_id))
            
            # Log the transaction
            sql_log = "INSERT INTO transactions (user_id, transaction_type, amount, timestamp) VALUES (%s, 'deposit', %s, NOW())"
            cursor.execute(sql_log, (user_id, amount))
            
            connection.commit()
            return f"Successfully deposited {amount} to user {user_id}'s account."
    except Exception as e:
        return f"Error: {e}"


def withdraw(user_id, amount):
    """
    Subtracts money from the user's account balance if sufficient funds exist.
    """
    try:
        with connection.cursor() as cursor:
            if amount <= 0:
                return "Withdraw amount must be greater than zero."
            
            # Check current balance
            sql_check = "SELECT balance FROM accounts WHERE user_id = %s"
            cursor.execute(sql_check, (user_id,))
            result = cursor.fetchone()
            
            if not result:
                return "User not found."
            
            if result["balance"] < amount:
                return "Insufficient funds."
            
            # Update the user's balance
            sql = "UPDATE accounts SET balance = balance - %s WHERE user_id = %s"
            cursor.execute(sql, (amount, user_id))
            
            # Log the transaction
            sql_log = "INSERT INTO transactions (user_id, transaction_type, amount, timestamp) VALUES (%s, 'withdraw', %s, NOW())"
            cursor.execute(sql_log, (user_id, amount))
            
            connection.commit()
            return f"Successfully withdrew {amount} from user {user_id}'s account."
    except Exception as e:
        return f"Error: {e}"


def transfer(sender_id, receiver_id, amount):
    """
    Transfers money from one user to another if the sender has sufficient funds.
    """
    try:
        with connection.cursor() as cursor:
            if amount <= 0:
                return "Transfer amount must be greater than zero."
            
            # Check sender's balance
            sql_check_sender = "SELECT balance FROM accounts WHERE user_id = %s"
            cursor.execute(sql_check_sender, (sender_id,))
            sender = cursor.fetchone()
            
            if not sender:
                return "Sender not found."
            
            if sender["balance"] < amount:
                return "Insufficient funds in sender's account."
            
            # Check if receiver exists
            sql_check_receiver = "SELECT balance FROM accounts WHERE user_id = %s"
            cursor.execute(sql_check_receiver, (receiver_id,))
            receiver = cursor.fetchone()
            
            if not receiver:
                return "Receiver not found."
            
            # Perform the transfer
            sql_update_sender = "UPDATE accounts SET balance = balance - %s WHERE user_id = %s"
            cursor.execute(sql_update_sender, (amount, sender_id))
            
            sql_update_receiver = "UPDATE accounts SET balance = balance + %s WHERE user_id = %s"
            cursor.execute(sql_update_receiver, (amount, receiver_id))
            
            # Log the transaction
            sql_log_sender = "INSERT INTO transactions (user_id, transaction_type, amount, timestamp) VALUES (%s, 'transfer_out', %s, NOW())"
            sql_log_receiver = "INSERT INTO transactions (user_id, transaction_type, amount, timestamp) VALUES (%s, 'transfer_in', %s, NOW())"
            cursor.execute(sql_log_sender, (sender_id, amount))
            cursor.execute(sql_log_receiver, (receiver_id, amount))
            
            connection.commit()
            return f"Successfully transferred {amount} from user {sender_id} to user {receiver_id}."
    except Exception as e:
        return f"Error: {e}"

# Close the connection when done (you might do this in a separate cleanup step)
def close_connection():
    connection.close()
