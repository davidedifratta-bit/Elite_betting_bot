from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import random

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot online!")


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


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("signal", signal))

print("Bot avviato...")

app.run_polling()
