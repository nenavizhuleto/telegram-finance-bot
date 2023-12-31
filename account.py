MAX_PER_DAY = 1000
MIN_PER_DAY = 100
PERIOD = 14

from datetime import date
import db

class Account:
    def __init__(self, income: float, expense: float):
        self.income = income
        self.expense = expense
        self.period = PERIOD
        self.max_per_day = MAX_PER_DAY
        self.min_per_day = MIN_PER_DAY

    def register_income(self, value: float):
        self.income = self.income + value

    def register_expense(self, value: float):
        self.expense = self.expense + value

    def register_daily_income(self, value: float):
        db.insert_income_transaction(value)

    def register_daily_expense(self, value: float):
        db.insert_expense_transaction(value)

    def get_income_by_date(self, dt: date):
        trns = db.get_transactions_by_date(db.TRANSACTION_DIRECTION_INCOME, dt)
        income = 0.0
        for t in trns:
            income = income + t.value

        return income

    def get_expense_by_date(self, dt: date):
        trns = db.get_transactions_by_date(db.TRANSACTION_DIRECTION_EXPENSE, dt)
        expense = 0.0
        for t in trns:
            expense = expense + t.value

        return expense


    def set_max_per_day(self, value: float):
        self.max_per_day = value

    def set_min_per_day(self, value: float):
        self.min_per_day = value

    def set_period(self, value: int):
        self.period = value

    def reset(self):
        self.income = 0
        self.expense = 0

    def info(self) -> str:
        return f"""
        Income/Expense: {self.income}/{self.expense}
        Free: {self.free()}
        Per Day: {self.per_day()}
        Save per day: {self.save_per_day()}
        Day limit: {self.day_limit()}
        Save per period: {self.save_per_period()}
        """

    def free(self):
        return self.income - self.expense

    def per_day(self):
        return self.free() / self.period

    def save_per_day(self):
        per_day = self.per_day()
        if per_day == 0:
            return 0.0

        if per_day >= self.max_per_day:
            return per_day - self.max_per_day
        else:
            save_per_day = per_day % 100
            if save_per_day < self.min_per_day:
                save_per_day = self.min_per_day

            return save_per_day

    def day_limit(self):
        return self.per_day() - self.save_per_day()

    def save_per_period(self):
        return self.save_per_day() * self.period

