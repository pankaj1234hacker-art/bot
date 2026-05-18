from telegram.ext import Updater, MessageHandler, Filters

TOKEN = "8775211756:AAFWtG1PNM393_nPcAchCNaDuEKIilhjGGg"

# ===================================
# GET STICKER FILE ID
# ===================================

def get_sticker(update, context):

    sticker = update.message.sticker

    if sticker:

        file_id = sticker.file_id

        update.message.reply_text(
            text=f"✅ STICKER FILE ID:\n\n{file_id}"
        )

# ===================================
# MAIN
# ===================================

updater = Updater(TOKEN, use_context=True)

dp = updater.dispatcher

dp.add_handler(
    MessageHandler(
        Filters.sticker,
        get_sticker
    )
)

print("BOT STARTED")

updater.start_polling()

updater.idle()
