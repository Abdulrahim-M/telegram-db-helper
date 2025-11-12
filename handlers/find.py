from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from database.db import search_item
from utils.broadcaster import broadcast

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        m = "Usage: /find <name or Index or phone>"
        await update.message.reply_text(m)
        await broadcast("bot_sent", update.message.chat.id, m)
        return

    query = " ".join(context.args)
    results = search_item(query)

    if results:
        reply = "\n\n".join(
            [f"🧾 *Data:* \n*Name:* {r[0]}\n*Index:* {r[1]}\n*unId:* {r[2]}"
             f"\n*Email:* {r[3]}\n*Phone:* {r[4]}\n*Address:* {r[5]}"
             for r in results]
        )
    else:
        reply = "No matching entries found."

    await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    await broadcast("bot_sent", update.message.chat.id, parse_mode=ParseMode.MARKDOWN)
