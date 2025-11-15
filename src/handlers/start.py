from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters

from services.selector import DB
from services.user_logs_handler import log_message
from utils.broadcaster import broadcast
from telegram.constants import ParseMode

from utils.fetch_message import get_message

ASK_ID = 1
ASKING = 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = get_message("start_message", update.message.chat.id)
    await update.message.reply_text(m, parse_mode=ParseMode.MARKDOWN)
    await broadcast("bot_sent", update.message.chat.id, m)

    await update.message.reply_text(get_message("start_ask_index", update.message.chat.id))
    return ASK_ID

async def receive_id(update, context):
    index = update.message.text.strip()
    record = DB().search_item(index).as_dict().pop(0)
    print(record)

    if record:
        context.user_data["record"] = record
        context.user_data["updated"] = False
        await ask_next_field(update, context)
        return ASKING
    else:
        await update.message.reply_text(get_message("start_index_not_found", update.message.chat.id))
        return ASK_ID


async def ask_next_field(update, context):
    record = context.user_data["record"]
    print(record)


    for key, value in record.items():
        if value is None: # and key != "address": //////////////////////////////////////////////////////////////////////////
            context.user_data["current_field"] = key
            field = key.replace("_", " ").title()
            await update.message.reply_text(get_message("start_ask_loop", update.message.chat.id).format(field))
            context.user_data["updated"] = True
            return ASKING

    new_record = record

    if new_record:
        reply = "\n\n".join(
            [get_message("find_command_output", update.message.chat.id).format(*r)
             for r in [new_record.values()]]
        )
        if context.user_data["updated"]:
            await update.message.reply_text(get_message("start_finish", update.message.chat.id), parse_mode=ParseMode.MARKDOWN)
            await broadcast("bot_sent", update.message.chat.id, "Data Saved!")
        elif not context.user_data["updated"]:
            await update.message.reply_text(get_message("start_finish_old", update.message.chat.id), parse_mode=ParseMode.MARKDOWN)
            await broadcast("bot_sent", update.message.chat.id, "Data already saved!")
    else:
        reply = get_message("find_command_notfound", update.message.chat.id)

    DB().update_row(new_record, {"index_id": new_record.get("index_id")})

    await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    await broadcast("bot_sent", update.message.chat.id, reply)
    return ConversationHandler.END

async def receive_field(update, context):
    field = context.user_data["current_field"]
    value = update.message.text.strip()

    # save user answer
    context.user_data["record"][field] = value

    # ask next missing field
    return await ask_next_field(update, context)

def start_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('start', start)],
            states={
                ASK_ID: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, receive_id)
                ],
                ASKING: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, receive_field)
                ]
            },
        fallbacks=[]
    )
