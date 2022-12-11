from menu import *
from login import *


def choose_account_type(customer_id):
    print(line)
    print("1. Checking account")
    print("2. Saving account")

    account_type = input("What type of account you would like to create: ")
    if account_type  == '1':
        account_type = "Checking"
        balance = 0
        account_id = create_id('account')
        cursor.execute("Insert into account values ({},'{}',{},{},'Active');".format(account_id, balance, account_type, customer_id))
        connect.commit()
        print(f"New checking account was created with ID: {account_id}") 
        clear_and_continue

    elif account_type  == '2':
        account_type = "Saving"
        balance = 0
        account_id = create_id('account')
        cursor.execute("Insert into account values ({},'{}',{},{}, 'Active');".format(account_id, balance, account_type, customer_id))
        connect.commit()
        print(f"New saving account was created with ID: {account_id}")
        clear_and_continue
    else:
        return


def show_accounts(customer_id):
    cursor.execute("SELECT * FROM account WHERE customer_id = '{}' AND status = 'Active';".format(customer_id))
    record = cursor.fetchall()
    lis = []
     
    print("ID------Type--------Balance")
    for row in record:
        lis.append(int(row[0]))
        if row[1] == 'C':
            print(f"{row[0]} Checking {row[2]}")
        elif row[1] == 'S':
            print(f"{row[0]} Saving {row[2]}")
    lis.sort()
    return lis


def check_balance(amount, account_id):
    cursor.execute("Select Balance from account where account_id='{}'".format(account_id))
    record = cursor.fetchone()
    if decimal.Decimal(amount) > decimal.Decimal(record[0]):
        return -1
    return 0


def statement(account_id, start_date, end_date):
    cursor.execute(
        "select transaction_id, type, amount, cursorrbalance_from, cursorrbalance_to, day, from_account, to_account from ((select * from transactions natural join transaction_info where from_account='{}') union (select * from transactions natural join transaction_info where to_account='{}')) as f WHERE f.day BETWEEN date '{}' - interval '1 month' AND '{}' ORDER BY day;".format(account_id, account_id, end_date , start_date ))
    record = cursor.fetchall()
    if len(record) == 0:
        print("There are No transactions")
        return
     
    print("Date---------Type---------Balance before---------Amount---------Balance after")
    for row in record:
        if row[1] == 'Deposit':
            print("{0}{1: <18}{2: <16}{3: <10}{4: <10}".format(row[5], "     Deposit", (decimal.Decimal(row[3]) - decimal.Decimal(row[2])), row[2], row[3]))
             
        elif row[1] == 'Withdrawal':
            print("{0}{1: <18}{2: <16}{3: <10}{4: <10}".format(row[5], "     Withdrawal", (decimal.Decimal(row[3]) + decimal.Decimal(row[2])), row[2], row[3]))
             
        elif row[1] == 'Transfer':
            if row[6] == account_id:
                print("{0}{1: <18}{2: <16}{3: <10}{4: <10}".format(row[5], "     Transfer Out", (decimal.Decimal(row[3]) + decimal.Decimal(row[2])), row[2], row[3]))
                 
            else:
                print("{0}{1: <18}{2: <16}{3: <10}{4: <10}".format(row[5], "     Transfer In", (decimal.Decimal(row[4]) - decimal.Decimal(row[2])), row[2], row[4]))
                 
    ending_balance = record[-1][3]
    print("The balance at the end of the month was: ${}".format(ending_balance))
     

