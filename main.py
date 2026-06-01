from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🎯 Daily Signal", callback_data="signal")],
        [InlineKeyboardButton("🔥 Over 2.5", callback_data="over")],
        [InlineKeyboardButton("⚽ BTTS", callback_data="btts")],
        [InlineKeyboardButton("💎 VIP", callback_data="vip")]
    ]

    await update.message.reply_text(
        "🔥 ELITE BETTING LAB 🔥\n\nScegli un'opzione:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "signal":
        await query.edit_message_text(
            "🎯 DAILY SIGNAL\n\n"
            "⚽ Manchester City vs Arsenal\n"
            "🎯 Over 2.5 Goals\n"
            "📈 Odds: 1.85\n"
            "💰 Stake: 8/10\n"
            "📊 Confidence: 82%"
        )

    elif query.data == "over":
        await query.edit_message_text(
            "🔥 OVER 2.5 SIGNAL\n\n"
            "⚽ Liverpool vs Chelsea\n"
            "📈 Odds: 1.90\n"
            "💰 Stake: 7/10\n"
            "📊 Confidence: 80%"
        )

    elif query.data == "btts":
        await query.edit_message_text(
            "⚽ BTTS SIGNAL\n\n"
            "⚽ Real Madrid vs Barcelona\n"
            "📈 Odds: 1.75\n"
            "💰 Stake: 9/10\n"
            "📊 Confidence: 87%"
        )

    elif query.data == "vip":
        await query.edit_message_text(
            "💎 VIP SIGNAL 💎\n\n"
            "⚽ Inter vs Juventus\n"
            "🎯 BTTS YES\n"
            "📈 Odds: 2.05\n"
            "💰 Stake: 10/10\n"
            "📊 Confidence: 91%"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot avviato...")

app.run_polling()
