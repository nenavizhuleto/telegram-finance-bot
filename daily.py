from datetime import date
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
        CallbackQueryHandler,
        CommandHandler,
        ContextTypes,
)

from log import logger
from data import (
        Action, 
        Routes,
        RoutesList,
        ONLY_BACK_KEYBOARD,
        account
)

DAILY_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Доход", callback_data=Action.ADD_INCOME),
            InlineKeyboardButton("Расход", callback_data=Action.ADD_EXPENSE),
        ]
    ],
)

import settings

def RoutesDaily() -> RoutesList:
    return [
        CallbackQueryHandler(daily_start, pattern=f"^{Action.DAILY}$"),
        CallbackQueryHandler(daily_income, pattern=f"^{Action.ADD_INCOME}$"),
        CallbackQueryHandler(daily_expense, pattern=f"^{Action.ADD_EXPENSE}$"),
        CallbackQueryHandler(daily_start_over, pattern=f"^{Action.BACK}$"),
        CommandHandler("settings", settings.settings_start)
    ]


def get_account_stats() -> str:
    acc = account()
    today = date.today()
    income = acc.get_income_by_date(today)
    expense = acc.get_expense_by_date(today)
    day_limit = round(acc.day_limit(), 2)
    free = day_limit - expense
    return f"""
Доходы/Расходы: {income}/{expense}
Дневной лимит: {day_limit}
Осталось: {free}
    """

# /start
async def daily_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message:
        return -1

    logger.info(f"daily_start -- {update.message.from_user}")
    text = f"""
Статистика на день:
{get_account_stats()}
    """

    await update.message.reply_text(text, reply_markup=DAILY_KEYBOARD)
    return Routes.DAILY

async def daily_start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
        logger.info(f"daily_start_over -- {query.data}")
    else:
        return -1

    text = f"""
Статистика:
{get_account_stats()}
    """

    await query.edit_message_text(text=text, reply_markup=DAILY_KEYBOARD)
    return Routes.DAILY


async def daily_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
        logger.info(f"daily_income -- {query.data}")
    else:
        return -1

    text = f"""
Введите доход
    """

    await query.edit_message_text(text=text, reply_markup=ONLY_BACK_KEYBOARD)
    return Routes.DAILY_INCOME


async def daily_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
        logger.info(f"daily_expense -- {query.data}")
    else:
        return -1

    text = f"""
Введите расход

    """

    await query.edit_message_text(text=text, reply_markup=ONLY_BACK_KEYBOARD)
    return Routes.DAILY_EXPENSE
