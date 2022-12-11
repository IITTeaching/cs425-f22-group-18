import psycopg2
from menu import *


def create_id(table_name):
    lis = []
    cursor.execute("Select * from {};".format(table_name,))
    record = cursor.fetchall()
    for row in record:
        lis.append(int(row[0]))
    lis.sort()
    if len(lis) == 0:
        return 1
    lis = str(1 + lis[len(lis) - 1])
    return lis


def customer_registration():
    print("Follow the steps below to create new customer account")
    name = input("Enter your name: ")
    password = input("Enter your password (maximum is 10 digits): ")
    branch_id = choose_branch()
    print("Choose an address: ")
    address_id = enter_address()
    customer_id = create_id("customer")      
    cursor.execute("insert into customer values({},'{}','{}','{}','{}');".format(customer_id, name, password, branch_id, address_id))
    connect.commit()
    print(line)
    print(f"Welcome {name}, your customer account was created with {customer_id} id number")
    print(line)
    clear_and_continue
    return customer_id


def employee_registration():
     
    print("Follow the steps below to create new employee account")
    name = input("Enter your name: ")
    print("If you are a manager at the bank, please choose option one")
    print("If you are a teller at the bank, please choose option one")
    print("1. Manager")
    print("2. Teller")
    answer = input("Choose an option: ")
    if answer == '1':
        position = 'Manager'
        salary = 130000.00
    else:
        position = 'Teller'
        salary = 45000.00
    password = input("Enter your password (10 digits max): ")
    SSN = input("Enter your SSN (9 digits): ")
    address_id = enter_address()
    branch_id = choose_branch()
    employee_id = create_id("employee")
    cursor.execute("insert into employee values({},'{}','{}','{}','{}','{}', '{}','{}');".format(employee_id, name, password, SSN, position, salary, branch_id, address_id))
    connect.commit()
    print(line)
    print(f"Welcome {name}, your employee account was created with {employee_id} id number")
    print(line)
    clear_and_continue
    return employee_id


def customer_signin():
    while True:
        print(line)
        print("Follow the steps below to sign into your account")
        print(line)
        customer_id = input("Enter you id: ")
        password = input("Enter your password: ")
        cursor.execute("Select * from customer where customer_id='{}' and password='{}'".format(customer_id ,password))
        record = cursor.fetchone()
        if record:
            return customer_id 
        else:
            print("Wrong id or password, please try again")
            clear_and_continue


def employee_signin():
    while (True):
        print(line)
        print("Follow the steps below to sign into your account")
        print(line)
        employee_id = input("Enter you id: ")
        password = input("Enter your password: ")
        cursor.execute("Select * from employee where employee_id='{}' and password='{}'".format(employee_id , password))
        record = cursor.fetchone()
        if record:
            return employee_id 
        else:
            print("Wrong id or password, please try again")
            clear_and_continue


def choose_branch():
    print("Existing branches at GPGorgon Grace & Go: ")
    cursor.execute("Select branch_id, city, state, zip from branch natural join address;")
    record = cursor.fetchall()
    lis = []
    for row in record:
        lis.append(int(row[0]))
        print(row[0], row[1], row[2], row[3])
    lis.sort()
    while True:
        address_id = input("Choose a branch: ")
        if int(address_id) <= len(lis) and int(address_id) > 0:
            return address_id
        else:
            print("Invalid")


def enter_address():
    print("Now, you need to enter your address")
    while True:
        city = input("Enter your city: ")
        state = input("Enter your state (2 letters): ")
        zip = input("Enter your zipcode (5 digits): ")
        address_id = create_id('address')
        cursor.execute("Insert into address values ({},'{}','{}','{}');".format(address_id, city, state, zip))
        connect.commit()
        print("Thank you, we got your address")
        print(line)
        clear_and_continue
        return address_id