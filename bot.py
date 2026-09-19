import os
import re
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)


BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Mexora Info Bot!\n\n"
        "Main public business information te "
        "user-consented verification vich help kar sakda haan.\n\n"
        "Phone number, Gmail ya UPI ID bhejo "
        "format check karan layi.\n\n"
        "⚠️ Private owner details, personal Gmail "
        "ya hidden information retrieve nahi karda."
    )


async def lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Usage:\n/lookup your_phone_or_upi"
        )
        return

    value = " ".join(context.args).strip()

    if len(value) > 200:
        await update.message.reply_text("Input bahut lamba hai.")
        return

    if "@" in value:
        result = "Email/UPI format detected."
    elif re.fullmatch(r"[0-9]{10}", value):
        result = "Phone number format detected."
    else:
        result = "Input received."

    await update.message.reply_text(
        f"✅ {result}\n\n"
        "Eh bot private owner details ya "
        "personal Gmail retrieve nahi karda.\n"
        "Public business verification layi "
        "official sources use karo."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Bot start karo\n"
        "/lookup - Input format check karo\n"
        "/help - Help"
    )


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable missing")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lookup", lookup))
    app.add_handler(CommandHandler("help", help_command))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
