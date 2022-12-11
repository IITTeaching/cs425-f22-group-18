import decimal
import time
import psycopg2
from os import system, name
from decimal import Decimal
from login import *
from customer_menu import *
from employee_menu import *


while True:
    line = "-----------------------------------------------------------------"
    # bank_name()
    print(line)
    print("Welcome to GPGorgon Grace & Go application")
    print(line)
    print("Please chooose one of the options below to continue with the app")
    print(line)
    print("If you are a customer please choose the option 1")
    print("If you are an employee please choose the option 2")
    print("1. Customers Tab")
    print("2. Employees Tab")
    answer = input("Please enter your answer: ")
    print(line)
    print("Thank you, now choose what you would like to do - login/register")

    if answer == '1':
        print("1. Customer login")
        print("2. Customer registration")
        print("3. Exit the application")
        answer1=input("Choose an option: ")
        print(line)
        if answer1 == '1':
            customer_id = customer_signin()
            customer(customer_id)
        elif answer1 == '2':
            customer_id = customer_registration()
            customer(customer_id)
        elif answer1 == '3':
            print("Thank you, Goodbye!")
            exit()
        else:
            print("Invalid input!")
            clear_and_continue

    elif answer == '2':
        print("1. Employee login")
        print("2. Empoyee registration")
        print("3. Exit the application")
        answer1=input("Choose an option: ")
        print(line)
        if answer1 == '1':
            id = employee_signin()
            employee(id)
        elif answer1 == '2':
            id = employee_registration()
            employee(id)
        elif answer1 == '3':
            print("Thank you, Goodbye!")
            exit()
        else:
            print("Invalid input!")
            clear_and_continue
    else:
        print("Invalid input!")
        clear_and_continue

conn.close()