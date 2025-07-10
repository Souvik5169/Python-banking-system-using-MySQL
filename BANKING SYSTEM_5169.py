import mysql.connector

# Function to connect to MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='root123',  # Replace with your MySQL password
            database='banking_system'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create a new account
def create_account(name):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (name) VALUES (%s)", (name,))
        conn.commit()
        
        # Retrieve the account ID of the newly created account
        cursor.execute("SELECT account_id FROM accounts WHERE name = %s ORDER BY account_id DESC LIMIT 1", (name,))
        account_id = cursor.fetchone()[0]
        
        print(f"Account for {name} created successfully! Your Account ID: {account_id}")
        conn.close()
        return account_id

# Function to deposit money into an account
def deposit(account_id, amount):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
        account = cursor.fetchone()

        if account:
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, account_id))
            conn.commit()
            print(f"Deposited ${amount} into account {account_id}.")
        else:
            print(f"Account ID {account_id} not found.")
        conn.close()

# Function to withdraw money from an account
def withdraw(account_id, amount):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
        account = cursor.fetchone()

        if account:
            balance = account[0]
            if balance >= amount:
                cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
                conn.commit()
                print(f"Withdrew ${amount} from account {account_id}.")
            else:
                print(f"Insufficient funds. Your balance is ${balance}.")
        else:
            print(f"Account ID {account_id} not found.")
        conn.close()

# Function to check account balance
def check_balance(account_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
        account = cursor.fetchone()

        if account:
            print(f"Account {account_id} balance: ${account[0]}")
        else:
            print(f"Account ID {account_id} not found.")
        conn.close()

# Main function to interact with the system
def main():
    while True:
        print("\n--- Banking System ---")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter account holder's name: ")
            account_id = create_account(name)  # Save the account ID for later use
        
        elif choice == '2':
            account_id = int(input("Enter your account ID: "))
            amount = float(input("Enter amount to deposit: "))
            deposit(account_id, amount)
        
        elif choice == '3':
            account_id = int(input("Enter your account ID: "))
            amount = float(input("Enter amount to withdraw: "))
            withdraw(account_id, amount)
        
        elif choice == '4':
            account_id = int(input("Enter your account ID: "))
            check_balance(account_id)
        
        elif choice == '5':
            print("Exiting the system...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
