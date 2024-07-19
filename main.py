from datetime import datetime
from getpass import getpass

OPTIONS = """[1] Show Balance
[2] Deposit
[3] Withdrawal
[4] Print Statement
[5] Quit"""

class Account:
    INITIAL_BALANCE = 1000
    def __init__(self, initial_balance=INITIAL_BALANCE):
        self.initial_balance = initial_balance
        self.deposits = []
        self.withdrawals = []

    @property
    def balance(self):
        return self.initial_balance + sum(self.deposits) - sum(self.withdrawals)

    def deposit(self, amount):
        self.deposits.append(amount)

    def withdraw(self, amount):
        if self.check_overdraft(amount):
            amount += 100
        self.withdrawals.append(amount)
    
    def check_overdraft(self, amount):
        return True if self.balance - amount <= 0 else False

    def statement(self, customer):
        return f"""Date: {datetime.now().strftime('%m/%d/%Y')}

        First National Bank of Python

        My Statement
        
        Customer Name: {customer.first_name} {customer.last_name}

        Inital Balance: {'${:,.2f}'.format(self.initial_balance)}

        Deposits Made: {'No deposits made.' if len(self.deposits) == 0 else ', '.join(['${:,.2f}'.format(x) for x in self.deposits])}

        Total Deposits: {'${:,.2f}'.format(sum(self.deposits))}

        Withdrawals Made: {'No withdrawals made.' if len(self.withdrawals) == 0 else ', '.join(['${:,.2f}'.format(x) for x in self.withdrawals])}

        Total Withdrawals: {'${:,.2f}'.format(sum(self.withdrawals))}

        Ending Balance: {'${:,.2f}'.format(self.balance)}
        """

class Customer:
    def __init__(self, first_name, last_name, username, password, initial_balance=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.account = Account()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def print_statement(self):
        return self.account.statement(self)

customer_database = [
    Customer("John", "Doe", "johndoe63", "password123"),
    Customer("Rachael", "Smith", "rsmith", "1234dogs")
]

def sign_in():
    print("Please input your credentials:")
    username = input('Username: ')
    password = getpass()

    for customer in customer_database:
        if (customer.username == username) & (customer.password == password):
            return customer

    return None

def main():
    attempts = 0

    while attempts < 5:
        user = sign_in()
        if user is None:
            attempts += 1
        elif isinstance(user, Customer):
            print(f"Welcome, {user.full_name}!")
            while True:
                choice = input(f"Please select from the following options:\n\n{OPTIONS}\n\nYour selection: ")
                if choice == '1':
                    print(f"\n\nYour balance is currently: {'${:,.2f}'.format(user.account.balance)}\n\n")
                    pass
                if choice == '2':
                    while True:
                        deposit_amount = input("How much are you depositing? Please enter only numbers and decimals. ")
                        try:
                            deposit_amount = float(deposit_amount)
                            user.account.deposit(deposit_amount)
                            print(f"\n\nThank you. Your balance is now: {'${:,.2f}'.format(user.account.balance)}\n\n")
                        except Exception as e:
                            print("You entered an invalid number.  Try again.")
                            continue
                        break
                if choice == '3':
                    if user.account.balance < 0:
                        print('\n\nWARNING: Your account balance is currently below $0.00.  You will incur an overdraft fee.\n\n')
                    while True:
                        withdraw_amount = input("How much are you withdrawing? Please enter only numbers and decimals. ")
                        try:
                            withdraw_amount = float(withdraw_amount)
                            future_balance = user.account.balance - withdraw_amount
                            if future_balance < 0:
                                print(f"\n\nWARNING: Your account balance will be {'${:,.2f}'.format(future_balance)}.  You will incur an overdraft fee.\n\n")
                                do_continue = input("Do you want to proceed?\n\n[Y]es\n[N]o\n\nYour selection: ")
                                if do_continue.upper().strip() == 'Y':
                                    user.account.withdraw(withdraw_amount)
                                    print(f"\n\nThank you. Your balance is now: {'${:,.2f}'.format(user.account.balance)}\n\n")
                            else:
                                user.account.withdraw(withdraw_amount)
                                print(f"\n\nThank you. Your balance is now: {'${:,.2f}'.format(user.account.balance)}\n\n")
                        except Exception as e:
                            print(e)
                            print("You entered an invalid number.  Try again.")
                            continue
                        break

                if choice == '4':
                    print(user.print_statement())
                if choice == '5':
                    print("Thank you, goodbye!")
                    break
            break

if __name__ == "__main__":
    main()