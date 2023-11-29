from income import RoutesDailyIncome, RoutesIncome
from expense import RoutesDailyExpense, RoutesExpense
from finance import RoutesFinance, finance_start
from settings import RoutesSettings, RoutesSettingsMaxPerDay, RoutesSettingsMinPerDay
from daily import RoutesDaily

from config import TOKEN
from data import Routes

from telegram import Update
from telegram.ext import (
        Application,
        CommandHandler,
        ConversationHandler,
)

def main() -> None:
    if not TOKEN:
        print("TOKEN not found. Check .env file")
        exit(1)

    app = Application.builder().token(TOKEN).build()

    handler = ConversationHandler(
            entry_points=[CommandHandler("start", finance_start)],
            states={
                Routes.FINANCE: RoutesFinance(),
                Routes.FINANCE_INCOME: RoutesIncome(),
                Routes.FINANCE_EXPENSE: RoutesExpense(),
                Routes.DAILY: RoutesDaily(),
                Routes.DAILY_INCOME: RoutesDailyIncome(),
                Routes.DAILY_EXPENSE: RoutesDailyExpense(),
                Routes.SETTINGS: RoutesSettings(),
                Routes.SETTINGS_MIN_PER_DAY: RoutesSettingsMinPerDay(),
                Routes.SETTINGS_MAX_PER_DAY: RoutesSettingsMaxPerDay(),
            },
            fallbacks=[
                CommandHandler("start", finance_start)
            ]
    )

    app.add_handler(handler)


    app.run_polling(allowed_updates=Update.ALL_TYPES)
    

if __name__ == "__main__":
    main()
