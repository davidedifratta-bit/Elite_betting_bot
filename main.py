from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, JobQueue 
import os
import random

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

 
vip_matches = [
    {
        "match": "⚽ Manchester City vs Arsenal",
        "market": "Over 2.5 Goals",
        "odds": "1.85",
        "stake": "8/10",
        "confidence": "82%"
    },

    {
        "match": "⚽ Real Madrid vs Barcelona",
        "market": "BTTS YES",
        "odds": "1.72",
        "stake": "9/10",
        "confidence": "87%"
    }
]
used_vip_matches = []

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
        f"⚽ Match: {match['match']}\n"
        f"🎯 Market: {match['market']}\n"
        f"📈 Odds: {match['odds']}\n"
        f"💰 Stake: {match['stake']}\n"
        f"📊 Confidence: {match['confidence']}\n\n"
        f"💎 Elite Betting Lab"
    )

        await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=
        f"⚽ Match: {match['match']}\n"
        f"🎯 Market: {match['market']}\n"
        f"📈 Odds: {match['odds']}\n"
        f"💰 Stake: {match['stake']}\n"
        f"📊 Confidence: {match['confidence']}\n\n"
        f"💎 Elite Betting Lab"
    )
async def over(update: Update, context: ContextTypes.DEFAULT_TYPE):

    match = random.choice(over_signals)
    await update.message.reply_text(
        f"🔥 OVER 2.5 SIGNAL 🔥\n\n"
        f"⚽ {match['match']}\n"
        f"🎯 Market: Over 2.5 Goals\n"
        f"📈 Odds: {match['odds']}\n"
        f"💰 Stake: {match['stake']}\n"
        f"🧠 AI Confidence: {match['confidence']}\n\n"
        f"━━━━━━━━━━━━\n"
        f"💎 Elite Betting Lab"
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
        "💎 VIP ACCESS 💎\n\n"
        "🔥 Daily VIP Signals\n"
        "📈 High Odds Bets\n"
        "🧠 AI Premium Predictions\n"
        "💰 High Confidence Picks\n\n"
        "📩 Contact admin: @TUOUSERNAME\n\n"
        "💎 Elite Betting Lab"
    
       )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "signal":

       high_priority = [m for m in matches if m["priority"] == "high"]
       pick = random.choice(high_priority)    

       await query.message.reply_text(
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

        await query.message.reply_text(
        f"🔥 OVER SIGNAL 🔥\n\n"
        f"{pick['match']}\n"
        f"🎯 Market: Over 2.5 Goals\n"
        f"📈 Odds: {pick['odds']}\n"
        f"💰 Stake: {pick['stake']}\n"
        f"📊 Confidence: {pick['confidence']}\n\n"
        f"💎 Elite Betting Lab"
      )

    elif query.data ==  "btts":

        pick = random.choice(matches)

        await query.message.reply_text(
        f"⚽ BTTS SIGNAL ⚽\n\n"
        f"{pick['match']}\n"
        f"🎯 Market: BTTS YES\n"
        f"📈 Odds: {pick['odds']}\n"
        f"💰 Stake: {pick['stake']}\n"
        f"📊 Confidence: {pick['confidence']}\n\n"
        f"💎 Elite Betting Lab"
        )
        

    elif query.data == "vip":
        available_vip = [m for m in vip_matches if m not in used_vip_matches]

        if not available_vip:
            used_vip_matches.clear()
            available_vip = vip_matches.copy()

        pick = random.choice(available_vip)
        used_vip_matches.append(pick)

            await query.edit_message_text(
            f"💎 VIP SIGNAL 💎\n\n"
            f"{pick['match']}\n"
            f"🎯 Market: {pick['market']}\n"
            f"📈 Odds: {pick['odds']}\n"
            f"💰 Stake: {pick['stake']}\n"
            f"📊 Confidence: {pick['confidence']}\n"
            f"💎 Elite Betting Lab"
            )


    

        

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("signal", signal))
app.add_handler(CommandHandler("over", over))
app.add_handler(CommandHandler("btts", btts))
app.add_handler(CommandHandler("vip", vip))

app.add_handler(CallbackQueryHandler(buttons))

print("Bot avviato!!")


async def auto_signal(context: ContextTypes.DEFAULT_TYPE):

    available_matches = [m for m in matches if m not in used_matches]

    if not available_matches:
        used_matches.clear()
        available_matches = matches

    match = random.choice(available_matches)
    used_matches.append(match)

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=
        f"⚽ Match: {match['match']}\n"
        f"🎯 Market: {match['market']}\n"
        f"📈 Odds: {match['odds']}\n"
        f"📊 Confidence: {match['confidence']}\n\n"
        )
job_queue = app.job_queue

job_queue.run_repeating(auto_signal, interval=3600, first=10)


print("Bot avviato!")

app.run_polling(
    allowed_updates=Update.ALL_TYPES,
    drop_pending_updates=True
)
