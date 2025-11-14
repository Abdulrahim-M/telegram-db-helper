from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from utils.export import export_csv, export_pdf, export_txt, export_xlsx
from utils.broadcaster import broadcast
from utils.fetch_message import get_message

async def export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define your buttons (text + callback_data)
    keyboard = [
        [
            InlineKeyboardButton("csv file", callback_data='export_csv'),
            InlineKeyboardButton("xlsx file", callback_data='export_xlsx')
        ],
        [
            InlineKeyboardButton("text file", callback_data='export_txt'),
            InlineKeyboardButton("PDF file", callback_data='export_pdf')
        ],
    ]

    # Wrap buttons in an InlineKeyboardMarkup
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message with buttons
    await update.message.reply_text(get_message("export_text", update.message.chat.id), reply_markup=reply_markup)
    await broadcast("bot_sent", update.message.chat.id, "exporting")

async def export_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == 'export_csv':
        file_data = export_csv()
        file_type = "CSV"

    elif choice == 'export_xlsx':
        file_data = export_xlsx()
        file_type = "xlsx"

    elif choice == 'export_txt':
        file_data = export_txt()
        file_type = "txt"

    elif choice == 'export_pdf':
        file_data = export_pdf()
        file_type = "pdf"

    
    await query.message.reply_document(file_data, filename=f"export.{file_type}")
    await broadcast("bot_sent", query.message.chat.id, f"exported {file_type}")
