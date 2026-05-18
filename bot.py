import logging
import random
import asyncio
import pytz

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler

# =========================
# BOT TOKEN
# =========================

BOT_TOKEN = "8775211756:AAFWtG1PNM393_nPcAchCNaDuEKIilhjGGg"

# =========================
# CHANNEL + LINKS
# =========================

CHANNEL_ID = "@TEHELKA_VIP_KING"

CHANNEL_LINK = "https://t.me/TEHELKA_VIP_KING"

REGISTER_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"

SUPPORT_LINK = "https://t.me/Next_level_user"

BOT_LINK = "https://t.me/Vip_Number_sureshot_bot"

# =========================
# STICKERS
# =========================

STICKER_2MIN = "CAACAgUAAyEFAATloOE5AAICAmoJ1-y3HvygDNQQukQL63uJdoOnAAKFEQACflHJVvhHK40SVtJHOwQ"

STICKER_1MIN = "CAACAgUAAxkBAAIBP2oKn8i0a1JqoNAqRLTxvqcwJzoWAAIXEwACvmTQVn4hqlDaxy8AATsE"

STICKER_START = "CAACAgUAAxkBAAIBSWoKopjKbEtd9eRIFwxok8JzHV4FAALSEAACt-6xVytut0bPId8JOwQ"

STICKER_MIDDLE1 = "CAACAgUAAyEFAATloOE5AAIB9WoJ02vKgrKJ85e-5vvj5CytikTsAAIiEgACUUDJVkSsO8zj-IA5OwQ"

STICKER_MIDDLE2 = "CAACAgUAAyEFAATloOE5AAIB6GoJ0iO50gAB2ZmmjkaahT3EJ9t7ygACahIAAvYiyVZikUGUoRZynzsE"

STICKER_MIDDLE3 = "CAACAgUAAyEFAATloOE5AAICBWoJ2CqnDBifKRuJWOsCrtKxtgvQAAIXFwACvDMZV1AUT-rGMRluOwQ"

STICKER_END = "CAACAgUAAxkBAAIBUWoKo0uIfCGeV5GfZU0Fv_hYOe8HAALYEQACMazJVuD7AUjcPT_gOwQ"

STICKER_FINAL = "CAACAgUAAxkBAAIBU2oKo39yvzCGf62ZmLIMd3cQk2TaAAJ-EwACnQdoV6lN-23qPLHPOwQ"

# =========================
# FINAL MESSAGE
# =========================

FINAL_MESSAGE = """
💎 VIP TEHELKA 💎

🔥 WINGO 1MIN VIP PREDICTION 🔥

✅ High Accuracy Signal
✅ Safe Number Support
✅ Daily VIP Entry

━━━━━━━━━━━━━━━━━━

🚀 JOIN VIP CHANNEL:
https://t.me/TEHELKA_VIP_KING

🔥 REGISTER HERE:
https://13lwin6.com/register?inviteCode=C6APK4N&from=web

📩 AFTER REGISTER
SEND YOUR UID NUMBER

📞 SUPPORT:
https://t.me/Next_level_user

━━━━━━━━━━━━━━━━━━

💎 VIP TEHELKA 💎
"""

# =========================
# LOGGING
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# NUMBER GENERATOR
# =========================

def generate_prediction():
    return random.randint(0, 9)

# =========================
# BUTTONS
# =========================

def main_buttons():
    keyboard = [
        [
            InlineKeyboardButton(
                "🔥 JOIN VIP CHANNEL 🔥",
                url=CHANNEL_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "📝 REGISTER NOW",
                url=REGISTER_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "📞 SUPPORT",
                url=SUPPORT_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "🎯 GET PREDICTION AGAIN",
                url=BOT_LINK
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)

# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = f"""
💎 VIP TEHELKA 💎

🔥 Welcome To VIP Prediction Bot 🔥

✅ Premium Prediction System
✅ Daily Wingo Prediction
✅ VIP Support Available

━━━━━━━━━━━━━━━━━━

🚀 Join Channel:
{CHANNEL_LINK}

🔥 Register:
{REGISTER_LINK}

📞 Support:
{SUPPORT_LINK}

━━━━━━━━━━━━━━━━━━
"""

    await update.message.reply_text(
        text,
        reply_markup=main_buttons()
    )

# =========================
# NORMAL REPLY
# =========================

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 VIP PREDICTION READY 🔥

Click Below Button 👇
"""

    await update.message.reply_text(
        text,
        reply_markup=main_buttons()
    )

# =========================
# SESSION SYSTEM
# =========================

async def run_prediction_session(app):

    await app.bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=STICKER_START
    )

    await asyncio.sleep(10)

    for i in range(10):

        number = generate_prediction()

        msg = f"""
🎯 VIP TEHELKA PREDICTION 🎯

🔥 NUMBER : {number}

⏰ ENTRY FAST
"""

        await app.bot.send_message(
            chat_id=CHANNEL_ID,
            text=msg
        )

        if i == 2:
            await app.bot.send_sticker(
                chat_id=CHANNEL_ID,
                sticker=STICKER_MIDDLE1
            )

        if i == 5:
            await app.bot.send_sticker(
                chat_id=CHANNEL_ID,
                sticker=STICKER_MIDDLE2
            )

        if i == 7:
            await app.bot.send_sticker(
                chat_id=CHANNEL_ID,
                sticker=STICKER_MIDDLE3
            )

        await asyncio.sleep(70)

    await app.bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=STICKER_END
    )

    await asyncio.sleep(3)

    await app.bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=STICKER_FINAL
    )

    await asyncio.sleep(2)

    await app.bot.send_message(
        chat_id=CHANNEL_ID,
        text=FINAL_MESSAGE
    )

# =========================
# ALERT SYSTEM
# =========================

async def send_2min_alert(app):

    await app.bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=STICKER_2MIN
    )

    await app.bot.send_message(
        chat_id=CHANNEL_ID,
        text="⏰ READY STAY... PREDICTION START SOON"
    )

async def send_1min_alert(app):

    await app.bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=STICKER_1MIN
    )

    await app.bot.send_message(
        chat_id=CHANNEL_ID,
        text="🔥 1 MIN LEFT..."
    )

# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            auto_reply
        )
    )

    scheduler = AsyncIOScheduler(
        timezone=pytz.timezone("Asia/Kolkata")
    )

    # =====================
    # 10 AM SESSION
    # =====================

    scheduler.add_job(
        lambda: asyncio.create_task(send_2min_alert(app)),
        trigger='cron',
        hour=9,
        minute=58
    )

    scheduler.add_job(
        lambda: asyncio.create_task(send_1min_alert(app)),
        trigger='cron',
        hour=9,
        minute=59
    )

    scheduler.add_job(
        lambda: asyncio.create_task(run_prediction_session(app)),
        trigger='cron',
        hour=10,
        minute=0
    )

    # =====================
    # 12 PM SESSION
    # =====================

    scheduler.add_job(
        lambda: asyncio.create_task(send_2min_alert(app)),
        trigger='cron',
        hour=11,
        minute=58
    )

    scheduler.add_job(
        lambda: asyncio.create_task(send_1min_alert(app)),
        trigger='cron',
        hour=11,
        minute=59
    )

    scheduler.add_job(
        lambda: asyncio.create_task(run_prediction_session(app)),
        trigger='cron',
        hour=12,
        minute=0
    )

    # =====================
    # 4 PM SESSION
    # =====================

    scheduler.add_job(
        lambda: asyncio.create_task(send_2min_alert(app)),
        trigger='cron',
        hour=15,
        minute=58
    )

    scheduler.add_job(
        lambda: asyncio.create_task(send_1min_alert(app)),
        trigger='cron',
        hour=15,
        minute=59
    )

    scheduler.add_job(
        lambda: asyncio.create_task(run_prediction_session(app)),
        trigger='cron',
        hour=16,
        minute=0
    )

    # =====================
    # 8 PM SESSION
    # =====================

    scheduler.add_job(
        lambda: asyncio.create_task(send_2min_alert(app)),
        trigger='cron',
        hour=19,
        minute=58
    )

    scheduler.add_job(
        lambda: asyncio.create_task(send_1min_alert(app)),
        trigger='cron',
        hour=19,
        minute=59
    )

    scheduler.add_job(
        lambda: asyncio.create_task(run_prediction_session(app)),
        trigger='cron',
        hour=20,
        minute=0
    )

    scheduler.start()

    print("BOT STARTED SUCCESSFULLY")

    app.run_polling()

# =========================
# RUN
# =========================

if __name__ == "__main__":
    main()
