from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import os
import random

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1003961580601
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

    keyboard = [
        [InlineKeyboardButton("🎯 Daily Signal", callback_data="signal")],
        [InlineKeyboardButton("🔥 Over 2.5", callback_data="over")],
        [InlineKeyboardButton("⚽ BTTS", callback_data="btts")],
        [InlineKeyboardButton("💎 VIP", callback_data="vip")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔥 ELITE BETTING LAB 🔥\n\nChoose an option:",
        reply_markup=reply_markup
    )

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    match = random.choice(matches)

    await update.message.reply_text(
        f"🔥 DAILY SIGNAL\n\n"
        f"{match}\n"
        f"✅ Over 2.5 Goals @1.85\n"
        f"Confidence: 82%"
    )
    await context.bot.send_message(
    chat_id=CHANNEL_ID,
    text=
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

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "signal":

        match = random.choice(matches)

        await query.message.reply_text(
            f"🔥 DAILY SIGNAL\n\n"
            f"{match}\n"
            f"✅ Over 2.5 Goals @1.85\n"
            f"Confidence: 82%"
        )

    elif query.data == "over":

        match = random.choice(over_signals)

        await query.message.reply_text(
            f"🔥 OVER SIGNAL\n\n"
            f"{match}\n"
            f"✅ Over 2.5 Goals\n"
            f"Odds: 1.80"
        )

    elif query.data == "btts":

        match = random.choice(btts_signals)

        await query.message.reply_text(
            f"🔥 BTTS SIGNAL\n\n"
            f"{match}\n"
            f"✅ Both Teams To Score\n"
            f"Odds: 1.75"
        )

    elif query.data == "vip":

        await query.message.reply_text(
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

app.add_handler(CallbackQueryHandler(buttons))

print("Bot avviato!!")
from telegram.ext import JobQueue

async def auto_signal(context: ContextTypes.DEFAULT_TYPE):

    match = random.choice(matches)

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=
            f"🔥 DAILY SIGNAL\n\n"
            f"{match}\n"
            f"✅ Over 2.5 Goals @1.85\n"
            f"Confidence: 82%"
    )

job_queue = app.job_queue


app.run_polling()
