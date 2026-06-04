from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import requests
import json
TOKEN = os.getenv("BOT_TOKEN")

WINS = 0
LOSSES = 0
PUSHES = 0

def load_stats():
    global WINS, LOSSES, PUSHES

    if os.path.exists("stats.json"):
        with open("stats.json", "r") as f:
            data = json.load(f)
            WINS = data.get("wins", 0)
            LOSSES = data.get("losses", 0)
            PUSHES = data.get("pushes", 0)

def save_stats():
    with open("stats.json", "w") as f:
        json.dump({
            "wins": WINS,
            "losses": LOSSES,
            "pushes": PUSHES
        }, f)

def add_win():
    global WINS
    WINS += 1
    save_stats()

def add_loss():
    global LOSSES
    LOSSES += 1
    save_stats()

def add_push():
    global PUSHES
    PUSHES += 1
    save_stats()

FOOTYSTATS_API_KEY = os.getenv("FOOTYSTATS_API_KEY")

print("API KEY:", FOOTYSTATS_API_KEY)

url = f"https://api.football-data-api.com/todays-matches?key={FOOTYSTATS_API_KEY}"

response = requests.get(url)

data = response.json()

if data["success"] and len(data["data"]) > 0:
    best_match = None
    best_score = 0

    for m in data["data"]:
        if int(m.get("o25_potential", 0)) < 60:
            continue

        if int(m.get("btts_potential", 0)) < 50:
            continue

        if float(m.get("team_a_xg_prematch", 0)) < 1.2:
            continue

        if float(m.get("team_b_xg_prematch", 0)) < 1.0:
            continue

        home_xg = float(m.get("team_a_xg_prematch", 0))
        away_xg = float(m.get("team_b_xg_prematch", 0))

        if abs(home_xg - away_xg) > 1.5:
            continue
            
        score = (
            int(m.get("o25_potential", 0))
            + int(m.get("btts_potential", 0))
            + int(float(m.get("team_a_xg_prematch", 0)) * 10)
            + int(float(m.get("team_b_xg_prematch", 0)) * 10)
            + int(float(m.get("corners_potential", 0)) * 5)
)

        if score > best_score:
            print(
                "NEW BEST:",
                m.get("home_name"),
                "vs",
                m.get("away_name"),
                "SCORE:",
                score
)
            best_score = score
            best_match = m

    match = best_match
    if best_score < 100:
        print("NO VALUE TODAY")
        exit()
    if best_score >= 240:
        STAKE = "10/10"
    elif best_score >= 220:
        STAKE = "9/10"
    elif best_score >= 200:
        STAKE = "8/10"
    elif best_score >= 180:
        STAKE = "7/10"
    else:
        STAKE = "6/10"
        
    print("BEST SCORE:", best_score)
    print("BEST MATCH:", match["home_name"], "vs", match["away_name"])

    print("HOME PPG:", match.get("home_ppg"))
    print("AWAY PPG:", match.get("away_ppg"))
    print("O35:", match.get("o35_potential"))
    print("O45:", match.get("o45_potential"))
    print("CORNERS:", match.get("corners_potential"))

    print("HOME:", match["home_name"])
    print("AWAY:", match["away_name"])
    print("BTTS:", match.get("btts_potential"))
    print("OVER 25:", match.get("o25_potential"))
    print("HOME GOALS:", match.get("team_a_xg_prematch"))
    print("AWAY GOALS:", match.get("team_b_xg_prematch"))
    if (
    int(match.get("o25_potential", 0)) >= 75
    and float(match.get("team_a_xg_prematch", 0)) >= 1.5
    and float(match.get("team_b_xg_prematch", 0)) >= 1.0
):
        print("🔥 OVER 2.5 CANDIDATE 🔥")
        print(match["home_name"], "vs", match["away_name"])
        print("Over25:", match.get("o25_potential"))
        print("Home Goals:", match.get("team_a_xg_prematch"))
        print("Away Goals:", match.get("team_b_xg_prematch"))
OVER_SIGNAL = f"""
🔥 OVER 2.5 SIGNAL 🔥

{match["home_name"]} vs {match["away_name"]}

Over25: {match.get("o25_potential")}
Home Goals: {match.get("team_a_xg_prematch")}
Away Goals: {match.get("team_b_xg_prematch")}
"""
STATS_SIGNAL = f"""
📈 ELITE BETTING LAB STATS

✅ Wins: {WINS}
❌ Losses: {LOSSES}
➖ Push: {PUSHES}

📊 Win Rate: {(WINS * 100 // max(1, WINS + LOSSES))}%

🚀 Tracking attivo
"""
BTTS_SIGNAL = f"""
⚽ BTTS SIGNAL ⚽

{match["home_name"]} vs {match["away_name"]}

BTTS: {match.get("btts_potential")}
Home Goals: {match.get("team_a_xg_prematch")}
Away Goals: {match.get("team_b_xg_prematch")}
"""

CORNER_SIGNAL = f"""
📐 CORNER SIGNAL 📐

{match["home_name"]} vs {match["away_name"]}

Corners Potential: {match.get("corners_potential")}
📈 Confidence: HIGH
"""
if (
    int(match.get("o25_potential", 0)) >= 70
    and int(match.get("btts_potential", 0)) >= 60
):
    MARKET_SIGNAL = "🔥 OVER 2.5 + ⚽ BTTS"

elif int(match.get("o25_potential", 0)) >= 70:
    MARKET_SIGNAL = "🔥 OVER 2.5"

elif int(match.get("btts_potential", 0)) >= 60:
    MARKET_SIGNAL = "⚽ BTTS YES"

else:
    MARKET_SIGNAL = "⚠️ NO CLEAR EDGE"
    
if best_score >= 260:
    CONFIDENCE = "99%"
elif best_score >= 240:
    CONFIDENCE = "97%"
elif best_score >= 220:
    CONFIDENCE = "93%"
elif best_score >= 200:
    CONFIDENCE = "88%"
else:
    CONFIDENCE = "82%"
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🎯 Daily Signal", callback_data="signal")],
        [InlineKeyboardButton("🔥 Over 2.5", callback_data="over")],
        [InlineKeyboardButton("⚽ BTTS", callback_data="btts")],
        [InlineKeyboardButton("📐 Corners", callback_data="corners")],
        [InlineKeyboardButton("📈 Stats", callback_data="stats")],
        [InlineKeyboardButton("💎 VIP", callback_data="vip")],
        [InlineKeyboardButton("⚙️ Admin", callback_data="admin")]
    ]
    await update.message.reply_text(
        "🔥 ELITE BETTING LAB 🔥\n\nScegli un'opzione:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    global WINS, LOSSES, PUSHES

    query = update.callback_query
    await query.answer()

    if query.data == "signal":
        await query.edit_message_text(
            f"🎯 DAILY SIGNAL\n\n"
            f"⚽ {match['home_name']} vs {match['away_name']}\n\n"
            f"📊 Smart Score: {best_score}\n"
            f"⚽ BTTS: {match.get('btts_potential')}\n"
            f"🔥 Over25: {match.get('o25_potential')}\n"
            f"🏠 Home xG: {match.get('team_a_xg_prematch')}\n"
            f"✈️ Away xG: {match.get('team_b_xg_prematch')}\n\n"
            f"📈 Confidence: {min(best_score, 99)}%\n"
            f"🎯 Market: {'OVER 2.5' if int(match.get('o25_potential',0)) > int(match.get('btts_potential',0)) else 'BTTS YES'}"
    )

    elif query.data == "over":
        await query.edit_message_text(OVER_SIGNAL)

    elif query.data == "btts":
        await query.edit_message_text(BTTS_SIGNAL)

    elif query.data == "corners":
        await query.edit_message_text(CORNER_SIGNAL)

    elif query.data == "stats":
        await query.edit_message_text(
            f"📈 ELITE BETTING LAB STATS\n\n"
            f"✅ Wins: {WINS}\n"
            f"❌ Losses: {LOSSES}\n"
            f"➖ Push: {PUSHES}\n\n"
            f"📊 Win Rate: {(WINS * 100 // max(1, WINS + LOSSES))}%\n\n"
            f"🚀 Tracking attivo"
    )

    elif query.data == "admin":

        keyboard = [
            [InlineKeyboardButton("✅ Add Win", callback_data="win")],
            [InlineKeyboardButton("❌ Add Loss", callback_data="loss")],
            [InlineKeyboardButton("➖ Add Push", callback_data="push")],
            [InlineKeyboardButton("🔄 Reset Stats", callback_data="reset")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back")]
    ]

        await query.edit_message_text(
            "⚙️ ADMIN PANEL",
            reply_markup=InlineKeyboardMarkup(keyboard)
    )
    elif query.data == "win":
        add_win()
        await query.edit_message_text(
            f"📈 ELITE BETTING LAB STATS\n\n"
            f"✅ Wins: {WINS}\n"
            f"❌ Losses: {LOSSES}\n"
            f"➖ Push: {PUSHES}"
    )
    elif query.data == "loss":
        add_loss()
        await query.edit_message_text(
            f"📈 ELITE BETTING LAB STATS\n\n"
            f"✅ Wins: {WINS}\n"
            f"❌ Losses: {LOSSES}\n"
            f"➖ Push: {PUSHES}"
    )
    elif query.data == "push":
        add_push()
        await query.edit_message_text(
            f"📈 ELITE BETTING LAB STATS\n\n"
            f"✅ Wins: {WINS}\n"
            f"❌ Losses: {LOSSES}\n"
            f"➖ Push: {PUSHES}"
    )
    elif query.data == "reset":
    

        WINS = 0
        LOSSES = 0
        PUSHES = 0

        save_stats()

        await query.edit_message_text("🔄 STATS RESET")
    elif query.data == "back":
        await start(update, context)
    elif query.data == "vip":
        await query.edit_message_text(
            f"💎 VIP SIGNAL 💎\n\n"
            f"⚽ {match['home_name']} vs {match['away_name']}\n\n"
            f"📊 Smart Score: {best_score}\n"
            f"⚽ BTTS: {match.get('btts_potential')}\n"
            f"🔥 Over25: {match.get('o25_potential')}\n"
            f"🏠 Home xG: {match.get('team_a_xg_prematch')}\n"
            f"✈️ Away xG: {match.get('team_b_xg_prematch')}\n\n"
            f"📈 Confidence: 99%\n"
            f"🎯 Market: {'OVER 2.5' if int(match.get('o25_potential',0)) > int(match.get('btts_potential',0)) else 'BTTS YES'}\n"
            f"💰 Stake: {STAKE}"
    )

load_stats()

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot avviato...")

app.run_polling()
