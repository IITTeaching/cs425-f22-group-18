import psycopg2
from decimal import Decimal
from menu import * 
from login import *


def deposit(account_id, amount, description, customer_id = 'NULL', employee_id = 'NULL'):
    cursor.execute("SELECT * FROM account WHERE account_id = '{}' AND status = 'Active';".format(account_id))
    record = cursor.fetchone()
    type_of_trans = 'Deposit'
    
    old_amount = record[2]
    new_amount = old_amount + Decimal(amount)

    cursor.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(new_amount, account_id))
    new_transaction(account_id, account_id, amount, description, type_of_trans, customer_id, employee_id, new_amount)
    connect.commit()
    print(f"Amount was deposited to account {account_id}")
    clear_and_continue
    pass


def withdraw(account_id, amount, description, customer_id = 'NULL', employee_id = 'NULL'):
    cursor.execute("SELECT * FROM account WHERE account_id = '{}';".format(account_id))
    record = cursor.fetchone()
    type_of_trans = 'Withdrawal'

    old_amount = record[2]
    new_amount = old_amount - Decimal(amount)

    cursor.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(new_amount, account_id))
    new_transaction(account_id, account_id, amount, description, type_of_trans, customer_id, employee_id, new_amount)
    connect.commit()
    print(f"Amount was withdrawn from account {account_id}")
    clear_and_continue
    pass


def local_transfer(from_account, to_account, amount, description, customer_id = 'NULL', employee_id = 'NULL'):
    cursor.execute("SELECT * FROM account WHERE account_id = '{}';".format(from_account))
    record = cursor.fetchone()
    type_of_trans = 'Transfer'

    from_acc_old_amount = record[2]
    from_acc_new_amount = from_acc_old_amount - Decimal(amount)

    cursor.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(from_acc_new_amount, from_account))
    connect.commit()
    cursor.execute("SELECT * FROM account WHERE account_id = '{}';".format(to_account))
    record2 = cursor.fetchone()
    to_acc_old_amount = record2[2]
    to_acc_new_amount = to_acc_old_amount + Decimal(amount)
    cursor.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(to_acc_new_amount, to_account))
    new_transaction(from_account, to_account, amount, description, type_of_trans, customer_id, employee_id, from_acc_new_amount, to_acc_new_amount)
    connect.commit()
    print(f"Amount was transferred from account {from_account} to account {to_account}")
    clear_and_continue


def external_transfer(from_account, amount, description, bank, account_number, routing_number, customer_id = 'NULL', employee_id = 'NULL'):
    cursor.execute("SELECT * FROM account WHERE account_id = '{}';".format(from_account))
    record = cursor.fetchone()
    type_of_trans = 'External_Transfer'
    
    from_acc_old_amount = record[2]
    from_acc_new_amount = from_acc_old_amount - Decimal(amount)

    cursor.execute("UPDATE account SET balance = {} WHERE account_id = '{}'".format(from_acc_new_amount, from_account))
    new_ext_transfer_transaction(from_account, amount, description, type_of_trans, bank, account_number, routing_number, customer_id, employee_id, from_acc_new_amount)
    connect.commit()
     
    print(f"Amount was transferred from account {from_account} to bank {bank}")
     
    clear_and_continue


def new_transaction(from_account, to_account, amount, description, type_of_trans, customer_id, employee_id, from_cursor_balance, to_cursor_balance='NULL', flag='T'):
    transaction_id = create_id("transactions")
    cursor.execute("Insert into transactions values ('{}','{}',{},'{}','{}','{}',{},{});".format(transaction_id, amount, description, type_of_trans, customer_id, employee_id, from_cursor_balance, to_cursor_balance))
    if flag=='T':
        cursor.execute("Insert into TransactionInformation values('{}','{}','{}');".format(transaction_id, from_account, to_account))
    else:
        pass
    connect.commit()


def new_ext_transfer_transaction(from_account, amount, description, type_of_trans, bank, account_number, routing_number, customer_id, employee_id, cursor_balance):
    transaction_id = create_id("transactions")
    cursor.execute(
        "Insert into transactions values ('{}','{}',{},'{}','{}','{}',{});".format(transaction_id, amount, description, type_of_trans, customer_id, employee_id, cursor_balance))
    cursor.execute("Insert into ExternalInformation values('{}','{}','{}','{}','{}')".format(transaction_id, from_account, bank, account_number, routing_number))
    connect.commit()