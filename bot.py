import os
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

import logging
import pytz

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

from apscheduler.schedulers.background import BackgroundScheduler

# ===================================
# 🔥 CHANGE THESE ONLY 🔥
# ===================================

TOKEN = "8775211756:AAFfKcYQKHJdQ_jyF-XQFvCx5dXfuCHrrLs"

CHANNEL_ID = "@https://t.me/TEHELKA_VIP_KING"

REGISTRATION_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"

CHANNEL_LINK = "hhttps://t.me/TEHELKA_VIP_KING"

SUPPORT_LINK = "@Next_level_user"

# ===================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

user_numbers = {}
verified_users = set()

timezone = pytz.timezone("Asia/Dhaka")

# ===================================
# START
# ===================================

def start(update: Update, context: CallbackContext):

    keyboard = [
        [InlineKeyboardButton("💎 VIP REGISTRATION 💎", url=REGISTRATION_LINK)],
        [InlineKeyboardButton("📢 JOIN VIP CHANNEL 📢", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I HAVE REGISTERED ✅", callback_data="registered")]
    ]

    text = """
╔════💎 VIP TEHELKA 💎════╗

🔥 MOST POWERFUL WINGO 1MIN PREDICTION 🔥

📈 Premium VIP Signals
🎯 Safe Number Access
⚡ Fast Winning Updates
🔐 VIP Member Verification

━━━━━━━━━━━━━━━━

🚨 COMPLETE REGISTRATION FIRST 🚨
"""

    update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ===================================
# BUTTON
# ===================================

def button(update: Update, context: CallbackContext):

    query = update.callback_query
    query.answer()

    if query.data == "registered":

        context.user_data["waiting_uid"] = True

        query.message.reply_text(
            """
🔐 VIP VERIFICATION REQUIRED 🔐

📌 Send Your Game UID Number

━━━━━━━━━━━━━━━━

⚡ After Verification
VIP Prediction Access Will Be Activated
"""
        )

    elif query.data == "prediction":

        query.message.reply_text(
            "📩 Send Any 3 Digit Number"
        )

# ===================================
# MESSAGE
# ===================================

def handle_message(update: Update, context: CallbackContext):

    user_id = update.message.from_user.id
    text = update.message.text.strip()

    # UID VERIFY
    if context.user_data.get("waiting_uid"):

        verified_users.add(user_id)

        context.user_data["waiting_uid"] = False

        keyboard = [
            [InlineKeyboardButton("🎯 GET VIP PREDICTION 🎯", callback_data="prediction")],
            [InlineKeyboardButton("💎 VIP REGISTRATION 💎", url=REGISTRATION_LINK)],
            [InlineKeyboardButton("🚀 JOIN VIP CHANNEL 🚀", url=CHANNEL_LINK)],
            [InlineKeyboardButton("📞 CONTACT SUPPORT 📞", url=SUPPORT_LINK)]
        ]

        update.message.reply_text(
            """
🎉 VIP VERIFICATION SUCCESSFUL 🎉

╔════ ACCESS GRANTED ════╗

🔥 VIP Prediction Activated
🔥 Wingo 1Min Access Enabled
🔥 Premium Support Enabled

━━━━━━━━━━━━━━━━

💎 WELCOME TO VIP TEHELKA 💎
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return

    # SAVE NUMBER
    if user_id in verified_users:

        if text.isdigit() and len(text) == 3:

            user_numbers[user_id] = text

            keyboard = [
                [InlineKeyboardButton("💎 VIP REGISTRATION 💎", url=REGISTRATION_LINK)],
                [InlineKeyboardButton("🚀 JOIN VIP CHANNEL 🚀", url=CHANNEL_LINK)],
                [InlineKeyboardButton("📞 CONTACT SUPPORT 📞", url=SUPPORT_LINK)]
            ]

            update.message.reply_text(
                f"✅ VIP Number Saved: {text}",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        else:

            update.message.reply_text(
                "❌ Send Only 3 Digit Number Example: 395"
            )

# ===================================
# SEND PREDICTION
# ===================================

def send_prediction(bot):

    if not user_numbers:
        return

    latest_number = list(user_numbers.values())[-1]

    formatted = " • ".join(latest_number)

    keyboard = [
        [InlineKeyboardButton("💎 VIP REGISTRATION 💎", url=REGISTRATION_LINK)],
        [InlineKeyboardButton("🚀 JOIN VIP CHANNEL 🚀", url=CHANNEL_LINK)],
        [InlineKeyboardButton("📞 CONTACT SUPPORT 📞", url=SUPPORT_LINK)]
    ]

    text = f"""
╔════💎 VIP TEHELKA 💎════╗

🕒 PERIOD: ***
🎯 SAFE NUMBER: {formatted}

📈 ACCURACY: 95.87%

━━━━━━━━━━━━━━━━

🔥 WINGO 1MIN GAME 🔥
"""

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ===================================
# ALERTS
# ===================================

def send_10min_alert(bot):

    text = """
🚨 ATTENTION VIP MEMBERS 🚨

🔥 BIG WINGO 1MIN PREDICTION
WILL START IN 10 MINUTES 🔥

⚡ Stay Ready
⚡ Don’t Miss The Entry

━━━━━━━━━━━━━━━━

💎 VIP TEHELKA 💎
"""

    bot.send_message(chat_id=CHANNEL_ID, text=text)

def send_1min_alert(bot):

    text = """
⏰ FINAL ALERT ⏰

🔥 VIP WINGO 1MIN PREDICTION
STARTING IN 1 MINUTE 🔥

📌 Get Ready For Entry
📌 Prediction About To Drop

━━━━━━━━━━━━━━━━

💎 VIP TEHELKA 💎
"""

    bot.send_message(chat_id=CHANNEL_ID, text=text)

# ===================================
# MAIN
# ===================================

def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    scheduler = BackgroundScheduler(timezone=timezone)

    # ==========================
    # 10 MIN ALERTS
    # ==========================

    scheduler.add_job(
        lambda: send_10min_alert(updater.bot),
        'cron',
        hour=9,
        minute=50,
        timezone=timezone
    )

    scheduler.add_job(
        lambda: send_10min_alert(updater.bot),
        'cron',
        hour=11,
        minute=50,
        timezone=timezone
    )

    scheduler.add_job(
        lambda: send_10min_alert(updater.bot),
        'cron',
        hour=15,
        minute=50,
        timezone=timezone
    )

    scheduler.add_job(
        lambda: send_10min_alert(updater.bot),
        'cron',
        hour=19,
        minute=50,
        timezone=timezone
    )

    # ==========================
    # 1 MIN ALERTS
    # ==========================

    scheduler.add_job(
        lambda: send_1min_alert(updater.bot),
        'cron',
        hour=9,
        minute=59,
        timezone=timezone
    )

    scheduler.add_job(
        lambda: send_1min_alert(updater.bot),
        'cron',
        hour=11,
        minute=59,
        timezone=timezone
    )

    scheduler.add_job(
        lambda: send_1min_alert(updater.bot),
        'cron',
        hour=15,
        minute=59,
        timezone=timezone
    )

    scheduler.add_job(
        lambda: send_1min_alert(updater.bot),
        'cron',
        hour=19,
        minute=59,
        timezone=timezone
    )

    # ==========================
    # AUTO POSTS
    # ==========================

    for minute in range(0, 11):

        scheduler.add_job(
            lambda: send_prediction(updater.bot),
            'cron',
            hour=10,
            minute=minute,
            timezone=timezone
        )

        scheduler.add_job(
            lambda: send_prediction(updater.bot),
            'cron',
            hour=12,
            minute=minute,
            timezone=timezone
        )

        scheduler.add_job(
            lambda: send_prediction(updater.bot),
            'cron',
            hour=16,
            minute=minute,
            timezone=timezone
        )

        scheduler.add_job(
            lambda: send_prediction(updater.bot),
            'cron',
            hour=20,
            minute=minute,
            timezone=timezone
        )
        def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    scheduler = BackgroundScheduler(timezone=timezone)

    scheduler.start()

    print("🔥 VIP TEHELKA BOT STARTED 🔥")

    updater.start_polling(drop_pending_updates=True)

    updater.idle()


if __name__ == "__main__":
    main()
