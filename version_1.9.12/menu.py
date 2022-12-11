import psycopg2
from os import system, name
import decimal
from decimal import Decimal

line = "-----------------------------------------------------------------"
connect = psycopg2.connect(
    host="localhost",
    database="project_demo",
    user="postgres",
    password="RatsMuLu0504!")
cursor=connect.cursor()


def clear_and_continue():
    while True:
        print(line)
        answer = input("Please press (Y/y) to continue").lower()
        if answer  == "y":
            # for windows
            if name == 'nt':
                _ = system('cls')
                break
        else:
            print("Invalid option")
            clear_and_continue
            pass