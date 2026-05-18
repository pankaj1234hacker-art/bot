import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

# ================= CONFIG =================

BOT_TOKEN = "8775211756:AAFWtG1PNM393_nPcAchCNaDuEKIilhjGGg"

CHANNEL_ID = "@YOUR_CHANNEL"

VIP_CHANNEL = "https://t.me/TEHELKA_VIP_KING"
REGISTER_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"
SUPPORT_LINK = "https://t.me/Next_level_user"

# ================= LOG =================

logging.basicConfig(level=logging.INFO)

# ================= USER DATA =================

uid_wait = set()
predict_wait = set()

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🔥 REGISTER", url=REGISTER_LINK)],
        [InlineKeyboardButton("✅ I HAVE REGISTERED", callback_data="reg")]
    ]

    await update.message.reply_text(
        "💎 VIP TEHELKA BOT\n\nStart Now 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= BUTTON =================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "reg":
        uid_wait.add(user_id)
        await query.message.reply_text("📩 Send your UID number")

    elif query.data == "pred":
        predict_wait.add(user_id)
        await query.message.reply_text("📌 Send last 3 digit of period")

# ================= MESSAGE =================

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    text = update.message.text

    # -------- UID --------
    if user_id in uid_wait:
        if text.isdigit():

            uid_wait.remove(user_id)

            keyboard = [[InlineKeyboardButton("🎯 GET PREDICTION", callback_data="pred")]]

            await update.message.reply_text(
                "✅ UID VERIFIED",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_text("❌ Only number allowed")
        return

    # -------- PRED --------
    if user_id in predict_wait:
        if text.isdigit():

            predict_wait.remove(user_id)

            await update.message.reply_text("📊 ANALYZING...")

            import asyncio
            await asyncio.sleep(5)

            result = random.choice(["BIG", "SMALL"])

            range_text = "5-9 🔵" if result == "BIG" else "0-4 🔴"

            keyboard = [
                [InlineKeyboardButton("💎 VIP CHANNEL", url=VIP_CHANNEL)],
                [InlineKeyboardButton("📞 SUPPORT", url=SUPPORT_LINK)],
                [InlineKeyboardButton("🔥 AGAIN", callback_data="pred")]
            ]

            await update.message.reply_text(
f"""
🔥 VIP PREDICTION

📌 PERIOD: {text}

🎯 RESULT: {result}

👉 {range_text}
""",
reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_text("❌ Send only digits")

# ================= CHANNEL SCHEDULER =================

def send_sticker(bot):
    bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker="YOUR_STICKER_FILE_ID"
    )

def send_prediction(bot):

    result = random.choice(["BIG", "SMALL"])
    period = random.randint(100,999)

    msg = f"""
🔥 CHANNEL PREDICTION

📌 PERIOD: {period}

🎯 RESULT: {result}
"""

    bot.send_message(chat_id=CHANNEL_ID, text=msg)

# ================= MAIN =================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    # handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

    scheduler = BackgroundScheduler(timezone=timezone("Asia/Kolkata"))

    # STICKER at :05
    scheduler.add_job(send_sticker, "cron",
                      hour="8,10,12,16,20",
                      minute="*",
                      second="5",
                      args=[app.bot])

    # PREDICTION at :10
    scheduler.add_job(send_prediction, "cron",
                      hour="8,10,12,16,20",
                      minute="*",
                      second="10",
                      args=[app.bot])

    scheduler.start()

    print("BOT RUNNING...")

    app.run_polling()

# ================= RUN =================

if __name__ == "__main__":
    main()
