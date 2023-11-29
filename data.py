from typing import Union, List
from utils import iota
from account import Account
from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    Update
)
from telegram.ext import (
        BaseHandler,
        CallbackContext,
)

# Types
RoutesList = List[BaseHandler[Update, CallbackContext]]

__account: Union[None, Account] = None

def account() -> Account:
    global __account
    if not __account:
        __account = Account(0, 0)

    return __account


class Action:
    # Start
    FINANCE = iota.next_char()
    SETTINGS = iota.next_char()
    DAILY = iota.next_char()

    # Settings
    RESET_ACCOUNT = iota.next_char()
    SET_MAX_PER_DAY = iota.next_char()
    SET_MIN_PER_DAY = iota.next_char()

    # Finance
    ADD_INCOME = iota.next_char()
    ADD_EXPENSE = iota.next_char()
    BACK = iota.next_char()

class Routes:
    START = iota.next()

    SETTINGS = iota.next()
    SETTINGS_MAX_PER_DAY = iota.next()
    SETTINGS_MIN_PER_DAY = iota.next()

    FINANCE = iota.next()

    DAILY = iota.next()
    DAILY_INCOME = iota.next()
    DAILY_EXPENSE = iota.next()

    FINANCE_INCOME = iota.next()
    FINANCE_EXPENSE = iota.next()

    END = iota.next()





ONLY_BACK_KEYBOARD = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Назад", callback_data=Action.BACK)
        ]
    ]
)
