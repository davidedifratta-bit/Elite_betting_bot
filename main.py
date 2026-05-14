from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context):
    await update.message.reply_text("Bot online!")

async def signal(update: Update, context):
    await update.message.reply_text(
        "🔥 DAILY SIGNAL\n\n"
        "⚽ Milan vs Roma\n"
        "✅ Over 2.5 Goals @1.85\n"
        "Confidence: 82%"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("signal", signal))
print("Bot avviato...")

app.run_polling()

