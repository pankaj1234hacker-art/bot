import os
import json
import sqlite3
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger


# ============================================================
# CONFIG
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

OWNER_ID = 8475261276

CHANNEL_ID = os.getenv(
    "CHANNEL_ID",
    "@TEHELKA_VIP_KING"
).strip()

TIMEZONE = ZoneInfo("Asia/Kolkata")

DB_PATH = os.getenv(
    "BOT_DB",
    "bot_data.sqlite3"
)

VIP_CHANNEL = "https://t.me/TEHELKA_VIP_KING"

SUPPORT_LINK = "https://t.me/Next_level_user"


# ============================================================
# OLD STICKER IDs
# ============================================================

STICKER_10MIN = (
    "CAACAgUAAxkBAAIBP2oKn8i0a1JqoNAqRLTxvqcwJzoWAAIXEwACvmTQVn4hqlDaxy8AATsE"
)

STICKER_2MIN = (
    "CAACAgUAAyEFAATloOE5AAICAmoJ1-y3HvygDNQQukQL63uJdoOnAAKFEQACflHJVvhHK40SVtJHOwQ"
)

STICKER_1MIN = (
    "CAACAgUAAxkBAAIBSWoKopjKbEtd9eRIFwxok8JzHV4FAALSEAACt-6xVytut0bPId8JOwQ"
)

RUNNING_STICKER = (
    "CAACAgUAAyEFAATloOE5AAIB9WoJ02vKgrKJ85e-5vvj5CytikTsAAIiEgACUUDJVkSsO8zj-5OwQ"
)

EXTRA_STICKER_1 = (
    "CAACAgUAAyEFAATloOE5AAIB6GoJ0iO50gAB2ZmmjkaahT3EJ9t7ygACahIAAvYiyVZikUGUoRZynzsE"
)

EXTRA_STICKER_2 = (
    "CAACAgUAAyEFAATloOE5AAICBWoJ2CqnDBifKRuJWOsCrtKxtgvQAAIXFwACvDMZV1AUT-rGMRluOwQ"
)

END_STICKER_1 = (
    "CAACAgUAAxkBAAIBUWoKo0uIfCGeV5GfZU0Fv_hYOe8HAALYEQACMazJVuD7AUjcPT_gOwQ"
)

END_STICKER_2 = (
    "CAACAgUAAxkBAAIBU2oKo39yvzCGf62ZmLIMd3cQk2TaAAJ-EwACnQdoV6lN-23qPLHPOwQ"
)


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

log = logging.getLogger(__name__)


# ============================================================
# DATABASE
# ============================================================

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def now_iso():
    return datetime.now(TIMEZONE).isoformat(timespec="seconds")


def init_db():

    conn = db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            user_id INTEGER PRIMARY KEY,
            added_by INTEGER NOT NULL,
            added_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            kind TEXT NOT NULL,
            content_type TEXT NOT NULL DEFAULT 'text',
            content TEXT,
            file_id TEXT,
            buttons_json TEXT,
            schedule_json TEXT,
            enabled INTEGER NOT NULL DEFAULT 1,
            created_by INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hour INTEGER NOT NULL,
            minute INTEGER NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER,
            action TEXT NOT NULL,
            detail TEXT,
            user_id INTEGER,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            joined_at TEXT NOT NULL,
            blocked INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Owner automatically becomes Full Admin
    cur.execute(
        """
        INSERT OR IGNORE INTO admins
        (user_id, added_by, added_at)
        VALUES (?, ?, ?)
        """,
        (
            OWNER_ID,
            OWNER_ID,
            now_iso()
        )
    )

    # Default sessions
    default_sessions = [
        ("Session 1", 10, 0),
        ("Session 2", 12, 0),
        ("Session 3", 15, 0),
        ("Session 4", 17, 0),
        ("Session 5", 19, 0),
        ("Session 6", 21, 0),
    ]

    for name, hour, minute in default_sessions:

        cur.execute(
            """
            SELECT id
            FROM sessions
            WHERE hour=? AND minute=?
            """,
            (hour, minute)
        )

        if not cur.fetchone():

            cur.execute(
                """
                INSERT INTO sessions
                (name, hour, minute)
                VALUES (?, ?, ?)
                """,
                (name, hour, minute)
            )

    conn.commit()
    conn.close()


# ============================================================
# ADMIN CHECK
# ============================================================

def is_admin(user_id: int):

    if user_id == OWNER_ID:
        return True

    conn = db()

    row = conn.execute(
        """
        SELECT 1
        FROM admins
        WHERE user_id=?
        """,
        (user_id,)
    ).fetchone()

    conn.close()

    return bool(row)


def log_action(
    action,
    detail="",
    user_id=None,
    message_id=None
):

    conn = db()

    conn.execute(
        """
        INSERT INTO logs
        (message_id, action, detail, user_id, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            message_id,
            action,
            detail,
            user_id,
            now_iso()
        )
    )

    conn.commit()
    conn.close()


# ============================================================
# BUTTON HELPERS
# ============================================================

def parse_buttons(raw):

    result = []

    if not raw:
        return result

    for line in raw.splitlines():

        if "|" not in line:
            continue

        text, url = line.split("|", 1)

        text = text.strip()
        url = url.strip()

        if not text:
            continue

        if not url.startswith(
            (
                "http://",
                "https://",
                "tg://"
            )
        ):
            continue

        result.append([
            text,
            url
        ])

    return result


def markup_from_json(raw):

    if not raw:
        return None

    try:

        buttons = json.loads(raw)

        rows = []

        for row in buttons:

            rows.append([
                InlineKeyboardButton(
                    str(button[0]),
                    url=str(button[1])
                )
                for button in row
            ])

        if not rows:
            return None

        return InlineKeyboardMarkup(rows)

    except Exception:

        return None


# ============================================================
# SEND PAYLOAD
# ============================================================

async def send_payload(
    bot,
    chat_id,
    content_type,
    content,
    file_id,
    buttons_json=None
):

    markup = markup_from_json(buttons_json)

    if content_type == "text":

        return await bot.send_message(
            chat_id=chat_id,
            text=content or "",
            reply_markup=markup
        )

    if content_type == "photo":

        return await bot.send_photo(
            chat_id=chat_id,
            photo=file_id,
            caption=content or "",
            reply_markup=markup
        )

    if content_type == "video":

        return await bot.send_video(
            chat_id=chat_id,
            video=file_id,
            caption=content or "",
            reply_markup=markup
        )

    if content_type == "document":

        return await bot.send_document(
            chat_id=chat_id,
            document=file_id,
            caption=content or "",
            reply_markup=markup
        )

    if content_type == "sticker":

        return await bot.send_sticker(
            chat_id=chat_id,
            sticker=file_id,
            reply_markup=markup
        )

    return await bot.send_message(
        chat_id=chat_id,
        text=content or "",
        reply_markup=markup
    )


# ============================================================
# BROADCAST
# ============================================================

async def broadcast_message(bot, row):

    conn = db()

    users = conn.execute(
        """
        SELECT user_id
        FROM subscribers
        WHERE blocked=0
        """
    ).fetchall()

    conn.close()

    sent = 0
    failed = 0

    for user in users:

        try:

            await send_payload(
                bot,
                user["user_id"],
                row["content_type"],
                row["content"],
                row["file_id"],
                row["buttons_json"]
            )

            sent += 1

        except Exception as exc:

            failed += 1

            if "blocked" in str(exc).lower():

                conn = db()

                conn.execute(
                    """
                    UPDATE subscribers
                    SET blocked=1
                    WHERE user_id=?
                    """,
                    (user["user_id"],)
                )

                conn.commit()
                conn.close()

    return sent, failed


# ============================================================
# SCHEDULER
# ============================================================

scheduler = AsyncIOScheduler(
    timezone=TIMEZONE
)

JOB_PREFIX = "dbmsg:"


def remove_message_jobs(message_id):

    prefix = f"{JOB_PREFIX}{message_id}:"

    for job in list(scheduler.get_jobs()):

        if job.id.startswith(prefix):

            try:
                scheduler.remove_job(job.id)

            except Exception:
                pass


def add_db_message_jobs(app, row):

    remove_message_jobs(row["id"])

    if not row["enabled"]:
        return

    try:

        schedule = json.loads(
            row["schedule_json"] or "{}"
        )

    except Exception:

        schedule = {}

    kind = row["kind"]

    # Quick send doesn't need a scheduler job
    if kind == "quick":
        return

    # One-time schedule
    if kind == "one_time":

        try:

            dt = datetime.fromisoformat(
                schedule["datetime"]
            ).astimezone(TIMEZONE)

        except Exception:

            return

        if dt > datetime.now(TIMEZONE):

            scheduler.add_job(
                send_db_message_job,
                DateTrigger(
                    run_date=dt
                ),
                id=f"{JOB_PREFIX}{row['id']}:once",
                replace_existing=True,
                args=[
                    app,
                    row["id"]
                ]
            )

        return

    # Recurring schedule
    times = schedule.get(
        "times",
        []
    )

    days = schedule.get(
        "days",
        [
            "mon",
            "tue",
            "wed",
            "thu",
            "fri",
            "sat",
            "sun"
        ]
    )

    if not times:
        return

    day_expr = ",".join(days)

    for index, time_value in enumerate(times):

        try:

            hour, minute = map(
                int,
                time_value.split(":")
            )

        except Exception:

            continue

        scheduler.add_job(
            send_db_message_job,
            CronTrigger(
                day_of_week=day_expr,
                hour=hour,
                minute=minute,
                timezone=TIMEZONE
            ),
            id=f"{JOB_PREFIX}{row['id']}:{index}",
            replace_existing=True,
            args=[
                app,
                row["id"]
            ]
        )


async def send_db_message_job(
    app,
    message_id
):

    conn = db()

    row = conn.execute(
        """
        SELECT *
        FROM messages
        WHERE id=?
        """,
        (message_id,)
    ).fetchone()

    conn.close()

    if not row:
        return

    if not row["enabled"]:
        return

    try:

        schedule = json.loads(
            row["schedule_json"] or "{}"
        )

        # Broadcast to bot subscribers
        if schedule.get(
            "broadcast",
            False
        ):

            sent, failed = await broadcast_message(
                app.bot,
                row
            )

            log_action(
                "sent",
                f"broadcast sent={sent} failed={failed}",
                message_id=message_id
            )

        else:

            await send_payload(
                app.bot,
                CHANNEL_ID,
                row["content_type"],
                row["content"],
                row["file_id"],
                row["buttons_json"]
            )

            log_action(
                "sent",
                "channel",
                message_id=message_id
            )

    except Exception as exc:

        log.exception(
            "Scheduled send failed: %s",
            exc
        )

        log_action(
            "error",
            str(exc),
            message_id=message_id
        )


# ============================================================
# CHANNEL HELPERS
# ============================================================

async def channel_text(
    app,
    text
):

    await app.bot.send_message(
        chat_id=CHANNEL_ID,
        text=text
    )


async def channel_sticker(
    app,
    sticker
):

    await app.bot.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=sticker
    )


async def session_sticker_job(
    app,
    sticker
):

    try:

        await channel_sticker(
            app,
            sticker
        )

    except Exception:

        log.exception(
            "Sticker send failed"
        )


async def session_text_job(
    app,
    text
):

    try:

        await channel_text(
            app,
            text
        )

    except Exception:

        log.exception(
            "Session text failed"
        )


# ============================================================
# SESSION AUTOMATIC SYSTEM
# ============================================================

def add_session_jobs(
    app,
    hour,
    minute,
    name
):

    base = (
        hour * 60
        + minute
    )

    # --------------------------------------------------------
    # 30 MINUTES BEFORE
    # --------------------------------------------------------

    reminder_total = base - 30

    reminder_total %= (
        24 * 60
    )

    reminder_hour, reminder_minute = divmod(
        reminder_total,
        60
    )

    scheduler.add_job(
        session_text_job,
        CronTrigger(
            hour=reminder_hour,
            minute=reminder_minute,
            timezone=TIMEZONE
        ),
        id=f"session:{hour:02d}{minute:02d}:r30",
        replace_existing=True,
        args=[
            app,
            f"GET READY\n\n30 minutes left for {name}."
        ]
    )

    # --------------------------------------------------------
    # 10 MINUTES BEFORE
    # --------------------------------------------------------

    total = (
        base - 10
    ) % (
        24 * 60
    )

    hh, mm = divmod(
        total,
        60
    )

    scheduler.add_job(
        session_sticker_job,
        CronTrigger(
            hour=hh,
            minute=mm,
            timezone=TIMEZONE
        ),
        id=f"session:{hour:02d}{minute:02d}:s10",
        replace_existing=True,
        args=[
            app,
            STICKER_10MIN
        ]
    )

    # --------------------------------------------------------
    # 2 MINUTES BEFORE
    # --------------------------------------------------------

    total = (
        base - 2
    ) % (
        24 * 60
    )

    hh, mm = divmod(
        total,
        60
    )

    scheduler.add_job(
        session_sticker_job,
        CronTrigger(
            hour=hh,
            minute=mm,
            timezone=TIMEZONE
        ),
        id=f"session:{hour:02d}{minute:02d}:s2",
        replace_existing=True,
        args=[
            app,
            STICKER_2MIN
        ]
    )

    # --------------------------------------------------------
    # 1 MINUTE BEFORE
    # --------------------------------------------------------

    total = (
        base - 1
    ) % (
        24 * 60
    )

    hh, mm = divmod(
        total,
        60
    )

    scheduler.add_job(
        session_sticker_job,
        CronTrigger(
            hour=hh,
            minute=mm,
            timezone=TIMEZONE
        ),
        id=f"session:{hour:02d}{minute:02d}:s1",
        replace_existing=True,
        args=[
            app,
            STICKER_1MIN
        ]
    )

    # --------------------------------------------------------
    # RUNNING STICKER
    # 10 minutes
    # --------------------------------------------------------

    for i in range(10):

        total = (
            base + i
        ) % (
            24 * 60
        )

        hh, mm = divmod(
            total,
            60
        )

        scheduler.add_job(
            session_sticker_job,
            CronTrigger(
                hour=hh,
                minute=mm,
                second=5,
                timezone=TIMEZONE
            ),
            id=f"session:{hour:02d}{minute:02d}:run{i}",
            replace_existing=True,
            args=[
                app,
                RUNNING_STICKER
            ]
        )

        # Extra sticker 1
        if i in (
            2,
            5,
            8
        ):

            scheduler.add_job(
                session_sticker_job,
                CronTrigger(
                    hour=hh,
                    minute=mm,
                    second=20,
                    timezone=TIMEZONE
                ),
                id=f"session:{hour:02d}{minute:02d}:x1{i}",
                replace_existing=True,
                args=[
                    app,
                    EXTRA_STICKER_1
                ]
            )

        # Extra sticker 2
        if i in (
            3,
            6,
            9
        ):

            scheduler.add_job(
                session_sticker_job,
                CronTrigger(
                    hour=hh,
                    minute=mm,
                    second=25,
                    timezone=TIMEZONE
                ),
                id=f"session:{hour:02d}{minute:02d}:x2{i}",
                replace_existing=True,
                args=[
                    app,
                    EXTRA_STICKER_2
                ]
            )

    # --------------------------------------------------------
    # END STICKERS
    # --------------------------------------------------------

    total = (
        base + 10
    ) % (
        24 * 60
    )

    hh, mm = divmod(
        total,
        60
    )

    scheduler.add_job(
        session_sticker_job,
        CronTrigger(
            hour=hh,
            minute=mm,
            second=40,
            timezone=TIMEZONE
        ),
        id=f"session:{hour:02d}{minute:02d}:end1",
        replace_existing=True,
        args=[
            app,
            END_STICKER_1
        ]
    )

    scheduler.add_job(
        session_sticker_job,
        CronTrigger(
            hour=hh,
            minute=mm,
            second=50,
            timezone=TIMEZONE
        ),
        id=f"session:{hour:02d}{minute:02d}:end2"
            )
