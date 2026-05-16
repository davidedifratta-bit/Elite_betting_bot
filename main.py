from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import os
import randomi

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1003961580601
matches = [
    {
        "match": "⚽ Manchester City vs Arsenal",
        "market": "Over 2.5 Goals",
        "odds": "1.85",
        "stake": "8/10",
        "confidence": "82%",
        "priority": "high"
    },
    {
        "match": "⚽ Real Madrid vs Girona",
        "market": "BTTS",
        "odds": "1.74",
        "stake": "7/10",
        "confidence": "79%",
        "priority": "high"
    },
    {
        "match": "⚽ Inter vs Napoli",
        "market": "Over 2.5 Goals",
        "odds": "1.91",
        "stake": "9/10",
        "confidence": "86%",
        "priority": "high"
    },
    {
        "match": "⚽ PSG vs Monaco",
        "market": "BTTS",
        "odds": "1.68",
        "stake": "6/10",
        "confidence": "77%",
        "priority": "high"
    },
    {
        "match": "⚽ Bayern Munich vs Dortmund",
        "market": "Over 3.5 Goals",
        "odds": "2.05",
        "stake": "8/10",
        "confidence": "84%",
        "priority": "high"
    }
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

    high_priority = [m for m in matches if m["priority"] == "high"]
    match = random.choice(high_priority)

    await update.message.reply_text(
        f"🔥 ELITE DAILY PICK 🔥\n\n"
        f"⚽ Match: {match}\n"
        f"🎯 Market: Over 2.5 Goals\n"
        f"📈 Odds: 1.85\n"
        f"💰 Stake: 8/10\n"
        f"📊 Confidence: 82%\n\n"
        f"💎 Elite Betting Lab"
    )

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=
        f"🔥 ELITE DAILY PICK 🔥\n\n"
        f"⚽ Match: {match}\n"
        f"🎯 Market: Over 2.5 Goals\n"
        f"📈 Odds: 1.85\n"
        f"💰 Stake: 8/10\n"
        f"📊 Confidence: 82%\n\n"
        f"💎 Elite Betting Lab"
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

    high_priority = [m for m in matches if m["priority"] == "high"]
    pick = random.choice(high_priority)    

       await update.message.reply_text(
    f"🔥 ELITE DAILY PICK 🔥\n\n"
    f"{pick['match']}\n"
    f"🎯 Market: {pick['market']}\n"
    f"📈 Odds: {pick['odds']}\n"
    f"💰 Stake: {pick['stake']}\n"
    f"📊 Confidence: {pick['confidence']}\n\n"
    f"💎 Elite Betting Lab"
)
elif query.data == "over":

    high_priority = [m for m in matches if m["priority"] == "high"]
    pick = random.choice(high_priority)

    await update.message.reply_text(
        f"🔥 OVER SIGNAL 🔥\n\n"
        f"{pick['match']}\n"
        f"🎯 Market: Over 2.5 Goals\n"
        f"📈 Odds: {pick['odds']}\n"
        f"💰 Stake: {pick['stake']}\n"
        f"📊 Confidence: {pick['confidence']}\n\n"
        f"💎 Elite Betting Lab"
    )

elif query.data == "btts":

    pick = random.choice(matches)

    await update.message.reply_text(
        f"⚽ BTTS SIGNAL ⚽\n\n"
        f"{pick['match']}\n"
        f"🎯 Market: BTTS YES\n"
        f"📈 Odds: {pick['odds']}\n"
        f"💰 Stake: {pick['stake']}\n"
        f"📊 Confidence: {pick['confidence']}\n\n"
        f"💎 Elite Betting Lab"
    )
await context.bot.send_message(
    chat_id=CHANNEL_ID,
    text=
    f"🔥 ELITE DAILY PICK 🔥\n\n"
    f"{pick['match']}\n"
    f"🎯 Market: {pick['market']}\n"
    f"📈 Odds: {pick['odds']}\n"
    f"💰 Stake: {pick['stake']}\n"
    f"📊 Confidence: {pick['confidence']}\n\n"
    f"💎 Elite Betting Lab"
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
