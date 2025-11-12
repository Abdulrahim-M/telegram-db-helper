from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler

from utils.broadcaster import broadcast
from utils.fetch_message import USER_LANG, get_message
from utils.load_locales import LOCALES

async def language_selector(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton(text=lang.upper(), callback_data=f"lang_{lang}")]
        for lang in LOCALES.keys()
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Select your language:", reply_markup=reply_markup)
    await broadcast("bot_sent", update.message.chat.id, "Select your language:")



async def language_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data  # e.g., 'lang_en'
    lang_code = data.split("_")[1]
    
    # Save language preference (for example, in memory)
    user_id = query.from_user.id
    USER_LANG[user_id] = lang_code
    
    m = get_message("start_message", query.message.chat.id)
    await query.edit_message_text(m)
    await broadcast("bot_sent", query.message.chat.id, m)
    return ConversationHandler.END
