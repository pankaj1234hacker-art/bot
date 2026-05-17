import os
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

import random
import time
import threading
import requests

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters
)

# ==================================================
# 🔥 VIP TEHELKA BOT CONFIG 🔥
# ==================================================

TOKEN = "8775211756:AAElPVrt88CwAU16JdUa36m51Y8DOehAZ5M"

CHANNEL_ID = "@TEHELKA_VIP_KING"

REGISTER_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"

CONTACT_USERNAME = "@Next_level_user"

# ==================================================
# GLOBAL VARIABLES
# ==================================================

user_waiting = {}

last_period = "***"

# ==================================================
# 🔥 PREDICTION SYSTEM
# ==================================================

def get_prediction():

    result_type = random.choice([
        "BIG 🔴",
        "SMALL 🔵"
    ])

    if result_type == "BIG 🔴":
        numbers = random.sample(range(5, 10), 2)

    else:
        numbers = random.sample(range(0, 5), 2)

    accuracy = round(random.uniform(91, 99), 1)

    return result_type, numbers, accuracy

# ==================================================
# 🔥 START MESSAGE
# ==================================================

def start(update, context):

    keyboard = [

        [
            InlineKeyboardButton(
                "💎 VIP REGISTER",
                url=REGISTER_LINK
            )
        ],

        [
            InlineKeyboardButton(
                "📢 VIP CHANNEL",
                url="https://t.me/vip_number_shot_official"
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 GET VIP PREDICTION",
                callback_data='vip_pred'
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(

f"""
╔══════════════════╗
 💎 VIP TEHELKA BOT 💎
╚══════════════════╝

🎮 WinGo 1 Minute Game

━━━━━━━━━━━━━━━━━━

🔥 Welcome VIP Member

✅ Join VIP Official Channel
✅ Complete VIP Registration
✅ Get Premium Prediction

━━━━━━━━━━━━━━━━━━

🔥 Registration Link 👇

{REGISTER_LINK}

━━━━━━━━━━━━━━━━━━

📞 For Any Problem Contact Here 👇

{CONTACT_USERNAME}

━━━━━━━━━━━━━━━━━━
""",

        reply_markup=reply_markup
    )

# ==================================================
# 🔥 BUTTON CLICK
# ==================================================

def button(update, context):

    query = update.callback_query

    user_id = query.from_user.id

    if query.data == 'vip_pred':

        user_waiting[user_id] = True

        query.edit_message_text(

"""
╔══════════════════╗
 💎 VIP TEHELKA 💎
╚══════════════════╝

🎮 WinGo 1 Minute Game

━━━━━━━━━━━━━━━━━━

📥 Enter Last 3 Digit

Example: 123

━━━━━━━━━━━━━━━━━━
"""
        )

# ==================================================
# 🔥 USER MESSAGE
# ==================================================

def handle_message(update, context):

    global last_period

    user_id = update.message.from_user.id

    if user_waiting.get(user_id):

        text = update.message.text

        if not text.isdigit() or len(text) != 3:

            update.message.reply_text(
                "❌ Please Enter Valid 3 Digit\n\nExample: 123"
            )

            return

        last_period = text

        update.message.reply_text(

"""
🔍 Analysing Market...

⏳ Fetching VIP Signal...
"""
        )

        time.sleep(2)

        user_waiting[user_id] = False

        result, numbers, accuracy = get_prediction()

        keyboard = [

            [
                InlineKeyboardButton(
                    "🔄 GET PREDICTION AGAIN",
                    callback_data='vip_pred'
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(

f"""
━━━━━━━━━━━━━━━━━━
💎 VIP TEHELKA PREDICTION 💎
━━━━━━━━━━━━━━━━━━

🎮 WinGo 1 Minute Game

🎲 Period Number: {last_period}

━━━━━━━━━━━━━━━━━━

🎯 Prediction:
{result}

🔢 Safe Numbers:
{numbers[0]} • {numbers[1]}

📈 Accuracy: {accuracy}%

━━━━━━━━━━━━━━━━━━

🔥 Registration Link Click Here 🔥

{REGISTER_LINK}

━━━━━━━━━━━━━━━━━━

📞 For Any Problem Contact Here 👇

{CONTACT_USERNAME}

━━━━━━━━━━━━━━━━━━
""",

            reply_markup=reply_markup
        )

# ==================================================
# 🔥 AUTO CHANNEL POST
# ==================================================

def auto_post():

    posted_times = []

    while True:

        current_time = time.strftime("%H:%M")

        # ==================================================
        # 🔥 10 MIN BEFORE ALERT
        # ==================================================

        alert_times = {

            "09:50": "10:00",
            "11:50": "12:00",
            "03:50": "04:00",
            "07:50": "08:00"
        }

        if current_time in alert_times and current_time not in posted_times:

            start_time = alert_times[current_time]

            alert_message = f"""
╔══════════════════╗
 🚨 VIP TEHELKA ALERT 🚨
╚══════════════════╝

🎮 WinGo 1 Minute Game

━━━━━━━━━━━━━━━━━━

🔥 VIP Prediction Session
Is About To Start 🔥

⏰ Starting Time: {start_time}

━━━━━━━━━━━━━━━━━━

⚡ Get Ready VIP Members
🎯 High Accuracy Signal Incoming

━━━━━━━━━━━━━━━━━━

🔥 Registration Link 👇

{REGISTER_LINK}

━━━━━━━━━━━━━━━━━━

📞 Contact Support 👇

{CONTACT_USERNAME}

━━━━━━━━━━━━━━━━━━
"""

            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

            data = {
                "chat_id": CHANNEL_ID,
                "text": alert_message
            }

            requests.post(url, data=data)

            posted_times.append(current_time)

        # ==================================================
        # 🔥 1 MIN BEFORE ALERT
        # ==================================================

        final_alert_times = {

            "09:59": "10:00",
            "11:59": "12:00",
            "03:59": "04:00",
            "07:59": "08:00"
        }

        if current_time in final_alert_times and current_time not in posted_times:

            start_time = final_alert_times[current_time]

            final_message = f"""
╔══════════════════╗
 ⚡ FINAL VIP ALERT ⚡
╚══════════════════╝

🎮 WinGo 1 Minute Game

━━━━━━━━━━━━━━━━━━

🚨 Prediction Starting In 1 Minute 🚨

⏰ Prediction Time: {start_time}

━━━━━━━━━━━━━━━━━━

💎 VIP Signal Ready
🎯 Market Analysis Completed
🔥 Big Winning Session Incoming

━━━━━━━━━━━━━━━━━━

🔥 Registration Link 👇

{REGISTER_LINK}

━━━━━━━━━━━━━━━━━━

📞 Contact Support 👇

{CONTACT_USERNAME}

━━━━━━━━━━━━━━━━━━
"""

            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

            data = {
                "chat_id": CHANNEL_ID,
                "text": final_message
            }

            requests.post(url, data=data)

            posted_times.append(current_time)

        # ==================================================
        # 🔥 PREDICTION TIMES
        # ==================================================

        valid_times = []

        # 10:00 → 10:10
        for i in range(0, 11):
            valid_times.append(f"10:{i:02}")

        # 12:00 → 12:10
        for i in range(0, 11):
            valid_times.append(f"12:{i:02}")

        # 04:00 → 04:10
        for i in range(0, 11):
            valid_times.append(f"04:{i:02}")

        # 08:00 → 08:10
        for i in range(0, 11):
            valid_times.append(f"08:{i:02}")

        if current_time in valid_times and current_time not in posted_times:

            result, numbers, accuracy = get_prediction()

            prediction_message = f"""
━━━━━━━━━━━━━━━━━━
💎 VIP TEHELKA PREDICTION 💎
━━━━━━━━━━━━━━━━━━

🎮 WinGo 1 Minute Game

🎲 Period Number: ***

━━━━━━━━━━━━━━━━━━

🎯 Prediction:
{result}

🔢 Safe Numbers:
{numbers[0]} • {numbers[1]}

📈 Accuracy: {accuracy}%

━━━━━━━━━━━━━━━━━━

🔥 Registration Link 👇

{REGISTER_LINK}

━━━━━━━━━━━━━━━━━━

📞 For Any Problem Contact Here 👇

{CONTACT_USERNAME}

━━━━━━━━━━━━━━━━━━
"""

            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

            data = {
                "chat_id": CHANNEL_ID,
                "text": prediction_message
            }

            requests.post(url, data=data)

            posted_times.append(current_time)

        time.sleep(5)

# ==================================================
# 🔥 MAIN FUNCTION
# ==================================================

def main():

    request_kwargs = {
        'proxy_url': None
    }

    updater = Updater(
        TOKEN,
        request_kwargs=request_kwargs
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CallbackQueryHandler(button))

    dp.add_handler(

        MessageHandler(
            Filters.text & ~Filters.command,
            handle_message
        )
    )

    threading.Thread(
        target=auto_post,
        daemon=True
    ).start()

    updater.start_polling()

    updater.idle()

# ==================================================
# 🔥 RUN BOT
# ==================================================

if __name__ == "__main__":
    main()
