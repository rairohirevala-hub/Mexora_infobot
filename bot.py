import os
import re
import asyncio
import threading
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)


BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Mexora Info Bot is running")

    def log_message(self, format, *args):
        return


def start_web_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()


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
    if re.fullmatch(r"[0-9]{10}", value):
        await update.message.reply_text(
            "🔎 Public business search hun add kar rahe haan.\n"
            "Private owner details retrieve nahi karda."
        )
        return
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

    threading.Thread(
        target=start_web_server,
        daemon=True
    ).start()

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
