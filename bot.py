import random
import logging
import asyncio

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone


# =====================================
# BOT CONFIG
# =====================================

BOT_TOKEN = "8775211756:AAFWtG1PNM393_nPcAchCNaDuEKIilhjGGg"

CHANNEL_ID = "@YOUR_CHANNEL_USERNAME"

VIP_CHANNEL = "https://t.me/YOUR_CHANNEL_USERNAME"

REGISTER_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"

SUPPORT_LINK = "https://t.me/Next_level_user"


# =====================================
# STICKERS
# =====================================

STICKER_10MIN = "CAACAgUAAxkBAAIBP2oKn8i0a1JqoNAqRLTxvqcwJzoWAAIXEwACvmTQVn4hqlDaxy8AATsE"

STICKER_2MIN = "CAACAgUAAyEFAATloOE5AAICAmoJ1-y3HvygDNQQukQL63uJdoOnAAKFEQACflHJVvhHK40SVtJHOwQ"

STICKER_1MIN = "CAACAgUAAxkBAAIBSWoKopjKbEtd9eRIFwxok8JzHV4FAALSEAACt-6xVytut0bPId8JOwQ"

RUNNING_STICKER = "CAACAgUAAyEFAATloOE5AAIB9WoJ02vKgrKJ85e-5vvj5CytikTsAAIiEgACUUDJVkSsO8zj-IA5OwQ"

EXTRA_STICKER_1 = "CAACAgUAAyEFAATloOE5AAIB6GoJ0iO50gAB2ZmmjkaahT3EJ9t7ygACahIAAvYiyVZikUGUoRZynzsE"

EXTRA_STICKER_2 = "CAACAgUAAyEFAATloOE5AAICBWoJ2CqnDBifKRuJWOsCrtKxtgvQAAIXFwACvDMZV1AUT-rGMRluOwQ"

END_STICKER_1 = "CAACAgUAAxkBAAIBUWoKo0uIfCGeV5GfZU0Fv_hYOe8HAALYEQACMazJVuD7AUjcPT_gOwQ"

END_STICKER_2 = "CAACAgUAAxkBAAIBU2oKo39yvzCGf62ZmLIMd3cQk2TaAAJ-EwACnQdoV6lN-23qPLHPOwQ"


# =====================================
# LOG
# =====================================

logging.basicConfig(level=logging.INFO)


# =====================================
# MEMORY
# =====================================

uid_wait = set()
prediction_wait = set()


# =====================================
# WELCOME TEXT
# =====================================

WELCOME_TEXT = """
╔════💎 VIP TEHELKA 💎════╗

🔥 WELCOME TO VIP TEHELKA 🔥

📈 MOST POWERFUL WINGO BOT
🎯 DAILY SAFE PREDICTION
⚡ FAST RESULT
🔐 UID VERIFICATION SYSTEM

━━━━━━━━━━━━━━━━

🚨 JOIN VIP CHANNEL & COMPLETE REGISTRATION 🚨
"""


# =====================================
# START COMMAND
# =====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [InlineKeyboardButton("💎 VIP CHANNEL", url=VIP_CHANNEL)],

        [InlineKeyboardButton("🔥 REGISTRATION", url=REGISTER_LINK)],

        [InlineKeyboardButton("📞 CONTACT SUPPORT", url=SUPPORT_LINK)],

        [InlineKeyboardButton("✅ I HAVE REGISTERED", callback_data="register_done")]

    ]

    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =====================================
# BUTTON SYSTEM
# =====================================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # REGISTER BUTTON
    if query.data == "register_done":

        uid_wait.add(user_id)

        await query.message.reply_text(
            "📌 SEND YOUR GAME UID NUMBER"
        )

    # PREDICTION BUTTON
    elif query.data == "get_prediction":

        prediction_wait.add(user_id)

        await query.message.reply_text(
            "📌 SEND LAST 3 DIGIT PERIOD NUMBER"
        )


# =====================================
# MESSAGE SYSTEM
# =====================================

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    text = update.message.text.strip()

    # UID VERIFY
    if user_id in uid_wait:

        if text.isdigit():

            uid_wait.remove(user_id)

            keyboard = [

                [InlineKeyboardButton("🔥 REGISTRATION", url=REGISTER_LINK)],

                [InlineKeyboardButton("📞 CONTACT SUPPORT", url=SUPPORT_LINK)],

                [InlineKeyboardButton("💎 VIP CHANNEL", url=VIP_CHANNEL)],

                [InlineKeyboardButton("🎯 GET PREDICTION", callback_data="get_prediction")]

            ]

            await update.message.reply_text(
                "✅ UID VERIFIED SUCCESSFULLY",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        else:

            await update.message.reply_text(
                "❌ ONLY NUMBER ALLOWED"
            )

        return


    # PREDICTION SYSTEM
    if user_id in prediction_wait:

        if not text.isdigit() or len(text) != 3:

            await update.message.reply_text(
                "❌ INVALID PERIOD NUMBER\n\n✅ SEND ONLY 3 DIGITS"
            )

            return

        prediction_wait.remove(user_id)

        await update.message.reply_text(
            "📊 MARKET ANALYZING..."
        )

        await asyncio.sleep(5)

        result = random.choice(["BIG", "SMALL"])

        # BIG = 0-4
        if result == "BIG":

            nums = random.sample(range(0, 5), 2)

        # SMALL = 5-9
        else:

            nums = random.sample(range(5, 10), 2)

        keyboard = [

            [InlineKeyboardButton("🎯 GET PREDICTION AGAIN", callback_data="get_prediction")],

            [InlineKeyboardButton("💎 VIP CHANNEL", url=VIP_CHANNEL)],

            [InlineKeyboardButton("📞 CONTACT SUPPORT", url=SUPPORT_LINK)]

        ]

        prediction_text = f"""
╔════💎 VIP TEHELKA 💎════╗

🕒 PERIOD: {text}

🎯 RESULT: {result}

🔥 SAFE NUMBERS: {nums[0]} • {nums[1]}

━━━━━━━━━━━━━━━━

🔥 WINGO 1MIN GAME 🔥
"""

        await update.message.reply_text(
            prediction_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return


# =====================================
# CHANNEL STICKER
# =====================================

async def send_sticker(app, sticker):

    await app.bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=sticker
    )


# =====================================
# CHANNEL PREDICTION
# =====================================

async def send_prediction(app):

    result = random.choice(["BIG", "SMALL"])

    # BIG = 0-4
    if result == "BIG":

        nums = random.sample(range(0, 5), 2)

    # SMALL = 5-9
    else:

        nums = random.sample(range(5, 10), 2)

    text = f"""
╔════💎 VIP TEHELKA 💎════╗

🕒 PERIOD: ***

🎯 RESULT: {result}

🔥 SAFE NUMBERS: {nums[0]} • {nums[1]}

━━━━━━━━━━━━━━━━

🔥 WINGO 1MIN GAME 🔥
"""

    keyboard = [

        [InlineKeyboardButton("🔥 REGISTRATION", url=REGISTER_LINK)],

        [InlineKeyboardButton("💎 VIP CHANNEL", url=VIP_CHANNEL)],

        [InlineKeyboardButton("📞 CONTACT SUPPORT", url=SUPPORT_LINK)]

    ]

    await app.bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =====================================
# MAIN FUNCTION
# =====================================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    # HANDLERS
    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(buttons))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            messages
        )
    )

    # INDIA TIMEZONE
    scheduler = AsyncIOScheduler(
        timezone=timezone("Asia/Kolkata")
    )


    # =====================================
    # BEFORE START STICKERS
    # =====================================

    # 10 minute before
    scheduler.add_job(
        send_sticker,
        "cron",
        hour="9,11,15,19",
        minute=50,
        args=[app, STICKER_10MIN]
    )

    # 2 minute before
    scheduler.add_job(
        send_sticker,
        "cron",
        hour="9,11,15,19",
        minute=58,
        args=[app, STICKER_2MIN]
    )

    # 1 minute before
    scheduler.add_job(
        send_sticker,
        "cron",
        hour="9,11,15,19",
        minute=59,
        args=[app, STICKER_1MIN]
    )


    # =====================================
    # RUNNING SESSION
    # =====================================

    # running sticker every minute
    scheduler.add_job(
        send_sticker,
        "cron",
        hour="10,12,16,20",
        minute="0-10",
        second=5,
        args=[app, RUNNING_STICKER]
    )

    # prediction every minute
    scheduler.add_job(
        send_prediction,
        "cron",
        hour="10,12,16,20",
        minute="0-10",
        second=10,
        args=[app]
    )


    # =====================================
    # EXTRA PREMIUM STICKERS
    # =====================================

    scheduler.add_job(
        send_sticker,
        "cron",
        hour="10,12,16,20",
        minute="2,5,8",
        second=20,
        args=[app, EXTRA_STICKER_1]
    )

    scheduler.add_job(
        send_sticker,
        "cron",
        hour="10,12,16,20",
        minute="3,6,9",
        second=25,
        args=[app, EXTRA_STICKER_2]
    )


    # =====================================
    # SESSION END
    # =====================================

    scheduler.add_job(
        send_sticker,
        "cron",
        hour="10,12,16,20",
        minute=10,
        second=40,
        args=[app, END_STICKER_1]
    )

    scheduler.add_job(
        send_sticker,
        "cron",
        hour="10,12,16,20",
        minute=10,
        second=50,
        args=[app, END_STICKER_2]
    )


    # START SCHEDULER
    scheduler.start()

    print("🔥 VIP TEHELKA BOT RUNNING 🔥")

    # START BOT
    app.run_polling()


# =====================================
# RUN
# =====================================

if __name__ == "__main__":
    main()
