# from fastapi import APIRouter

# router=APIRouter(
#     prefix="/",
#     tags=["Calculations"]
# )

def add(num1:int,num2:int) :
    return num1+num2

def sub(num1:int,num2:int):
    return num1-num2

def multi(num1:int,num2:int):
    return num1*num2

def div(num1:int,num2:int):
    return num1/num2

def insufficient(Exception):
    pass

class BankAccount():
    def __init__(self,starting_balance=0):
        self.balance=starting_balance
    def deposite(self,amount):
        self.balance+=amount
    def withdrawl(self,amount):
        if amount>self.balance:
            raise insufficient("Insufficient funds")
        self.balance-=amount
    def interest(self):
        self.balance*=1.1


