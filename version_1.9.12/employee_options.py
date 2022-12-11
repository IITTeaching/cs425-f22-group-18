from menu import *


def choose_any_account():
    cursor.execute("SELECT account_id,type,balance,name FROM account natural join customer where status='Active';")
    record = cursor.fetchall()
    lis = []     
    print("ID----------Type----------Balance")     
    for row in record:
        lis.append(int(row[0]))
        if row[1] == 'Checking':
            print(f"{row[0]} Checking {row[2]} Customer: {row[3]}")
        elif row[1] == 'Saving':
            print(f"{row[0]} Saving {row[2]} Customer {row[3]}")
    lis.sort()
    return lis


def show_pending(a_id):
    print("Pending Transactions")     
    print("Internal transaction Timeline")     
    cursor.execute("select transaction_id,type,amount,cursorrbalance_from,cursorrbalance_to,day,from_account,to_account from ((select * from transactions natural join transaction_info where from_account='{}') union (select * from transactions natural join transaction_info where to_account='{}')) as f where extract(month from day)=extract(month from cursorrent_timestamp) order by day;".format(a_id,a_id))
    record=cursor.fetchall()
    if len(record)==0:
        print("No transactions have been made this month")     
    print("Date----------Type----------Balance before----------Amount----------Balance after")
    for row in record:
        if row[1] == 'Deposit':
            print("{0}{1: <18}{2: <16}{3: <10}{4: <10}".format(row[5], "     Deposit", (decimal.Decimal(row[3]) - decimal.Decimal(row[2])), row[2], row[3]))
             
        elif row[1] == 'Withdrawal':
            print("{0}{1: <18}{2: <16}{3: <10}{4: <10}".format(row[5], "     Withdrawal", (decimal.Decimal(row[3]) + decimal.Decimal(row[2])), row[2], row[3]))
             
        elif row[1] == 'Transfer':
            if row[6] == a_id:
                print("{0}{1: <18}{2: <16}{3: <10}{4: <10}".format(row[5], "     Transfer Out", (decimal.Decimal(row[3]) + decimal.Decimal(row[2])), row[2], row[3]))
                 
            else:
                print("{0}{1: <18}{2: <16}{3: <10}{4: <10}".format(row[5], "     Transfer In", (decimal.Decimal(row[4]) - decimal.Decimal(row[2])), row[2], row[4]))
                 
    ending_balance = record[-1][3]
    print("The balance at the end of the month is: ${}".format(ending_balance))
     

def branch_total_balances(branch):
    cursor.execute("SELECT SUM(balance) AS total_balance FROM account NATURAL JOIN customer WHERE branch_id = '{}' AND status = 'Active'".format(branch ))
    record = cursor.fetchone()
    total = record[0]
    if total != None:
        print("The total amount of funds at this branch is: ${}".format(total))
        clear_and_continue
    else:
        print("The total amount of money at this branch is: $ 0.00") 
        clear_and_continue


def number_of_transactions(branch, start_date, end_date):
    cursor.execute("SELECT COUNT(transaction_id) AS total_transactions FROM transactions NATURAL JOIN customer WHERE branch_id = '{}' AND day BETWEEN date '{}' - interval '1 month' AND '{}'".format(branch, end_date , start_date))
    record1 = cursor.fetchone()
    cursor.execute("SELECT COUNT(transaction_id) AS total_transactions FROM transactions NATURAL JOIN employee WHERE branch_id = '{}' AND day BETWEEN date '{}' - interval '1 month' AND '{}'".format(branch, end_date , start_date))
    record2 = cursor.fetchone()
    total = record1[0] + record2[0]
    if total > 0:
        print("The total number of transactions made at this branch during the specified month is: {} Transactions".format(total))
        pass
    else:
        print("There has been no transactions made at this branch during the specified month.")
        pass

