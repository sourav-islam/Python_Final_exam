import uuid

class User:
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = self.name + str(uuid.uuid4())[:5]
        self.__balance = 0
        self.transactions = []
        self.loan_count = 0
        self.total_loan = 0

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            self.transactions.append(f"D:{amount}")
            print(f"Successfully deposited {amount} TK")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            self.transactions.append(f"W:{amount}")
            print(f"Successfully withdrew {amount} TK")
        else:
            print("Withdrawal amount exceeded.")

    def check_balance(self):
        print(f"Available balance: {self.__balance} TK")
        return self.__balance

    def check_transaction_history(self):
        print("Transaction history:")
        for transaction in self.transactions:
            print(transaction)

    def take_loan(self, loan_amount, loan_feature):
        if loan_feature:
            if self.loan_count < 2:
                self.__balance += loan_amount
                self.transactions.append(f"Loan:{loan_amount}")
                self.loan_count += 1
                self.total_loan += loan_amount
                print(f"Loan of {loan_amount} TK approved.")
            else:
                print("Loan limit exceeded, Cannot take more than 2 loans.")
        else:
            print("Loan feature is currently disabled.")

    def transfer(self, recipient, amount):
        if self.__balance >= amount:
            self.__balance -= amount
            recipient.__balance += amount
            self.transactions.append(f"Trans:{amount} to {recipient.name}")
            recipient.transactions.append(f"Rec:{amount} from {self.name}")
            print(f"Successfully transferred {amount} TK to {recipient.name}.")
        else:
            print("Insufficient balance for transfer.")

class Admin:
    def __init__(self, name,password):
        self.name = name
        self.password = password
        self.users = []
        self.loan_feature = True
    def authenticate(self,admin_name, admin_password):
        return self.name == admin_name and self.password == admin_password
          
    def create_account(self, name, email, address, account_type):
        new_user = User(name, email, address, account_type)
        self.users.append(new_user)
        print(f"Account created for {name}. Account Number: {new_user.account_number}")
        return new_user

    def delete_account(self, account_number):
        for user in self.users:
            if user.account_number == account_number:
                self.users.remove(user)
                print(f"Account {account_number} deleted.")
                return
        print("Account not found.")

    def view_all_accounts(self):
        print("All user accounts:")
        for user in self.users:
            print(f"Name: {user.name}, Email: {user.email}, Account Number: {user.account_number}, Balance: {user._User__balance} TK")

    def check_total_balance(self):
        total_balance = sum(user._User__balance for user in self.users)
        print(f"Total balance available in the bank: {total_balance} TK")
        return total_balance

    def check_total_loans(self):
        total_loans = sum(user.total_loan for user in self.users)
        print(f"Total loan amount: {total_loans} TK")
        return total_loans

    def ONOF_loan_feature(self):
        self.loan_feature = not self.loan_feature
        status = "enabled" if self.loan_feature else "disabled"
        print(f"Loan feature has been {status}.")


def main():
    admin = Admin("admin",1234)

    while True:
        print("\n****** Banking Management System ******")
        print("1. Admin")
        print("2. User Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            admin_name = input("Enter admin name: ")
            admin_password = int(input("Enter admin password: "))

            if admin.authenticate(admin_name, admin_password):
              print("\nAdmin login successful.")
              while True:
                print("\nAdmin Dashboard:")
                print("1. Create a user account")
                print("2. Delete a user account")
                print("3. View all user accounts")
                print("4. Check total available balance of the bank")
                print("5. Check total loan amount")
                print("6. ON/OF loan feature")
                print("7. Exit")

                admin_choice = input("Enter your choice: ")

                if admin_choice == "1":
                    name = input("Enter user name: ")
                    email = input("Enter user email: ")
                    address = input("Enter user address: ")
                    account_type = input("Enter account type (Savings/Current): ")
                    admin.create_account(name, email, address, account_type)

                elif admin_choice == "2":
                    account_number = input("Enter the account number to delete: ")
                    admin.delete_account(account_number)

                elif admin_choice == "3":
                    admin.view_all_accounts()

                elif admin_choice == "4":
                    admin.check_total_balance()

                elif admin_choice == "5":
                    admin.check_total_loans()

                elif admin_choice == "6":
                    admin.ONOF_loan_feature()

                elif admin_choice == "7":
                    print("Exiting admin operations.")
                    break

                else:
                    print("Invalid choice.")
            else:
                print("Invalid admin username & password.")
        elif choice == "2":
            email = input("Enter your email: ")
            user = next((user for user in admin.users if user.email == email), None)
             
            if user:
                while True:
                    print("\nUser Dashboard")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Transfer")
                    print("4. Take Loan")
                    print("5. Check Balance")
                    print("6. Transaction History")
                    print("7. Logout")

                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":
                        amount = int(input("Enter amount to deposit: "))
                        user.deposit(amount)

                    elif user_choice == "2":
                        amount = int(input("Enter amount to withdraw: "))
                        user.withdraw(amount)

                    elif user_choice == "3":
                        recipient_email = input("Enter recipient email: ")
                        recipient = next((u for u in admin.users if u.email == recipient_email), None)

                        if recipient:
                            amount = int(input("Enter amount to transfer: "))
                            user.transfer(recipient, amount)
                        else:
                            print("Recipient not found.")

                    elif user_choice == "4":
                        amount = int(input("Enter loan amount: "))
                        user.take_loan(amount, admin.loan_feature)

                    elif user_choice == "5":
                        user.check_balance()

                    elif user_choice == "6":
                        user.check_transaction_history()

                    elif user_choice == "7":
                        print("Logging out.")
                        break

                    else:
                        print("Invalid choice.")

            else:
                print("User not found.")

        elif choice == "3":
            print("Exiting the system")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
