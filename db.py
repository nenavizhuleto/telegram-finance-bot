from datetime import date
import sqlite3
from typing import List

TRANSACTION_DIRECTION_INCOME = 0
TRANSACTION_DIRECTION_EXPENSE = 1

con = sqlite3.connect("finance.db")


class Transaction:
    def __init__(self, kwargs):
        self.id = kwargs[0]
        self.date = sqlite3.Date.fromisoformat(kwargs[1])
        self.direction = kwargs[2]
        self.value = kwargs[3]


def get_transactions() -> List[Transaction]:
    cur = con.cursor()
    res = cur.execute("SELECT * FROM transactions")
    all = res.fetchall()
    trns = []
    for i in all:
        trns.append(Transaction(i))

    return trns

def get_transactions_by_date(dir: int, dt: date) -> List[Transaction]:
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM transactions WHERE direction = {dir} AND date = '{dt}'")
    all = res.fetchall()
    trns = []
    for i in all:
        trns.append(Transaction(i))

    return trns

def get_income_transactions() -> List[Transaction]:
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM transactions WHERE direction = {TRANSACTION_DIRECTION_INCOME}")
    all = res.fetchall()
    trns = []
    for i in all:
        trns.append(Transaction(i))

    return trns


def get_expense_transactions() -> List[Transaction]:
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM transactions WHERE direction = {TRANSACTION_DIRECTION_EXPENSE}")
    all = res.fetchall()
    trns = []
    for i in all:
        trns.append(Transaction(i))

    return trns


def insert_income_transaction(value: float):
    cur = con.cursor()
    res = cur.execute(f"INSERT INTO transactions (direction, value) VALUES ({TRANSACTION_DIRECTION_INCOME}, {value})")
    return res.lastrowid
    

def insert_expense_transaction(value: float):
    cur = con.cursor()
    res = cur.execute(f"INSERT INTO transactions (direction, value) VALUES ({TRANSACTION_DIRECTION_EXPENSE}, {value})")
    return res.lastrowid

if __name__ == "__main__":
    cur = con.cursor()
    transaction_sql = """
CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL DEFAULT (date('now')),
        direction INT NOT NULL,
        value FLOAT NOT NULL
);
    """

    cur.execute(transaction_sql)


