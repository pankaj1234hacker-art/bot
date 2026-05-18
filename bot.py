import os
import random
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
# TOKEN
# ===================================

TOKEN = "8775211756:AAFWtG1PNM393_nPcAchCNaDuEKIilhjGGg"

# ===================================
# LINKS
# ===================================

CHANNEL_ID = "@TEHELKA_VIP_KING"

REGISTRATION_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"

CHANNEL_LINK = "https://t.me/TEHELKA_VIP_KING"

SUPPORT_LINK = "https://t.me/Next_level_user"

# ===================================
# STICKERS
# ===================================

STICKER_10MIN = "CAACAgUAAxkBAAIBP2oKn8i0a1JqoNAqRLTxvqcwJzoWAAIXEwACvmTQVn4hqlDaxy8AATsE"

STICKER_2MIN = "CAACAgUAAyEFAATloOE5AAICAmoJ1-y3HvygDNQQukQL63uJdoOnAAKFEQACflHJVvhHK40SVtJHOwQ"

STICKER_1MIN = "CAACAgUAAxkBAAIBSWoKopjKbEtd9eRIFwxok8JzHV4FAALSEAACt-6xVytut0bPId8JOwQ"

STICKER_MIDDLE_1 = "CAACAgUAAyEFAATloOE5AAIB9WoJ02vKgrKJ85e-5vvj5CytikTsAAIiEgACUUDJVkSsO8zj-IA5OwQ"

STICKER_MIDDLE_2 = "CAACAgUAAyEFAATloOE5AAIB6GoJ0iO50gAB2ZmmjkaahT3EJ9t7ygACahIAAvYiyVZikUGUoRZynzsE"

STICKER_END_1 = "CAACAgUAAxkBAAIBUWoKo0uIfCGeV5GfZU0Fv_hYOe8HAALYEQACMazJVuD7AUjcPT_gOwQ"

STICKER_END_2 = "CAACAgUAAxkBAAIBU2oKo39yvzCGf62ZmLIMd3cQk2TaAAJ-EwACnQdoV6lN-23qPLHPOwQ"

# ===================================
# SETTINGS
# ===================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

timezone = pytz.timezone("Asia/Kolkata")

verified_users = set()
user_waiting = {}

# ===================================
# START COMMAND
# ===================================

def start(update: Update, context: CallbackContext):

    keyboard = [
        [InlineKeyboardButton("💎 VIP REGISTRATION 💎", url=REGISTRATION_LINK)],
        [InlineKeyboardButton("🚀 JOIN VIP CHANNEL 🚀", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I HAVE REGISTERED ✅", callback_data="registered")]
    ]

    text = """
💎 VIP TEHELKA 💎

🔥 WINGO 1MIN VIP PREDICTION 🔥

✅ High Accuracy Signal
✅ Safe Number Support
✅ Daily VIP Entry

━━━━━━━━━━━━━━━━━━

🚀 COMPLETE REGISTRATION FIRST
"""

    update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ===================================
# BUTTONS
# ===================================

def button(update: Update, context: CallbackContext):

    query = update.callback_query
    query.answer()

    user_id = query.from_user.id

    if query.data == "registered":

        context.user_data["waiting_uid"] = True

        query.message.reply_text(
            """
🔐 VIP VERIFICATION REQUIRED

📩 SEND YOUR GAME UID NUMBER
"""
        )

    elif query.data == "prediction":

        user_waiting[user_id] = True

        query.message.reply_text(
            """
🎯 SEND ANY 3 DIGIT NUMBER

Example: 123
"""
        )

# ===================================
# USER MESSAGE
# ===================================

def handle_message(update: Update, context: CallbackContext):

    user_id = update.message.from_user.id
    text = update.message.text.strip()

    # UID VERIFY
    if context.user_data.get("waiting_uid"):

        verified_users.add(user_id)

        context.user_data["waiting_uid"] = False

        keyboard = [
            [InlineKeyboardButton("🎯 GET PREDICTION 🎯", callback_data="prediction")],
            [InlineKeyboardButton("🚀 JOIN CHANNEL 🚀", url=CHANNEL_LINK)],
            [InlineKeyboardButton("📞 CONTACT SUPPORT 📞", url=SUPPORT_LINK)]
        ]

        update.message.reply_text(
            """
🎉 VIP VERIFICATION SUCCESSFUL

💎 ACCESS GRANTED 💎
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return

    # PREDICTION SYSTEM
    if user_waiting.get(user_id):

        if not text.isdigit() or len(text) != 3:

            update.message.reply_text(
                "❌ SEND ONLY 3 DIGIT NUMBER"
            )

            return

        result = random.choice(["BIG", "SMALL"])

        if result == "BIG":
            numbers = random.sample(range(1, 5), 2)
        else:
            numbers = random.sample(range(5, 10), 2)

        accuracy = random.randint(93, 99)

        keyboard = [
            [InlineKeyboardButton("🎯 GET PREDICTION AGAIN 🎯", callback_data="prediction")],
            [InlineKeyboardButton("📞 CONTACT SUPPORT 📞", url=SUPPORT_LINK)],
            [InlineKeyboardButton("🔥 VIP REGISTRATION 🔥", url=REGISTRATION_LINK)],
            [InlineKeyboardButton("🚀 JOIN TEHELKA CHANNEL 🚀", url=CHANNEL_LINK)]
        ]

        update.message.reply_text(
            f"""
💎 TEHELKA VIP 💎

🎲 PERIOD NUMBER
➤ {text}

━━━━━━━━━━━━━━━━━━

📊 RESULT
➤ {result}

━━━━━━━━━━━━━━━━━━

🔢 SAFE NUMBERS
➤ {numbers[0]} • {numbers[1]}

━━━━━━━━━━━━━━━━━━

📈 ACCURACY
➤ {accuracy}%

━━━━━━━━━━━━━━━━━━
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ===================================
# 10 MIN ALERT
# ===================================

def send_alert(bot):

    bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=STICKER_10MIN
    )

    bot.send_message(
        chat_id=CHANNEL_ID,
        text="""
🚨 VIP ALERT 🚨

🔥 BIG SESSION STARTING IN 10 MINUTES 🔥
"""
    )

# ===================================
# 2 MIN ALERT
# ===================================

def send_2min_alert(bot):

    bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=STICKER_2MIN
    )

    bot.send_message(
        chat_id=CHANNEL_ID,
        text="""
⏰ 2 MINUTES LEFT ⏰

🔥 STAY READY VIP MEMBERS 🔥
"""
    )

# ===================================
# FINAL ALERT
# ===================================

def send_final_alert(bot):

    bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=STICKER_1MIN
    )

    bot.send_message(
        chat_id=CHANNEL_ID,
        text="""
⏰ FINAL ALERT ⏰

🔥 SESSION STARTING IN 1 MINUTE 🔥
"""
    )

# ===================================
# SEND PREDICTION
# ===================================

def send_prediction(bot):

    if random.randint(1, 3) == 1:

        bot.send_sticker(
            chat_id=CHANNEL_ID,
            sticker=random.choice([
                STICKER_MIDDLE_1,
                STICKER_MIDDLE_2
            ])
        )

    result = random.choice(["BIG", "SMALL"])

    if result == "BIG":
        numbers = random.sample(range(1, 5), 2)
    else:
        numbers = random.sample(range(5, 10), 2)

    accuracy = random.randint(93, 99)

    keyboard = [
        [InlineKeyboardButton("📞 CONTACT SUPPORT 📞", url=SUPPORT_LINK)],
        [InlineKeyboardButton("🔥 VIP REGISTRATION 🔥", url=REGISTRATION_LINK)],
        [InlineKeyboardButton("🚀 JOIN TEHELKA CHANNEL 🚀", url=CHANNEL_LINK)]
    ]

    text = f"""
💎 TEHELKA VIP 💎

🎮 WINGO 1 MINUTE

━━━━━━━━━━━━━━━━━━

📊 RESULT
➤ {result}

━━━━━━━━━━━━━━━━━━

🔢 SAFE NUMBERS
➤ {numbers[0]} • {numbers[1]}

━━━━━━━━━━━━━━━━━━

📈 ACCURACY
➤ {accuracy}%

━━━━━━━━━━━━━━━━━━
"""

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ===================================
# SESSION END MESSAGE
# ===================================

def send_end_message(bot):

    bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=STICKER_END_1
    )

    bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=STICKER_END_2
    )

    bot.send_message(
        chat_id=CHANNEL_ID,
        text="""
💎 VIP TEHELKA 💎

🔥 WINGO 1MIN VIP PREDICTION 🔥

✅ High Accuracy Signal
✅ Safe Number Support
✅ Daily VIP Entry

━━━━━━━━━━━━━━━━━━

🚀 JOIN VIP CHANNEL
https://t.me/TEHELKA_VIP_KING

🔥 REGISTER HERE
https://13lwin6.com/register?inviteCode=C6APK4N&from=web

📩 AFTER REGISTER
SEND YOUR UID NUMBER

📞 SUPPORT
https://t.me/Next_level_user

━━━━━━━━━━━━━━━━━━

💎 VIP TEHELKA 💎
"""
    )

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

    scheduler.configure(job_defaults={'max_instances': 1})

    # 10 MIN ALERTS
    for hour in [9, 11, 15, 19]:

        scheduler.add_job(
            lambda: send_alert(updater.bot),
            'cron',
            hour=hour,
            minute=50
        )

    # 2 MIN ALERTS
    for hour in [9, 11, 15, 19]:

        scheduler.add_job(
            lambda: send_2min_alert(updater.bot),
            'cron',
            hour=hour,
            minute=58
        )

    # FINAL ALERTS
    for hour in [9, 11, 15, 19]:

        scheduler.add_job(
            lambda: send_final_alert(updater.bot),
            'cron',
            hour=hour,
            minute=59
        )

    # PREDICTIONS
    for minute in range(0, 11):

        scheduler.add_job(
            lambda: send_prediction(updater.bot),
            'cron',
            hour=10,
            minute=minute,
            second=10
        )

        scheduler.add_job(
            lambda: send_prediction(updater.bot),
            'cron',
            hour=12,
            minute=minute,
            second=10
        )

        scheduler.add_job(
            lambda: send_prediction(updater.bot),
            'cron',
            hour=16,
            minute=minute,
            second=10
        )

        scheduler.add_job(
            lambda: send_prediction(updater.bot),
            'cron',
            hour=20,
            minute=minute,
            second=10
        )

    # SESSION END
    for hour in [10, 12, 16, 20]:

        scheduler.add_job(
            lambda: send_end_message(updater.bot),
            'cron',
            hour=hour,
            minute=11
        )

    scheduler.start()

    print("VIP TEHELKA BOT STARTED")

    updater.start_polling()

    updater.idle()

# ===================================

if __name__ == "__main__":
    main()
