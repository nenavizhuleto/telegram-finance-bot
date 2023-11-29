from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
        CallbackQueryHandler,
        ContextTypes,
)


from log import logger
from data import (
        Action, 
        Routes,
        RoutesList,
)

import finance
import settings

START_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Бюджет", callback_data=Action.FINANCE),
            InlineKeyboardButton("Настройки", callback_data=Action.SETTINGS)
        ],
    ]
)

def RoutesStart() -> RoutesList:
    return [
        CallbackQueryHandler(start_finance, pattern=f"^{Action.FINANCE}$"),
        CallbackQueryHandler(start_settings, pattern=f"^{Action.SETTINGS}$"),
    ]


# Entry point
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message:
        return -1

    logger.info(f"start -- {update.message.from_user}")
    text = f"""
Главный экран
    """

    await update.message.reply_text(text, reply_markup=START_KEYBOARD)
    return Routes.START

async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
        logger.info(f"start_over -- {query.data}")

    else:
        return -1

    text = f"""
Главный экран
    """

    await query.edit_message_text(text=text, reply_markup=START_KEYBOARD)
    return Routes.START

async def start_finance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
        logger.info(f"start_finance -- {query.data}")
    else:
        return -1

    await finance.finance_start_over(update, context)
    return Routes.FINANCE

async def start_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
        logger.info(f"start_settings -- {query.data}")
    else:
        return -1

    await settings.settings_start_over(update, context)
    return Routes.SETTINGS
