from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
        MessageHandler,
        CallbackQueryHandler,
        ContextTypes,
        filters
)


from log import logger
from data import (
        Routes,
        Action,
        RoutesList,
        account
)

import finance

SETTINGS_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Установить верхний лимит в день", callback_data=Action.SET_MAX_PER_DAY)],
        [InlineKeyboardButton("Установить нижний лимит в день", callback_data=Action.SET_MIN_PER_DAY)],
        [InlineKeyboardButton("Сбросить аккаунт", callback_data=Action.RESET_ACCOUNT)],
        [InlineKeyboardButton("Назад", callback_data=Action.BACK)]
    ]
)

def RoutesSettings() -> RoutesList:
    return [
        CallbackQueryHandler(settings_reset_account, pattern=f"^{Action.RESET_ACCOUNT}$"),
        CallbackQueryHandler(settings_set_max_per_day_prompt, pattern=f"^{Action.SET_MAX_PER_DAY}$"),
        CallbackQueryHandler(settings_set_min_per_day_prompt, pattern=f"^{Action.SET_MIN_PER_DAY}$"),
        CallbackQueryHandler(finance.finance_start_over, pattern=f"^{Action.BACK}$")
    ]

def RoutesSettingsMaxPerDay() -> RoutesList:
    return [
        MessageHandler(filters.TEXT & ~filters.COMMAND, __settings_set_max_per_day),
        CallbackQueryHandler(finance.finance_start_over, pattern=f"^{Action.BACK}$")
    ]

def RoutesSettingsMinPerDay() -> RoutesList:
    return [
        MessageHandler(filters.TEXT & ~filters.COMMAND, __settings_set_min_per_day),
        CallbackQueryHandler(finance.finance_start_over, pattern=f"^{Action.BACK}$")
    ]

async def settings_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message:
        return -1

    text = f"""
Настройки
    """

    await update.message.reply_text(text, reply_markup=SETTINGS_KEYBOARD)
    return Routes.SETTINGS


async def settings_reset_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
        logger.info(f"settings_reset_account -- {query.data}")
    else:
        return -1

    account().reset()

    await finance.finance_start_over(update, context)
    return Routes.FINANCE

async def settings_set_min_per_day_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
        logger.info(f"settings_set_min_per_day_prompt -- {query.data}")
    else:
        return -1
    await query.edit_message_text("Введите значение нижней границы в день")
    return Routes.SETTINGS_MIN_PER_DAY

async def __settings_set_min_per_day(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        text = update.message.text
    else:
        return -1
    logger.info("changing min_per_day")
    try:
        account().set_min_per_day(float(text))
    except:
        await update.message.reply_text("Неверное значение нижней границы в день")
    await settings_start(update, context)
    return Routes.SETTINGS

async def settings_set_max_per_day_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
        logger.info(f"settings_set_max_per_day_prompt -- {query.data}")
    else:
        return -1
    await query.edit_message_text("Введите значение верхней границы в день")
    return Routes.SETTINGS_MAX_PER_DAY

async def __settings_set_max_per_day(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        text = update.message.text
    else:
        return -1
    logger.info("changing max_per_day")
    try:
        account().set_max_per_day(float(text))
    except:
        await update.message.reply_text("Неверное значение верхней границы в день")
    await settings_start(update, context)
    return Routes.SETTINGS
