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


def RoutesDailyIncome() -> RoutesList:
    return [
        MessageHandler(filters.TEXT & ~filters.COMMAND, input_daily_income),
        CallbackQueryHandler(daily.daily_start_over, pattern=f"^{Action.BACK}$")
    ]

def RoutesIncome() -> RoutesList:
    return [
        MessageHandler(filters.TEXT & ~filters.COMMAND, input_income),
        CallbackQueryHandler(finance.finance_start_over, pattern=f"^{Action.BACK}$")
    ]

async def input_daily_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        text = update.message.text
    else:
        return -1

    logger.info("Adding income %s", text)

    try:
        account().register_daily_income(float(text))
    except:
        await update.message.reply_text("Неверное значение доходов")

    await daily.daily_start(update, context)
    return Routes.DAILY

async def input_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        text = update.message.text
    else:
        return -1

    logger.info("Adding income %s", text)

    try:
        account().register_income(float(text))
    except:
        await update.message.reply_text("Неверное значение доходов")

    await finance.finance_start(update, context)
    return Routes.FINANCE
