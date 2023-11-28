import logging
from utils import iota
import finance

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, Update
from telegram.ext import (
        Application,
        CallbackQueryHandler,
        CommandHandler,
        ContextTypes,
        ConversationHandler,
        MessageHandler,
        filters
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Callback data
ADD_INCOME, ADD_EXPENSE, BACK = range(3)

from dotenv import load_dotenv

load_dotenv()
import os
TOKEN = os.getenv("TOKEN")




# Routes
class Routes:
    START = iota.next()
    INCOME = iota.next()
    EXPENSE = iota.next()
    END = iota.next()

account = finance.Account(0, 0)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.from_user:
        user = update.message.from_user
        logger.info("User %s started conversation", user.first_name)
    else:
        logger.info("Unknown user started conversation")
        return -1

    keyboard = [
        [
            InlineKeyboardButton("Add Income", callback_data=str(ADD_INCOME)),
            InlineKeyboardButton("Add Expense", callback_data=str(ADD_EXPENSE)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Welcome\nStats: {account.info()}", reply_markup=reply_markup)

    return Routes.START

async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
    else:
        return -1

    keyboard = [
        [
            InlineKeyboardButton("Add Income", callback_data=str(ADD_INCOME)),
            InlineKeyboardButton("Add Expense", callback_data=str(ADD_EXPENSE)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"Welcome\nStats: {account.info()}", reply_markup=reply_markup)

    return Routes.START

async def add_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
    else:
        return -1

    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(BACK))
        ]
    ]

    await query.edit_message_text(
        text="Adding income", reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return Routes.INCOME


async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
    else:
        return -1

    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(BACK))
        ]
    ]

    await query.edit_message_text(
        text="Adding expense", reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return Routes.EXPENSE


async def input_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        text = update.message.text
    else:
        return -1

    logger.info("Adding income %s", text)

    try:
        account.register_income(float(text))
    except:
        await update.message.reply_text("Invalid income value")

    await start(update, context)
    return Routes.START


async def input_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        text = update.message.text
    else:
        return -1

    logger.info("Adding expense %s", text)

    try:
        account.register_expense(float(text))
    except:
        await update.message.reply_text("Invalid expense value")

    await start(update, context)
    return Routes.START



def main() -> None:
    app = Application.builder().token(TOKEN).build()

    handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                Routes.START: [
                    CallbackQueryHandler(add_income, pattern=f"^{ADD_INCOME}$"),
                    CallbackQueryHandler(add_expense, pattern=f"^{ADD_EXPENSE}$"),
                    CallbackQueryHandler(start_over, pattern=f"^{BACK}$")
                ],
                Routes.INCOME: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, input_income),
                    CallbackQueryHandler(start_over, pattern=f"^{BACK}$")
                ],
                Routes.EXPENSE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, input_expense),
                    CallbackQueryHandler(start_over, pattern=f"^{BACK}$")
                ],
            },
            fallbacks=[
                CommandHandler("start", start)
            ]
    )

    app.add_handler(handler)


    app.run_polling(allowed_updates=Update.ALL_TYPES)
    

if __name__ == "__main__":
    main()
