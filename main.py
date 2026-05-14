from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import random

TOKEN = os.getenv("BOT_TOKEN")

matches = [
    "⚽ Milan vs Roma",
    "⚽ Arsenal vs Chelsea",
    "⚽ Real Madrid vs Barcelona",
    "⚽ Inter vs Juventus"
]

over_signals = [
    "⚽ Milan vs Roma",
    "⚽ Arsenal vs Chelsea",
    "⚽ Inter vs Juventus"
]

btts_signals = [
    "⚽ Liverpool vs Tottenham",
    "⚽ PSG vs Monaco",
    "⚽ Napoli vs Atalanta"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot online!")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match = random.choice(matches)

    await update.message.reply_text(
        f"🔥 DAILY SIGNAL\n\n"
        f"{match}\n"
        f"✅ Over 2.5 Goals @1.85\n"
        f"Confidence: 82%"
    )

async def over(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match = random.choice(over_signals)

    await update.message.reply_text(
        f"🔥 OVER SIGNAL\n\n"
        f"{match}\n"
        f"✅ Over 2.5 Goals\n"
        f"Odds: 1.80"
    )

async def btts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match = random.choice(btts_signals)

    await update.message.reply_text(
        f"🔥 BTTS SIGNAL\n\n"
        f"{match}\n"
        f"✅ Both Teams To Score\n"
        f"Odds: 1.75"
    )

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💎 VIP ACCESS\n\n"
        "VIP Signals Daily\n"
        "High Odds Bets\n"
        "Safe Predictions\n\n"
        "Contact admin: @TUOUSERNAME"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("signal", signal))
app.add_handler(CommandHandler("over", over))
app.add_handler(CommandHandler("btts", btts))
app.add_handler(CommandHandler("vip", vip))

print("Bot avviato...")

app.run_polling()
