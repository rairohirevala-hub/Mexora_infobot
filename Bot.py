
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! 👋\n\n"
        "Mexora Info Bot ready aa.\n\n"
        "Public business info lookup layi /check likho."
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "UPI ID / phone number bhejo.\n\n"
        "Main sirf publicly available business details "
        "check karan layi help kar sakda haan."
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))

    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app.run_polling()


if __name__ == "__main__":
    main()
