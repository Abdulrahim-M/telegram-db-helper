from telegram import Update
from telegram.ext import ContextTypes

from database.user_logs_handler import log_message
from utils.broadcaster import broadcast
from telegram.constants import ParseMode

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = """
⚙️ تعليمات الاستخدام:

`/find`:
أدخل `\u200e/find` متبوعًا برقم الجلوس أو الرقم الجامعي للحصول على بيانات الطالب.

`/export`:
لاستخراج جميع البيانات في أحد الصيغ المتاحة.

`/template`:
لإنشاء رسالة بصيغة محددة، تعمل كقالب يمكن تطبيقه لاستخراج جميع البيانات.

"""
    await update.message.reply_text(m, parse_mode=ParseMode.MARKDOWN)
    await broadcast("bot_sent", update.message.chat.id, m)
