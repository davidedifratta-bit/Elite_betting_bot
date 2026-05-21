from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, JobQueue 
import os
import random
from datetime import datetime
import requests
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1003961580601
FOOTYSTATS_API_KEY = os.getenv("FOOTYSTATS_API_KEY")
used_matches = []
def get_footystats_prediction():

    url = f"https://api.footystats.org/todays-matches?key={FOOTYSTATS_API_KEY}"    

    response = requests.get(url)

    data = response.json()
    print(response.text)
    matches = []

    for match in data:
        print(data)
        league = match.get("competition_name", "")
        match_time = match.get("date_unix", "")
        formatted_time = datetime.fromtimestamp(int(match_time)).strftime("%H:%M")
        
        # top_leagues = [
#     "Premier League",
#     ...
# ]

# if league not in top_leagues:
#     continue    
        home_team = match.get("home_name", "Home")
        formatted_time = datetime.fromtimestamp(int(match_time)).strftime("%H:%M") if match_time else "TBD"
        away_team = match.get("away_name", "Away")

        odds = 1.85

        if odds:
            match_name = f"{home_team} vs {away_team}"

            if match_name in used_matches:
                continue

            used_matches.append(match_name)
            prediction = {
                "match": f"⚽ {home_team} vs {away_team}",
                "league": league,
                "time": formatted_time,
                "market": random.choice([
                "Over 2.5 Goals",
                "BTTS",
                "Under 2.5 Goals"
]),
                "odds": str(odds),
                "stake": "8/10",
                "confidence": f"{random.randint(74, 89)}%",
                "priority": "high"
            }

            matches.append(prediction)

    return matches[:2]
    
matches = get_footystats_prediction()
print(matches) 
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

       if not matches:
           await query.message.reply_text("Nessun match disponibile.")
           return

       pick = random.choice(matches)
        
       
           

       await query.edit_message_text(
           f"🔥 ELITE DAILY PICK 🔥\n\n"
           f"{pick['match']}\n"
           f"🎯 Market: {pick['market']}\n"
           f"📈 Odds: {pick['odds']}\n"
           f"💰 Stake: {pick['stake']}\n"
           f"📊 Confidence: {pick['confidence']}\n\n"
           f"💎 Elite Betting Lab"
       )
    

    elif query.data == "over":
        
        high_priority = [m for m in matches if "OVER" in m["market"].upper()]

        if not high_priority:
            await query.message.reply_text("Nessun match OVER trovato.")
            return

        pick = random.choice(high_priority)

        await query.edit_message_text(
        f"🔥 OVER SIGNAL 🔥\n\n"
        f"{pick['match']}\n"
        f"🎯 Market: Over 2.5 Goals\n"
        f"📈 Odds: {pick['odds']}\n"
        f"💰 Stake: {pick['stake']}\n"
        f"📊 Confidence: {pick['confidence']}\n\n"
        f"💎 Elite Betting Lab"
      )

    elif query.data ==  "btts": 
        
        btts_matches = [m for m in matches if "BTTS" in m["market"].upper()]

        if not btts_matches:
            await query.message.reply_text("Nessun match BTTS trovato.")
            return

        pick = random.choice(btts_matches)
        await query.edit_message_text(
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

     available_matches = matches

     if not available_matches:
         return

     match = random.choice(available_matches)   
    
     used_matches.append(match)

     await context.bot.send_message(
         chat_id=CHANNEL_ID,
        text=
            f"🔥 ELITE BETTING LAB 🔥\n\n"
            f"🏆 League: {match['league']}\n"
            f"⏰ Time: {match['time']}\n"
            f"⚽ Match: {match['match']}\n"
            f"🎯 Market: {match['market']}\n"
            f"📈 Odds: {match['odds']}\n"
            f"📊 Confidence: {match['confidence']}\n\n"
            f"💎 Premium AI Pick"
     )
job_queue = app.job_queue
    

job_queue.run_repeating(auto_signal, interval=60, first=5)


print("Bot avviato!")

app.run_polling(
    allowed_updates=Update.ALL_TYPES,
    drop_pending_updates=True
)
