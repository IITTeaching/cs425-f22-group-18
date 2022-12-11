from menu import *
from customer_options import *
from employee_options import *
from transactions import *
from login import *


def employee(employee_id):
    cursor.execute("Select name,position from employee where employee_id='{}'".format(employee_id))
    rec = cursor.fetchone()
    manager = False
    if rec[1] == "Manager" :
        manager = True
    while True:
        print(line)
        print("Welcome",rec[0],"  Position:",rec[1])
        print("Choose from the options below to manage or create accounts")
        print("1. Deposit money ")
        print("2. Withdraw money")
        print("3. Transfer money between accounts at this bank")
        print("4. Transfer money to different bank")

        if manager == True:
            print("5. View statement for an account")
            print("6. View pending transactions for an account")
            print("7. View analytics")
            print("8. Apply overdraft fees if balance is below 0")
        print("9. Log out")
        print(line)
        choose = input("Choose which action you would like to perform: ")

        if choose == '1':
            lis=choose_any_account()
            while True:
                account_id = input("Enter an account id: ")
                if int(account_id ) in lis:
                    amount = input("Enter deposit amount: ")
                     
                    if decimal.Decimal(amount ) < 0:
                        print("Amount that is less than or equal to 0 cannot be deposited")
                        clear_and_continue
                        break
                    description = input("Enter description: ")
                    deposit(account_id, amount, description, employee_id)
                    break
                else:
                    print("Account with that id does not exist")
                    clear_and_continue
                    break

        elif choose == '2':
            lis = choose_any_account()
            while True:
                account_id = input("Which account you would like to withdraw from: ")
                if int(account_id) in lis:
                    amount = input("Enter withdrawal amount: ")
                     
                    if decimal.Decimal(amount) > 0 and check_balance(amount, account_id) == -1:
                        print("Amount that is more than account balance cannot be withdrawn")
                        clear_and_continue
                        break
                    description = input("Enter description: ")
                    withdraw(account_id, amount, description, employee_id)
                    break
                else:
                    print("Account with that id does not exist")
                    break

        elif choose  == '3':
            while True:
                lis = choose_any_account()
                from_account = input("Choose the id of the account you want to transfer the money from: ")
                lis2 = choose_any_account()
                to_account = input("Choose the id of the account you want to transfer the money to: ")
                if int(from_account ) in lis and int(to_account ) in lis2:
                     
                    amount = input("Please choose transfer amount: ")
                     
                    if decimal.Decimal(amount ) >0 and check_balance(amount, from_account):
                        print("Amount to be withdrawn greater than account balance")
                        clear_and_continue
                        break

                    description = input("Please write a short description: ")
                    local_transfer(from_account, to_account, amount, description, employee_id)
                    break
                else:
                    print("Account with that id does not exist")
                    break

        elif choose  == '4':
            lis = choose_any_account()
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
                    external_transfer(from_account, amount, description, bank, account_number, routing_number, employee_id)
                    break
                else:
                    print("Account with that id does not exist")
                    break

        elif choose  == '5':
            if manager == False:
                print(line)
                print("Wrong Input")
                print(line)
                clear_and_continue
            else:
                print(line)
                print("Accounts: ")
                lis=choose_any_account()
                clear_and_continue

        elif choose  == '6':
            if manager == False:
                print(line)
                print("Wrong Input")
                print(line)
                clear_and_continue
            else:
                lis = choose_any_account()                 
                id = input("Which account you would like to see pending transactions for: ")
                if int(id) in lis:
                    show_pending(id)
                    clear_and_continue
                else:
                    print("Invalid input")
                    clear_and_continue

        elif choose  == '7':
            if manager == False:                 
                print("Wrong Input")                 
                clear_and_continue
            else:                 
                print("Analytics: ")
                print(" 1. View branch total customers' balances")
                print(" 2. View transaction numbers for each branch for a single month")                 
                option = input("Choose an option: ")
                if option == '1':
                    print("Branch total: ")                     
                    branch = choose_branch()                     
                    branch_total_balances(branch)                     
                    pass
                elif option == '2':                     
                    print("Number of transactions: ")                     
                    branch = choose_branch()                     
                    year = input("Please enter a year (YYYY): ")                     
                    month = input("Please enter a month (MM): ")
                    start_date = "{}-{}-01".format(year, month)
                    end_date = "{}-{}-02".format(year, month)
                    number_of_transactions(branch, start_date, end_date)
                    clear_and_continue
                    pass
                else:
                    print("Invalid option")
                    clear_and_continue
                    pass
                pass

        elif choose =='8':
            if (manager == False):                 
                print("Wrong Input")                 
                clear_and_continue
                continue

            print("Overdraft Fees")
            print("Overdraft fees apply for accounts with balance less than $0")
            clear_and_continue
            print(line)
            cursor.execute(" update account set balance = balance - 10 where customer_id in (select customer_id from customer as c,employee as e where c.branch_id=e.branch_id and e.employee_id='{}') and type='S' and balance<200;".format(employee_id))
            connect.commit()
            print("Overdraft fees were applied")
            clear_and_continue

        elif choose  == '9':
            print("Logging out...")
            clear_and_continue
            break
        
        else:
            print("Wrong Input")
            clear_and_continue


