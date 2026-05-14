from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

import os
import random

TOKEN = os.getenv("BOT_TOKEN")

CHAT_ID = "METTI_QUI_IL_TUO_CHAT_ID"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot online! 🔥")


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    matches = [
        "⚽ Inter vs Milan",
        "⚽ Arsenal vs Chelsea",
        "⚽ Real Madrid vs Barcelona"
    ]

    match = random.choice(matches)

    await update.message.reply_text(
        f"🔥 DAILY SIGNAL\n\n"
        f"{match}\n"
        f"✅ Over 2.5 Goals @1.85\n"
        f"Confidence: 82%"
    )


async def auto_signal(context: ContextTypes.DEFAULT_TYPE):

    matches = [
        "⚽ Inter vs Milan",
        "⚽ Arsenal vs Chelsea",
        "⚽ Real Madrid vs Barcelona"
    ]

    match = random.choice(matches)

    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=
        f"🔥 AUTO SIGNAL\n\n"
        f"{match}\n"
        f"✅ BTTS YES @1.72\n"
        f"Confidence: 79%"
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("signal", signal))

job_queue = app.job_queue
job_queue.run_repeating(auto_signal, interval=86400, first=10)

print("Bot avviato... 🔥")

app.run_polling()
