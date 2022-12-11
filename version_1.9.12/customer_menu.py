import decimal
from decimal import Decimal
from menu import *
from customer_options import *
from transactions import *


def customer(customer_id):
    while True:
        cursor.execute("Select name from customer where customer_id='{}'".format(customer_id))
        record = cursor.fetchone()
        print(line)
        print("Welcome", record[0])
        print("Choose what you would like to do")
        print("1. Create account")
        print("2. Deposit money into an account")
        print("3. Withdraw money from an account")
        print("4. Transfer money between accounts")
        print("5. Transfer to a different bank")
        print("6. Show your account types")
        print("7. Show your transactions")
        print("8. Delete account")
        print("9. log out")
         
        choose=input("Enter your option: ")

        if choose == '1':
            print("Account Type: ")
            choose_account_type(customer_id)

        elif choose == '2':
            lis = show_accounts(customer_id)
            while True:
                account_id = input("Which account you would like to deposit to: ")
                if int(account_id) in lis:
                    if decimal.Decimal(amount) < 0:
                        print("Amount that is less than or equal to 0 cannot be deposited")
                        clear_and_continue
                        break
                    description = input("Enter description: ")
                    deposit(account_id, amount, description, customer_id)
                    break
                else:
                    print("Account with that id does not exist")
                    break

        elif choose == '3':
            lis = show_accounts(customer_id)
            while True:
                account_id = input("Which account you would like to withdraw from: ")
                if int(account_id ) in lis:
                     
                    amount = input("Enter withdrawal amount: ")
                     
                    if decimal.Decimal(amount) > 0 and check_balance(amount,account_id) == -1:
                        print("Amount that is more than account balance cannot be withdrawn")
                        clear_and_continue
                        break
                    description = input("Enter description: ")
                    withdraw(account_id, amount, description, customer_id)
                    break
                else:
                    print("Account with that id does not exist")
                    break
            pass

        elif choose == '4':
            print("Money transfer: ")
            print("1. Transfer money between accounts you own")
            print("2. Transfer money to someone else")
             
            transfer_type = input("Choose an option: ")
            if transfer_type == "1":
                while True:
                    lis = show_accounts(customer_id)
                    from_account = input("Which account you would like to trasfer money from: ")
                    lis1 = show_accounts(customer_id)
                    to_account = input("Which account you would like to trasfer money to: ")
                    if int(from_account) in lis and int(to_account) in lis1:
                         
                        amount = input("Choose transfer amount: ")
                         
                        if check_balance(amount, from_account):
                            print("Amount that is more than account balance cannot be withdrawn")
                            clear_and_continue
                            break
                        description = input("Enter description: ")
                        local_transfer(from_account, to_account, amount, description, customer_id)
                        break
                    else:
                        print("Account with that id does not exist ")
                        break

                pass
            elif transfer_type == '2':
                while True:
                    lis = show_accounts(customer_id)
                    from_account = input("Which account you would like to trasfer money from: ")
                    cursor.execute("SELECT * FROM account;")
                    record = cursor.fetchall()
                    lis1 = []
                    for row in record:
                        lis1.append(int(row[0]))
                    lis1.sort()
                    to_account = input("Which account you would like to trasfer money to: ")
                    if int(from_account) in lis and int(to_account) in lis1:
                         
                        amount = input("Choose transfer amount: ")
                         
                        if (check_balance(amount, from_account)):
                            print("Amount that is more than account balance cannot be withdrawn")
                            clear_and_continue
                            break
                        description = input("Enter description: ")
                        local_transfer(from_account, to_account, amount, description, customer_id)
                        break
                    else:
                        print("Account with that id does not exist ")
                        break

                pass

        elif choose == '5':
            cursor.execute("SELECT * FROM account WHERE customer_id = '{}';".format(customer_id))
            record = cursor.fetchall()
            lis = show_accounts(customer_id)

            while True:
                from_account = input("Which account you would like to trasfer money from: ")

                if int(from_account ) in lis:
                    bank = input("Enter bank you want to transfer money to: ")
                    account_number = input("Enter the account number (12 Digits): ")
                    routing_number = input("Enter the routing number (9 Digits): ")
                    amount = input("Enter transfer amount: ")
                     
                    if check_balance(amount, from_account):
                        print("Amount that is more than account balance cannot be withdrawn")
                        clear_and_continue
                        break
                    description = input("Enter description: ")
                    external_transfer(from_account, amount, description, bank, account_number, routing_number, customer_id)
                    break
                else:
                    print("Account with that id does not exist")
                    break

            pass

        elif choose == '6':
            show_accounts(customer_id)
            clear_and_continue
            pass

        elif choose == '7':
            print("Transactions: ")
            print("Accounts: ")
            show_accounts(customer_id)
             
            account = input("Enter the ID of the account you want to view transactions for: ")
            year = input("Enter a year (4 digit number): ")
            month = input("Enter a month (2 digit Number): ")
            start_date = "{}-{}-01".format(year, month)
            end_date = "{}-{}-02".format(year, month)

            statement(account, start_date, end_date)
            clear_and_continue
            pass

        elif choose == '8':
            print("Delete Account:")
            lis = show_accounts(customer_id)
             
            account_to_delete = input("Enter ID of the account you want to close: ")
            cursor.execute("Select Balance from account where account_id='{}'".format(account_to_delete))
            record = cursor.fetchone()
            balance = record[0]
            if int(account_to_delete ) in lis and decimal.Decimal(balance) == 0:
                cursor.execute("UPDATE account SET Status='{}' WHERE account_id='{}'".format('Closed', account_to_delete))
                connect.commit() 
                print("Account was deleted")
                clear_and_continue
                pass
            else:
                print("Account's balance is greater than 0 and it cannot be deleted")
                clear_and_continue
                pass

        elif choose == '9':
            print("You have been signed out")
            clear_and_continue
            return

        else:
            print("Choose a valid option")
            break