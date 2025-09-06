import pytest
from app.calculations import add,sub,multi,div,BankAccount,insufficient

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1,num2,expected",[
         (5,3,8),
         (3,2,5),
         (7,5,12)
])
def test_add(num1,num2,expected):
    print("testing add function")
    assert add(num1,num2) == expected   

def test_sub():
    assert sub(2,3) == -1

def test_multi():
    assert multi(2,3) == 6

def test_div():
    assert div(3,3) == 1

def test_bank_set_initial_amount(bank_account):
    # bank_account=BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    # bank_account= BankAccount()
    assert zero_bank_account.balance == 0

def test_deposite(bank_account):
    # bank_account=BankAccount(50)
    bank_account.deposite(20)
    assert bank_account.balance == 70

def test_withdrawl(bank_account):
    # bank_account=BankAccount(50)
    bank_account.withdrawl(20)
    assert bank_account.balance == 30

def test_interest(bank_account):
    # bank_account=BankAccount(50)
    bank_account.interest()
    assert round(bank_account.balance,6)== 55

@pytest.mark.parametrize("deposited,withdrew,expected",[
         (200,100,100),
         (100,50,50),
         (74000,4000,70000)
])

def test_bank_transaction(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposite(deposited)
    zero_bank_account.withdrawl(withdrew)
    assert zero_bank_account.balance == expected

