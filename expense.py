from telegram import Update
from telegram.ext import (
        CallbackQueryHandler,
        MessageHandler,
        ContextTypes,
        filters
)


from log import logger
from data import (
        Action,
        Routes,
        RoutesList,
        account
)


import finance
import daily

def RoutesDailyExpense() -> RoutesList:
    return [
        MessageHandler(filters.TEXT & ~filters.COMMAND, input_daily_expense),
        CallbackQueryHandler(daily.daily_start_over, pattern=f"^{Action.BACK}$")
    ]


def RoutesExpense() -> RoutesList:
    return [
        MessageHandler(filters.TEXT & ~filters.COMMAND, input_expense),
        CallbackQueryHandler(finance.finance_start_over, pattern=f"^{Action.BACK}$")
    ]

async def input_daily_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        text = update.message.text
    else:
        return -1

    logger.info("Adding expense %s", text)

    try:
        account().register_daily_expense(float(text))
    except:
        await update.message.reply_text("Неверное значение расходов")

    await daily.daily_start(update, context)
    return Routes.DAILY

async def input_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        text = update.message.text
    else:
        return -1

    logger.info("Adding expense %s", text)

    try:
        account().register_expense(float(text))
    except:
        await update.message.reply_text("Неверное значение расходов")

    await finance.finance_start(update, context)
    return Routes.FINANCE
