import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from database.bot_logs_handler import log_outgoing_message
from handlers.lang_selector import language_selector, language_callback
from handlers.start import start
from handlers.find import find
from handlers.export import export, export_file, CallbackQueryHandler
from handlers.template import get_conv_handler
from database.user_logs_handler import log_message
from config import BOT_TOKEN
from utils.broadcaster import subscribe
from utils.load_locales import load_locales

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register listener
subscribe("bot_sent", log_outgoing_message)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    load_locales()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("find", find))
    app.add_handler(CommandHandler("select_language", language_selector))
    app.add_handler(get_conv_handler())
    app.add_handler(CommandHandler("export", export))

    app.add_handler(CallbackQueryHandler(language_callback, pattern=r"^lang_"))
    app.add_handler(CallbackQueryHandler(export_file, pattern=r"^export_"))

    app.add_handler(MessageHandler(filters.ALL, log_message))

    app.run_polling()

if __name__ == "__main__":
    main()
