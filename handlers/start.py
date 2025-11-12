from telegram import Update
from telegram.ext import ContextTypes

from database.user_logs_handler import log_message
from utils.broadcaster import broadcast
from telegram.constants import ParseMode

from utils.fetch_message import get_message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = get_message("start_message", update.message.chat.id)
    await update.message.reply_text(m, parse_mode=ParseMode.MARKDOWN)
    await broadcast("bot_sent", update.message.chat.id, m)
