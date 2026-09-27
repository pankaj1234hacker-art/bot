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

BOT_TOKEN = "8775211756:AAH71BWiFcy0wlmaez0orQzzk7JU1kqFMs4"

CHANNEL_ID = "@TEHELKA_VIP_KING"

VIP_CHANNEL = "https://t.me/TEHELKA_VIP_KING"

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
# LOGGING
# =====================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)


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

    if query.data == "register_done":

        uid_wait.add(user_id)

        await query.message.reply_text(
            "📌 SEND YOUR GAME UID NUMBER"
        )

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

    # =================================
    # UID SYSTEM
    # =================================

    if user_id in uid_wait:

        if text.isdigit():

            uid_wait.remove(user_id)
