from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from utils.export import export_csv, export_pdf, export_txt, export_xlsx
from utils.broadcaster import broadcast

async def export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define your buttons (text + callback_data)
    keyboard = [
        [
            InlineKeyboardButton("csv file", callback_data='1'),
            InlineKeyboardButton("xlsx file", callback_data='2')
        ],
        [
            InlineKeyboardButton("text file", callback_data='3'),
            InlineKeyboardButton("PDF file", callback_data='4')
        ],
    ]

    # Wrap buttons in an InlineKeyboardMarkup
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message with buttons
    await update.message.reply_text("نوع الملف:", reply_markup=reply_markup)
    await broadcast("bot_sent", update.message.chat.id, "exporting")

async def export_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == '1':
        file_data = export_csv()
        file_type = "CSV"

    elif choice == '2':
        file_data = export_xlsx()
        file_type = "xlsx"

    elif choice == '3':
        file_data = export_txt()
        file_type = "txt"

    elif choice == '4':
        file_data = export_pdf()
        file_type = "pdf"

    
    await query.message.reply_document(file_data, filename=f"export.{file_type}")
    await broadcast("bot_sent", update.message.chat.id, f"exported {file_type}")
