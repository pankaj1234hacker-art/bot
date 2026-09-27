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
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

BOT_TOKEN = "8775211756:AAH71BWiFcy0wlmaez0orQzzk7JU1kqFMs4"
CHANNEL_ID = "@TEHELKA_VIP_KING"

VIP_CHANNEL = "https://t.me/TEHELKA_VIP_KING"
SUPPORT_LINK = "https://t.me/Next_level_user"
REGISTER_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"

# Existing sticker IDs
STICKER_10MIN = "CAACAgUAAxkBAAIBP2oKn8i0a1JqoNAqRLTxvqcwJzoWAAIXEwACvmTQVn4hqlDaxy8AATsE"
STICKER_2MIN = "CAACAgUAAyEFAATloOE5AAICAmoJ1-y3HvygDNQQukQL63uJdoOnAAKFEQACflHJVvhHK40SVtJHOwQ"
STICKER_1MIN = "CAACAgUAAxkBAAIBSWoKopjKbEtd9eRIFwxok8JzHV4FAALSEAACt-6xVytut0bPId8JOwQ"
RUNNING_STICKER = "CAACAgUAAyEFAATloOE5AAIB9WoJ02vKgrKJ85e-5vvj5CytikTsAAIiEgACUUDJVkSsO8zj-IA5OwQ"
EXTRA_STICKER_1 = "CAACAgUAAyEFAATloOE5AAIB6GoJ0iO50gAB2ZmmjkaahT3EJ9t7ygACahIAAvYiyVZikUGUoRZynzsE"
EXTRA_STICKER_2 = "CAACAgUAAyEFAATloOE5AAICBWoJ2CqnDBifKRuJWOsCrtKxtgvQAAIXFwACvDMZV1AUT-rGMRluOwQ"
END_STICKER_1 = "CAACAgUAAxkBAAIBUWoKo0uIfCGeV5GfZU0Fv_hYOe8HAALYEQACMazJVuD7AUjcPT_gOwQ"
END_STICKER_2 = "CAACAgUAAxkBAAIBU2oKo39yvzCGf62ZmLIMd3cQk2TaAAJ-EwACnQdoV6lN-23qPLHPOwQ"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

WELCOME_TEXT = """
WELCOME TO VIP TEHELKA

Aaj ka Daily Prediction Time :

10:00 AM — Session
12:00 PM — Session
03:00 PM — Session
05:00 PM — Session
07:00 PM — Session
09:00 PM — Session

Time par ready raho.
Jaldi se diposit karo or mota profit kamao 
deposit hamisa 2 k se Jada Karna 
REGISTER_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"
Koi problem ho to msg plz 
SUPPORT_LINK = "https://t.me/Next_level_user"
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("VIP CHANNEL", url=VIP_CHANNEL)],
        [InlineKeyboardButton("CONTACT SUPPORT", url=SUPPORT_LINK)]
    ]

    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def send_sticker(app, sticker):
    await app.bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=sticker
    )


async def send_text(app, text):
    await app.bot.send_message(
        chat_id=CHANNEL_ID,
        text=text
    )


async def morning_message(app):
    # Jaldi se diposit karo or mota profit kamao 
deposit hamisa 2 k se Jada Karna 
REGISTER_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"
Koi problem ho to msg plz 
SUPPORT_LINK = "https://t.me/Next_level_user".
    text = """
GOOD MORNING EVERYONE

VIP TEHELKA

Aaj ka Daily Routine:

10:00 AM — Session
12:00 PM — Session
03:00 PM — Session
05:00 PM — Session
07:00 PM — Session
09:00 PM — Session

Time par ready raho.
Jaldi se diposit karo or mota profit kamao 
deposit hamisa 2 k se Jada Karna 
REGISTER_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"
Koi problem ho to msg plz 
SUPPORT_LINK = "https://t.me/Next_level_user"
"""
    await send_text(app, text)


async def ready_message(app, session_time):
    text = f"""
GET READY

Sirf 30 Minutes Baaki!

{session_time} Session ke liye ready raho.

Time par online raho.
Latest updates check karte raho.
Jaldi se diposit karo or mota profit kamao 
deposit hamisa 2 k se Jada Karna 
REGISTER_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"
Koi problem ho to msg plz 
SUPPORT_LINK = "https://t.me/Next_level_user"
VIP TEHELKA
"""
    await send_text(app, text)


async def daily_routine_message(app, session_time): Jaldi se diposit karo or mota profit kamao 
deposit hamisa 2 k se Jada Karna 
REGISTER_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"
Koi problem ho to msg plz 
SUPPORT_LINK = "https://t.me/Next_level_user"
    text = f"""
DAILY ROUTINE UPDATE

Next Session — {session_time}

Ab next session ke liye ready raho.

Stay Connected.

VIP TEHELKA
"""
    await send_text(app, text)


async def final_message(app):
    # Apna final message yahan khud add kar sakte ho.
    text = """
TODAY'S SESSION IS COMPLETE
Jaldi se diposit karo or mota profit kamao 
deposit hamisa 2 k se Jada Karna 
REGISTER_LINK = "https://13lwin6.com/register?inviteCode=C6APK4N&from=web"
Koi problem ho to msg plz 
SUPPORT_LINK = "https://t.me/Next_level_user"
sare bande abhi ke liye withdrawal kar legne or agla prediction start hone se phle diposit kar lange 
VIP TEHELKA
"""
    await send_text(app, text)


def add_session_jobs(scheduler, app, hour, minute):
    """
    One 10-minute session:
    - 10 min before sticker
    - 2 min before sticker
    - 1 min before sticker
    - Running sequence
    - Extra stickers
    - End stickers
    """

    # 10 minutes before
    scheduler.add_job(
        send_sticker,
        "cron",
        hour=hour,
        minute=minute - 10,
        second=0,
        args=[app, STICKER_10MIN]
    )

    # 2 minutes before
    scheduler.add_job(
        send_sticker,
        "cron",
        hour=hour,
        minute=minute - 2,
        second=0,
        args=[app, STICKER_2MIN]
    )

    # 1 minute before
    scheduler.add_job(
        send_sticker,
        "cron",
        hour=hour,
        minute=minute - 1,
        second=0,
        args=[app, STICKER_1MIN]
    )

    # Session running: every minute for 10 minutes
    for i in range(10):
        current_minute = minute + i

        scheduler.add_job(
            send_sticker,
            "cron",
            hour=hour,
            minute=current_minute,
            second=5,
            args=[app, RUNNING_STICKER]
        )

        # Existing extra sticker pattern
        if i in (2, 5, 8):
            scheduler.add_job(
                send_sticker,
                "cron",
                hour=hour,
                minute=current_minute,
                second=20,
                args=[app, EXTRA_STICKER_1]
            )

        if i in (3, 6, 9):
            scheduler.add_job(
                send_sticker,
                "cron",
                hour=hour,
                minute=current_minute,
                second=25,
                args=[app, EXTRA_STICKER_2]
            )

    # Session ending stickers
    scheduler.add_job(
        send_sticker,
        "cron",
        hour=hour,
        minute=minute + 10,
        second=40,
        args=[app, END_STICKER_1]
    )

    scheduler.add_job(
        send_sticker,
        "cron",
        hour=hour,
        minute=minute + 10,
        second=50,
        args=[app, END_STICKER_2]
    )


def main():
    scheduler = AsyncIOScheduler(
        timezone=timezone("Asia/Kolkata")
    )

    async def post_init(application):
        scheduler.start()

        print("VIP TEHELKA BOT RUNNING")
        print("TIMEZONE: Asia/Kolkata")
        print("CHANNEL:", CHANNEL_ID)
        print("SCHEDULER STARTED")

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    # 8:00 AM
    scheduler.add_job(
        morning_message,
        "cron",
        hour=8,
        minute=0,
        second=0,
        args=[app]
    )

    # ==================================================
    # 6 SESSION TIMES
    # ==================================================

    sessions = [
        (10, 0, "10:00 AM"),
        (12, 0, "12:00 PM"),
        (15, 0, "03:00 PM"),
        (17, 0, "05:00 PM"),
        (19, 0, "07:00 PM"),
        (21, 0, "09:00 PM"),
    ]

    for hour, minute, display_time in sessions:

        # 30-minute reminder
        reminder_hour = hour
        reminder_minute = minute - 30

        if reminder_minute < 0:
            reminder_hour -= 1
            reminder_minute += 60

        scheduler.add_job(
            ready_message,
            "cron",
            hour=reminder_hour,
            minute=reminder_minute,
            second=0,
            args=[app, display_time]
        )

        # Existing 10/2/1 minute + session sticker sequence
        add_session_jobs(
            scheduler,
            app,
            hour,
            minute
        )

    # Daily routine/update messages
    # Existing routine timing pattern can be edited by you.
    routine_times = [
        (11, 0, "12:00 PM"),
        (14, 0, "03:00 PM"),
        (16, 0, "05:00 PM"),
        (18, 0, "07:00 PM"),
    ]

    for hour, minute, next_time in routine_times:
        scheduler.add_job(
            daily_routine_message,
            "cron",
            hour=hour,
            minute=minute,
            second=0,
            args=[app, next_time]
        )

    # Final message after 09:10 PM session
    scheduler.add_job(
        final_message,
        "cron",
        hour=21,
        minute=10,
        second=55,
        args=[app]
    )

    app.run_polling()


if __name__ == "__main__":
    main()
