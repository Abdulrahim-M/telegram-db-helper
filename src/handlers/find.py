from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from database.db import search_item
from utils.broadcaster import broadcast
from utils.fetch_message import get_message

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        m = get_message("find_command_text", update.message.chat.id)
        await update.message.reply_text(m)
        await broadcast("bot_sent", update.message.chat.id, m)
        return

    query = " ".join(context.args)
    results = search_item(query)

    if results:
        reply = "\n\n".join(
            [get_message("find_command_output", update.message.chat.id).format(*r)
             for r in results]
        )
    else:
        reply = get_message("find_command_notfound", update.message.chat.id)

    await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    await broadcast("bot_sent", update.message.chat.id, reply)
