from flask import Flask, request
import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from datetime import datetime
import pytz

app = Flask(__name__)

# Currency & OTC only
ALLOWED_SYMBOLS = [
    "EURUSD", "USDJPY", "GBPUSD", "USDCHF", "USDCAD", "AUDUSD", "NZDUSD",
    "EURJPY", "EURGBP", "AUDJPY", "GBPJPY", "CHFJPY", "NZDJPY", "CADJPY",
    "OTC_EURUSD", "OTC_USDJPY", "OTC_GBPUSD", "OTC_USDCAD", "OTC_AUDUSD"
]

@app.route("/")
def home():
    return "15s Heikin Ashi Signal Bot Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        symbol = data.get("symbol", "").upper()
        sma5 = float(data.get("sma5", 0))
        sma10 = float(data.get("sma10", 0))
        rsi = float(data.get("rsi", 50))
        volume = float(data.get("volume", 0))
        avg_volume = float(data.get("avg_volume", 0))

        # Filter by symbol
        if symbol not in ALLOWED_SYMBOLS:
            return {"message": "Invalid symbol"}, 200

        # Volume must be above or below average significantly
        if volume < avg_volume * 0.9:
            volume_condition = "low"
        elif volume > avg_volume * 1.1:
            volume_condition = "high"
        else:
            return {"message": "Volume not significant"}, 200

        # Time in EST
        est = pytz.timezone("US/Eastern")
        entry_time = datetime.now(est).strftime("%I:%M %p EST")

        message = None
        if sma5 > sma10 and rsi < 70 and volume_condition == "high":
            message = f"🟢 BUY signal for {symbol}\n🕒 Entry time: {entry_time}"
        elif sma5 < sma10 and rsi > 30 and volume_condition == "low":
            message = f"🔴 SELL signal for {symbol}\n🕒 Entry time: {entry_time}"

        if message:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": message}
            )

        return {"status": "ok"}, 200
    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)