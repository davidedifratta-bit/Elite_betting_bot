from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import requests
import json
print("VERSIONE TEST 12345")
from datetime import datetime
TOKEN = os.getenv("BOT_TOKEN")

HISTORY = []

def load_history():
    global HISTORY

    if os.path.exists("history.json"):
        with open("history.json", "r") as f:
            HISTORY = json.load(f)
            
WINS = 0
LOSSES = 0
PUSHES = 0
PROFIT = 0

def load_stats():
    global WINS, LOSSES, PUSHES, PROFIT

    if os.path.exists("stats.json"):
        with open("stats.json", "r") as f:
            data = json.load(f)
            WINS = data.get("wins", 0)
            LOSSES = data.get("losses", 0)
            PUSHES = data.get("pushes", 0)
            PROFIT = data.get("profit", 0)

def save_stats():
    with open("stats.json", "w") as f:
        json.dump({
            "wins": WINS,
            "losses": LOSSES,
            "pushes": PUSHES,
            "profit": PROFIT
        }, f)
def save_history():
    with open("history.json", "w") as f:
        json.dump(HISTORY, f)
def add_win():
    global WINS, PROFIT
    WINS += 1
    PROFIT += 1

    HISTORY.append("WIN")
    
    save_stats()
    save_history()

def add_loss():
    global LOSSES, PROFIT
    LOSSES += 1
    PROFIT -= 1

    HISTORY.append("LOSS")
    
    save_stats()
    save_history()

def add_push():
    global PUSHES
    PUSHES += 1

    HISTORY.append("PUSH")
    
    save_stats()
    save_history()
FOOTYSTATS_API_KEY = os.getenv("FOOTYSTATS_API_KEY")

print("Bot avviato...")

url = f"https://api.football-data-api.com/todays-matches?key={FOOTYSTATS_API_KEY}"

response = requests.get(url)

data = response.json()
print("MATCHES FOUND:", len(data["data"]))

if data["success"] and len(data["data"]) > 0:
    best_match = None
    best_score = 0
    score = 0

    for m in data["data"]:
        print(m.get("home_name"), "vs", m.get("away_name"))
        print("BTTS:", m.get("btts_potential"),
              "O25:", m.get("o25_potential"),
              "HXG:", m.get("team_a_xg_prematch"),
              "AXG:", m.get("team_b_xg_prematch"),
              "ODDS:", m.get("odds_ft_over25"))
          
        
        over25_odds = float(m.get("odds_ft_over25", 0) or 0)
        print(
            "ODDS RAW:",
            m.get("home_name"),
            "vs",
            m.get("away_name"),
            "VALUE=",
            repr(m.get("odds_ft_over25"))
)

        print(
            "ODDS FLOAT:",
            over25_odds
)
        print("FILTRO QUOTA =", over25_odds)

        if over25_odds < 1.70:
            print("STOP QUOTA BASSA")
            continue

        if over25_odds > 1.90:
            print("STOP QUOTA ALTA")
            continue
        if int(m.get("o25_potential", 0)) < 45:
            print("STOP O25")
            continue

        if int(m.get("btts_potential", 0)) < 45:
            print("STOP BTTS")
            continue

        if float(m.get("team_a_xg_prematch", 0)) < 1.2:
            print("STOP HOME XG")
            continue

        if float(m.get("team_b_xg_prematch", 0)) < 1.0:
            print("STOP AWAY XG")
            continue

        home_xg = float(m.get("team_a_xg_prematch", 0))
        away_xg = float(m.get("team_b_xg_prematch", 0))
        print(
            "CHECK:",
            m.get("home_name"),
            "vs",
            m.get("away_name"),
            "DIFF:",
            abs(home_xg - away_xg)
)
        market_odds = over25_odds

        if abs(home_xg - away_xg) > 1.5:
            print("STOP XG DIFF")
            continue
        if float(m.get("team_b_xg_prematch", 0)) < 0.50:
            print("STOP AWAY XG")
            continue
        print("ARRIVATO ALLO SCORE")
        score = (
            int(m.get("o25_potential", 0))
            + int(m.get("btts_potential", 0))
            + int(float(m.get("team_a_xg_prematch", 0)) * 10)
            + int(float(m.get("team_b_xg_prematch", 0)) * 10)
            + int(float(m.get("corners_potential", 0)))
)
        print("SCORE CALCOLATO:", score)
        if score < 150:
            continue
    
        print(
            "PASSED:",
            m.get("home_name"),
            "vs",
            m.get("away_name"),
            "SCORE:",
            score
)
    if score > best_score:
        print("REAL SCORE:", score, "BEST:", best_score)
        print(
            "NEW BEST:",
            m.get("home_name"),
            "vs",
            m.get("away_name"),
            "SCORE:",
            score
    )
    print("PARTITA ACCETTATA:", over25_odds)
    best_score = score
    best_match = m
    print("NUOVO BEST SALVATO:")
    print(best_match.get("home_name"), "vs", best_match.get("away_name"))
    print("BEST SCORE:", best_score)

match = best_match

if match is None:
    print("NO MATCH FOUND")
    match = {
        "home_name": "Nessuna partita",
        "away_name": "trovata"
        }
if best_score < 100:
    print("NO VALUE TODAY")

    
    
    print("ARRIVATO ALLA FINE")
    print("####################")
    print("FINAL PICK")
    print(match.get("home_name"), "vs", match.get("away_name"))
    print("FINAL SCORE:", best_score)    
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
    int(match.get("o25_potential", 0)) >= 75
    and int(match.get("btts_potential", 0)) >= 75
):
    MARKET_SIGNAL = "🔥 OVER 2.5 + ⚽ BTTS"

elif int(match.get("o25_potential", 0)) >= 75:
    MARKET_SIGNAL = "🔥 OVER 2.5"

elif int(match.get("btts_potential", 0)) >= 75:
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
        [InlineKeyboardButton("📜 History", callback_data="history")],
        [InlineKeyboardButton("💎 VIP", callback_data="vip")],
        [InlineKeyboardButton("⚙️ Admin", callback_data="admin")]
    ]
    await update.message.reply_text(
        "🔥 ELITE BETTING LAB 🔥\n\nScegli un'opzione:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    global WINS, LOSSES, PUSHES, STAKE

    query = update.callback_query
    await query.answer()

    if query.data == "signal":
        
        match_time = datetime.fromtimestamp(
            int(match.get("date_unix", 0))
        ).strftime("%d/%m %H:%M")
        
        await query.edit_message_text(
            f"🎯 DAILY SIGNAL\n\n"
            f"⚽ {match['home_name']} vs {match['away_name']}\n\n"
            f"🕒 Kick Off: {match_time}\n\n"
            f"📊 Smart Score: {best_score}\n"
            f"⚽ BTTS: {match.get('btts_potential')}\n"
            f"🔥 Over25: {match.get('o25_potential')}\n"
            f"🏠 Home xG: {match.get('team_a_xg_prematch')}\n"
            f"✈️ Away xG: {match.get('team_b_xg_prematch')}\n\n"
            f"📈 Confidence: {min(best_score, 99)}%\n"
            f"🎯 Market: {'OVER 2.5' if int(match.get('o25_potential',0)) > int(match.get('btts_potential',0)) else 'BTTS YES'}"
            f"💸 Quota: {market_odds}\n"
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
            f"💰 Profit: {PROFIT}U\n\n"
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
        
    elif query.data == "history":

        if len(HISTORY) == 0:
            await query.edit_message_text(
                "📜 HISTORY\n\nNessun risultato salvato."
            )

        else:
            text = "📜 LAST RESULTS\n\n"

            for result in HISTORY[-10:]:
                text += f"{result}\n"

            total = len(HISTORY)

            winrate = round((WINS / (WINS + LOSSES)) * 100, 1) if (WINS + LOSSES) > 0 else 0

            text += f"\n📊 Total Bets: {total}"
            text += f"\n✅ Wins: {WINS}"
            text += f"\n❌ Losses: {LOSSES}"
            text += f"\n➖ Pushes: {PUSHES}"
            text += f"\n📈 Win Rate: {winrate}%"

            await query.edit_message_text(text)
  
    await query.edit_message_text(
        f"VIP\n\n"
        f"Match: {match['home_name']} vs {match['away_name']}\n"
        f"Score: {best_score}\n"
        f"Confidence: {CONFIDENCE}\n"
        f"Stake: {STAKE}"
    )

load_stats()
load_history()




app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot avviato...")
print("VERSIONE TEST 999999")

app.run_polling()
