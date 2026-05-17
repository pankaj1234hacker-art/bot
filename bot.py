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
# CONFIG
# ===================================

TOKEN = "8775211756:AAFWtG1PNM393_nPcAchCNaDuEKIilhjGGg"

ADMIN_ID = 8793501975

CHANNEL_ID = "@TEHELKA_VIP_KING"

CHANNEL_LINK = "https://t.me/TEHELKA_VIP_KING"

SUPPORT_LINK = "https://t.me/Next_level_user"

REGISTRATION_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"

# ===================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

timezone = pytz.timezone("Asia/Kolkata")

verified_users = set()
all_users = set()

# ===================================
# START
# ===================================

def start(update: Update, context: CallbackContext):

    user_id = update.message.from_user.id

    all_users.add(user_id)

    keyboard = [
        [InlineKeyboardButton("🔥 VIP REGISTRATION 🔥", url=REGISTRATION_LINK)],
        [InlineKeyboardButton("🚀 JOIN TEHELKA CHANNEL 🚀", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I HAVE REGISTERED ✅", callback_data="registered")]
    ]

    text = """
╔══════════════════════╗
      💎 VIP TEHELKA 💎
╚══════════════════════╝

🔥 MOST POWERFUL WINGO BOT 🔥

⚡ PREMIUM VIP PREDICTION
⚡ HIGH ACCURACY SIGNAL
⚡ FAST WINNING SUPPORT

━━━━━━━━━━━━━━━━━━

📌 COMPLETE REGISTRATION FIRST
📌 THEN VERIFY YOUR UID

━━━━━━━━━━━━━━━━━━
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

    # REGISTERED BUTTON
    if query.data == "registered":

        context.user_data["waiting_uid"] = True

        query.message.reply_text(
            """
╔══════════════════════╗
      🔐 UID VERIFY 🔐
╚══════════════════════╝

📥 SEND YOUR GAME UID NUMBER

━━━━━━━━━━━━━━━━━━

⚡ AFTER VERIFICATION
VIP PREDICTION ACCESS
WILL BE ACTIVATED
"""
        )

    # PREDICTION BUTTON
    elif query.data == "prediction":

        context.user_data["waiting_prediction"] = True

        query.message.reply_text(
            """
╔══════════════════════╗
   🎯 GET PREDICTION 🎯
╚══════════════════════╝

📩 SEND ANY 3 DIGIT NUMBER

Example:
123

━━━━━━━━━━━━━━━━━━
"""
        )

# ===================================
# MESSAGES
# ===================================

def handle_message(update: Update, context: CallbackContext):

    user_id = update.message.from_user.id

    text = update.message.text.strip()

    all_users.add(user_id)

    # ===================================
    # UID VERIFY
    # ===================================

    if context.user_data.get("waiting_uid"):

        verified_users.add(user_id)

        context.user_data["waiting_uid"] = False

        keyboard = [
            [InlineKeyboardButton("🎯 GET PREDICTION 🎯", callback_data="prediction")],
            [InlineKeyboardButton("🔥 VIP REGISTRATION 🔥", url=REGISTRATION_LINK)],
            [InlineKeyboardButton("🚀 JOIN CHANNEL 🚀", url=CHANNEL_LINK)],
            [InlineKeyboardButton("📞 CONTACT SUPPORT 📞", url=SUPPORT_LINK)]
        ]

        update.message.reply_text(
            """
╔══════════════════════╗
   🎉 UID VERIFIED 🎉
╚══════════════════════╝

🔥 VIP ACCESS ACTIVATED 🔥

⚡ PREDICTION ENABLED
⚡ PREMIUM SIGNAL ACCESS
⚡ FAST ENTRY SUPPORT

━━━━━━━━━━━━━━━━━━
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return

    # ===================================
    # PREDICTION SYSTEM
    # ===================================

    if context.user_data.get("waiting_prediction"):

        if not text.isdigit() or len(text) != 3:

            update.message.reply_text(
                """
❌ INVALID NUMBER

PLEASE SEND ONLY
3 DIGIT NUMBER

Example:
123
"""
            )

            return

        result = random.choice(["BIG", "SMALL"])

        # BIG = 1-4
        if result == "BIG":
            numbers = random.sample(range(1, 5), 2)

        # SMALL = 5-9
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
╔══════════════════════╗
      💎 TEHELKA VIP 💎
╚══════════════════════╝

        🎮 WINGO 1 MINUTE 🎮

━━━━━━━━━━━━━━━━━━

🎲 PERIOD NUMBER
➤ {text}

━━━━━━━━━━━━━━━━━━

📊 RESULT
➤ {result}

━━━━━━━━━━━━━━━━━━

🔢 SAFE NUMBERS
➤ {numbers[0]}  •  {numbers[1]}

━━━━━━━━━━━━━━━━━━

📈 ACCURACY
➤ {accuracy}%

━━━━━━━━━━━━━━━━━━

🔥 PREMIUM VIP SIGNAL 🔥

⚡ HIGH ACCURACY PREDICTION
⚡ VIP WINNING FORMAT
⚡ SAFE ENTRY SUPPORT

━━━━━━━━━━━━━━━━━━
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        context.user_data["waiting_prediction"] = False

# ===================================
# AUTO ALERT
# ===================================

def send_alert(bot):

    text = """
╔══════════════════════╗
      🚨 VIP ALERT 🚨
╚══════════════════════╝

🔥 BIG PREDICTION SESSION 🔥

⚡ GET READY FOR ENTRY
⚡ PREMIUM SIGNAL STARTING

━━━━━━━━━━━━━━━━━━
"""

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=text
    )

# ===================================
# FINAL ALERT
# ===================================

def send_final_alert(bot):

    text = """
╔══════════════════════╗
      ⏰ FINAL ALERT ⏰
╚══════════════════════╝

🔥 PREDICTION STARTING
IN 1 MINUTE 🔥

⚡ STAY READY
⚡ DON'T MISS ENTRY

━━━━━━━━━━━━━━━━━━
"""

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=text
    )

# ===================================
# AUTO PREDICTION POST
# ===================================

def send_prediction(bot):

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
╔══════════════════════╗
   💎 AUTO PREDICTION 💎
╚══════════════════════╝

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

🔥 VIP TEHELKA 🔥

━━━━━━━━━━━━━━━━━━
"""

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ===================================
# ADMIN PANEL
# ===================================

def panel(update: Update, context: CallbackContext):

    if update.message.from_user.id != ADMIN_ID:
        return

    update.message.reply_text(
        f"""
👑 ADMIN PANEL 👑

👥 TOTAL USERS:
{len(all_users)}

✅ VERIFIED USERS:
{len(verified_users)}
"""
    )

# ===================================
# BROADCAST
# ===================================

def broadcast(update: Update, context: CallbackContext):

    if update.message.from_user.id != ADMIN_ID:
        return

    msg = update.message.text.replace("/broadcast", "").strip()

    if not msg:

        update.message.reply_text(
            "❌ SEND MESSAGE"
        )

        return

    sent = 0

    for user in all_users:

        try:

            context.bot.send_message(
                chat_id=user,
                text=msg
            )

            sent += 1

        except:
            pass

    update.message.reply_text(
        f"✅ MESSAGE SENT TO {sent} USERS"
    )

# ===================================
# MAIN
# ===================================

def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    # COMMANDS
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("panel", panel))
    dp.add_handler(CommandHandler("broadcast", broadcast))

    # BUTTONS
    dp.add_handler(CallbackQueryHandler(button))

    # MESSAGES
    dp.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command,
            handle_message
        )
    )

    # SCHEDULER
    scheduler = BackgroundScheduler(
        timezone=timezone
    )

    # ===================================
    # 10 MIN ALERTS
    # ===================================

    scheduler.add_job(
        lambda: send_alert(updater.bot),
        'cron',
        hour=9,
        minute=50
    )

    scheduler.add_job(
        lambda: send_alert(updater.bot),
        'cron',
        hour=11,
        minute=50
    )

    scheduler.add_job(
        lambda: send_alert(updater.bot),
        'cron',
        hour=15,
        minute=50
    )

    scheduler.add_job(
        lambda: send_alert(updater.bot),
        'cron',
        hour=19,
        minute=50
    )

    # ===================================
    # FINAL ALERTS
    # ===================================

    scheduler.add_job(
        lambda: send_final_alert(updater.bot),
        'cron',
        hour=9,
        minute=59
    )

    scheduler.add_job(
        lambda: send_final_alert(updater.bot),
        'cron',
        hour=11,
        minute=59
    )

    scheduler.add_job(
        lambda: send_final_alert(updater.bot),
        'cron',
        hour=15,
        minute=59
    )

    scheduler.add_job(
        lambda: send_final_alert(updater.bot),
        'cron',
        hour=19,
        minute=59
    )

    # ===================================
    # AUTO POSTS
    # ===================================

    for minute in range(0, 11):

        scheduler.add_job(
            lambda: send_prediction(updater.bot),
            'cron',
            hour=10,
            minute=minute
        )

        scheduler.add_job(
            lambda: send_prediction(updater.bot),
            'cron',
            hour=12,
            minute=minute
        )

        scheduler.add_job(
            lambda: send_prediction(updater.bot),
            'cron',
            hour=16,
            minute=minute
        )

        scheduler.add_job(
            lambda: send_prediction(updater.bot),
            'cron',
            hour=20,
            minute=minute
        )

    scheduler.start()

    print("🔥 VIP TEHELKA BOT STARTED 🔥")

    updater.start_polling()

    updater.idle()

# ===================================

if __name__ == "__main__":
    main()
