
import os
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    keyboard = [
        [InlineKeyboardButton(
            "Monthly — 30 дней",
            callback_data="plan_30",
        )],
        [InlineKeyboardButton(
            "VIP — 90 дней",
            callback_data="plan_90",
        )],
        [InlineKeyboardButton(
            "Premium — 180 дней",
            callback_data="plan_180",
        )],
    ]

    await update.message.reply_text(
        "Добро пожаловать в ELINA PRIVATE ✨\n\n"
        "Выбери подходящий тариф:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def choose_plan(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    plans = {
        "plan_30": ("Monthly", 30),
        "plan_90": ("VIP", 90),
        "plan_180": ("Premium", 180),
    }

    plan_name, days = plans[query.data]

    await query.message.reply_text(
        f"Ты выбрала тариф {plan_name}.\n"
        f"Срок доступа: {days} дней.\n\n"
        "Скоро здесь появится оформление подписки 💕"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        CallbackQueryHandler(choose_plan, pattern=r"^plan_")
    )

    print("Ellie запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
