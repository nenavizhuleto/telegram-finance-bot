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

FINANCE_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Доход", callback_data=Action.ADD_INCOME),
            InlineKeyboardButton("Расход", callback_data=Action.ADD_EXPENSE),
        ]
    ],
)

import settings
import daily

def RoutesFinance() -> RoutesList:
    return [
        CallbackQueryHandler(finance_start, pattern=f"^{Action.FINANCE}$"),
        CallbackQueryHandler(finance_income, pattern=f"^{Action.ADD_INCOME}$"),
        CallbackQueryHandler(finance_expense, pattern=f"^{Action.ADD_EXPENSE}$"),
        CallbackQueryHandler(finance_start_over, pattern=f"^{Action.BACK}$"),
        CommandHandler("settings", settings.settings_start),
        CommandHandler("daily", daily.daily_start)
    ]


def get_account_stats() -> str:
    acc = account()
    return f"""
Доходы/Расходы: {acc.income}/{acc.expense}
Свободные: {acc.free()}
В день: {round(acc.per_day(), 2)}
Накоплений в день: {round(acc.save_per_day(), 2)}
Дневной лимит: {round(acc.day_limit(), 2)}
Накоплений за период ({acc.period} дней): {round(acc.save_per_period(), 2)}
    """

# /start
async def finance_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message:
        return -1

    logger.info(f"finance_start -- {update.message.from_user}")
    text = f"""
Статистика:
{get_account_stats()}
    """

    await update.message.reply_text(text, reply_markup=FINANCE_KEYBOARD)
    return Routes.FINANCE

async def finance_start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
        logger.info(f"finance_start_over -- {query.data}")
    else:
        return -1

    text = f"""
Статистика:
{get_account_stats()}
    """

    await query.edit_message_text(text=text, reply_markup=FINANCE_KEYBOARD)
    return Routes.FINANCE


async def finance_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
        logger.info(f"finance_income -- {query.data}")
    else:
        return -1

    text = f"""
    Введите доход
    """

    #await query.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(keyboard, input_field_placeholder="Сумма"))
    await query.edit_message_text(text=text, reply_markup=ONLY_BACK_KEYBOARD)
    return Routes.FINANCE_INCOME


async def finance_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
        logger.info(f"finance_expense -- {query.data}")
    else:
        return -1

    text = f"""
    Введите расход
    """

    await query.edit_message_text(text=text, reply_markup=ONLY_BACK_KEYBOARD)
    return Routes.FINANCE_EXPENSE
