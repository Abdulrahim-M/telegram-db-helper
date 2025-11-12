from io import BytesIO
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from telegram.constants import ParseMode
from database.db import all_items
from utils.broadcaster import broadcast
from utils.text_replace import replace_data

ASKING = 1

async def template_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = """أكتب الصيغة التي تريد استخراج البيانات فيها بإستخدام:
• `$name$`    => name
• `$index$`   => Index
• `$unid$`    => university ID
• `$email$`   => Email
• `$phone$`   => Phone number
• `$address$` => Address
"""
    keyboard = [[InlineKeyboardButton("Cancel", callback_data='cancel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(m,parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

    await broadcast("bot_sent", update.message.chat.id, m)
    return ASKING

async def replace_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    data = all_items()
    num = 1
    result = ""

    for r in data:
        text = replace_data(user_input, r)
        result += f"\n\n{num}. " + text
        num += 1

    file = BytesIO(result.encode("utf-8"))
    file.name = "data.txt"

    await update.message.reply_document(document=file)
    await broadcast("bot_sent", update.message.chat.id, file.name)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data != "cancel":
        return
    
    await query.message.edit_text("Cancelled.")
    await broadcast("bot_sent", query.message.chat.id, "Cancelled.")
    return ConversationHandler.END

def get_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('template', template_all)],
        states={ASKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, replace_all)]},
        fallbacks=[CallbackQueryHandler(cancel)]
    )
