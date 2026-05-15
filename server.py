from flask import Flask, jsonify, render_template_string
from flask_cors import CORS

import random
import pytz

from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

india = pytz.timezone("Asia/Kolkata")

pairs = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "USDCAD",
    "EURJPY",
    "GBPJPY"
]

patterns = [
    "ENGULFING",
    "PIN BAR",
    "HAMMER",
    "SHOOTING STAR",
    "DOJI"
]


def get_session(hour):

    if 5 <= hour < 12:
        return "TOKYO SESSION"

    elif 12 <= hour < 17:
        return "LONDON SESSION"

    else:
        return "NEW YORK SESSION"


@app.route("/")
def home():

    return render_template_string("""

<!DOCTYPE html>

<html>

<head>

<title>HASIBUL SIGNAL BOT</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body{
background:#0f172a;
color:white;
font-family:Arial;
padding:15px;
}

.card{
background:#1e293b;
padding:15px;
border-radius:15px;
margin-bottom:15px;
box-shadow:0 0 10px rgba(0,0,0,0.5);
}

.buy{
color:#00ff95;
font-size:24px;
font-weight:bold;
}

.sell{
color:#ff4d6d;
font-size:24px;
font-weight:bold;
}

.wait{
color:yellow;
font-size:24px;
font-weight:bold;
}

.title{
font-size:28px;
font-weight:bold;
margin-bottom:20px;
text-align:center;
}

.info{
margin-top:8px;
font-size:18px;
}

.clock{
text-align:center;
font-size:20px;
margin-bottom:20px;
color:#38bdf8;
}

</style>

</head>

<body>

<div class="title">
🚀 HASIBUL SIGNAL BOT
</div>

<div class="clock" id="clock"></div>

<div id="signals"></div>

<script>

function updateClock(){

const now = new Date();

document.getElementById("clock").innerHTML =
"🕒 " + now.toLocaleTimeString();

}

setInterval(updateClock,1000);

updateClock();

async function loadSignals(){

let response = await fetch('/signal');

let data = await response.json();

let html = '';

data.forEach(item => {

let signalClass = "wait";

if(item.signal.includes("BUY")){
signalClass = "buy";
}

else if(item.signal.includes("SELL")){
signalClass = "sell";
}

html += `

<div class="card">

<div class="${signalClass}">
${item.signal}
</div>

<div class="info">📊 Pair: ${item.pair}</div>

<div class="info">⏰ Entry: ${item.entry_time}</div>

<div class="info">⌛ Expiry: ${item.expiry}</div>

<div class="info">⏳ Ends: ${item.expiry_time}</div>

<div class="info">🎯 Confidence: ${item.confidence}%</div>

<div class="info">📈 RSI: ${item.rsi}</div>

<div class="info">📉 MACD: ${item.macd}</div>

<div class="info">📊 EMA: ${item.ema_trend}</div>

<div class="info">🕯 Pattern: ${item.pattern}</div>

<div class="info">🌊 Volatility: ${item.volatility}</div>

<div class="info">🌍 Session: ${item.session}</div>

</div>

`;

});

document.getElementById('signals').innerHTML = html;

}

loadSignals();

setInterval(loadSignals,15000);

</script>

</body>

</html>

""")


@app.route("/signal")
def signal():

    now = datetime.now(india)

    data = []

    for pair in pairs:

        rsi = random.randint(35, 80)

        macd = random.choice([
            "BUY",
            "SELL"
        ])

        ema = random.choice([
            "UPTREND",
            "DOWNTREND"
        ])

        if macd == "BUY" and ema == "UPTREND":
            confidence = random.randint(88, 99)

        elif macd == "SELL" and ema == "DOWNTREND":
            confidence = random.randint(88, 99)

        else:
            confidence = random.randint(70, 84)

        volatility = random.choice([
            "LOW",
            "MEDIUM",
            "HIGH"
        ])

        pattern = random.choice(patterns)

        signal = "WAIT SIGNAL"

        if (
            rsi < 45
            and macd == "BUY"
            and ema == "UPTREND"
        ):
            signal = "BUY SIGNAL"

        elif (
            rsi > 60
            and macd == "SELL"
            and ema == "DOWNTREND"
        ):
            signal = "SELL SIGNAL"

        if pattern == "DOJI":
            signal = "WAIT SIGNAL"

        if confidence >= 95 and volatility == "LOW":
            expiry = "5 MIN"
            trade_duration = "5 MIN"

        elif confidence >= 90:
            expiry = "3 MIN"
            trade_duration = "3 MIN"

        else:
            expiry = "1 MIN"
            trade_duration = "1 MIN"

        second = now.second

        next_candle = 60 - second

        trade_time = now.strftime("%I:%M:%S %p")

        entry_time = now.strftime("%I:%M:%S %p")

        if expiry == "1 MIN":

            expiry_time = (
                now + timedelta(minutes=1)
            ).strftime("%I:%M:%S %p")

        elif expiry == "3 MIN":

            expiry_time = (
                now + timedelta(minutes=3)
            ).strftime("%I:%M:%S %p")

        else:

            expiry_time = (
                now + timedelta(minutes=5)
            ).strftime("%I:%M:%S %p")

        signal_data = {

            "pair": pair,
            "session": get_session(now.hour),

            "price": round(
                random.uniform(1.10000, 1.50000),
                5
            ),

            "rsi": rsi,
            "ema_trend": ema,
            "macd": macd,
            "signal": signal,
            "trade_duration": trade_duration,
            "confidence": confidence,
            "volatility": volatility,
            "pattern": pattern,
            "entry_time": entry_time,
            "trade_time": trade_time,
            "expiry": expiry,
            "expiry_time": expiry_time,
            "refresh": "15 SEC"

        }

        data.append(signal_data)

    return jsonify(data)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )