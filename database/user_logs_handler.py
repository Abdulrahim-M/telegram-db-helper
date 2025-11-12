
import sqlite3
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import ContextTypes

conn = sqlite3.connect("data/data.db", check_same_thread=False)
cursor = conn.cursor()

async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return  # Ignore non-message updates (like button clicks)

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.username
    reply_to = update.message.reply_to_message.message_id if update.message.reply_to_message else None
    forwarded_from = None

    if getattr(update.message, "forward_from", None):
        forwarded_from = update.message.forward_from.id
    elif getattr(update.message, "forward_from_chat", None):
        forwarded_from = update.message.forward_from_chat.id

    if update.message.text:
        msg_type = "text"
        message_content = update.message.text
    elif update.message.photo:
        msg_type = "photo"
        message_content = f"[Photo ID: {update.message.photo[-1].file_id}]"
    elif update.message.sticker:
        msg_type = "sticker"
        message_content = f"[Sticker ID: {update.message.sticker.file_id}]"
    elif update.message.voice:
        msg_type = "voice"
        message_content = f"[Voice ID: {update.message.voice.file_id}]"
    elif update.message.document:
        msg_type = "document"
        message_content = f"[Document ID: {update.message.document.file_id}]"
    else:
        msg_type = "other"
        message_content = "[Unsupported type]"

    cursor.execute("""
    INSERT INTO chat_logs (chat_id, user_id, username, message, type, timestamp, reply_to, forwarded_from)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        chat_id,
        user_id,
        username,
        message_content,
        msg_type,
        datetime.now(timezone.utc).isoformat(),
        reply_to,
        forwarded_from,
    ))
    conn.commit()

