import logging
from telegram.ext import CallbackContext, ConversationHandler
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup

updater = Updater(token='908551265:AAELjDonWh-hJNpcCFp_gx6ctlEKwdRaty4', use_context=True)
job = updater.job_queue
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

FIRST, SECOND, THIRD, FOURTH = range(4)

def start(update, context):
    update.message.reply_text("Welcome to my awesome bot!")

def echo(update, context):
    message = 'You enter this Area: {}'.format(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    context.bot.send_message(chat_id=update.effective_chat.id, text='The price of your property is: COP 357238901 Aprox')

def caps(update, context):
    print (update.callback_query)
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def type_rs(update, context):
    lang_1 = InlineKeyboardButton(text="House \U0001F3D8", callback_data="House")
    lang_2 = InlineKeyboardButton(text="Apartment \U0001F3EC", callback_data="Apartment")
    #lang_3 = InlineKeyboardButton(text="Nederlands \U0001F1F3\U0001F1F1", callback_data="ch_lang_nl")

    #lang_keyboard = InlineKeyboardMarkup([[lang_1, lang_2], [lang_3]])
    lang_keyboard = InlineKeyboardMarkup([[lang_1, lang_2]])

    context.bot.send_message(chat_id=update.effective_chat.id, text='What type of property do you have?',
                reply_markup=lang_keyboard)

    return FIRST

def stratum(update, context):
    query = update.callback_query
    query.edit_message_text(text="You selected type: {}".format(query.data))
    lang_1 = InlineKeyboardButton(text="One \U00000031\U000020E3", callback_data='One')
    lang_2 = InlineKeyboardButton(text="Two \U00000032\U000020E3", callback_data="Two")
    lang_3 = InlineKeyboardButton(text="Three \U00000033\U000020E3", callback_data="Three")
    lang_4 = InlineKeyboardButton(text="Four \U00000034\U000020E3", callback_data="Four")
    lang_5 = InlineKeyboardButton(text="Five \U00000035\U000020E3", callback_data="Five")
    lang_6 = InlineKeyboardButton(text="Six \U00000036\U000020E3", callback_data="Six")

    lang_keyboard = InlineKeyboardMarkup([[lang_1, lang_2],[lang_3, lang_4],[lang_5, lang_6]])

    context.bot.send_message(chat_id=update.effective_chat.id, text='What stratum do you have?',
                reply_markup=lang_keyboard)

    return SECOND

"""def button2(update, context):
    query = update.callback_query
    query.edit_message_text(text="You selected stratum: {}".format(query.data))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Pitu la manzanita')"""

def rooms(update, context):
    query = update.callback_query
    query.edit_message_text(text="You selected stratum: {}".format(query.data))
    lang_1 = InlineKeyboardButton(text="One \U00000031\U000020E3", callback_data='One')
    lang_2 = InlineKeyboardButton(text="Two \U00000032\U000020E3", callback_data="Two")
    lang_3 = InlineKeyboardButton(text="Three \U00000033\U000020E3", callback_data="Three")
    lang_4 = InlineKeyboardButton(text="Four \U00000034\U000020E3", callback_data="Four")

    lang_keyboard = InlineKeyboardMarkup([[lang_1, lang_2],[lang_3, lang_4]])

    context.bot.send_message(chat_id=update.effective_chat.id, text='How many rooms do you have? ',
                reply_markup=lang_keyboard)

    return THIRD

def bathrooms(update, context):
    query = update.callback_query
    query.edit_message_text(text="You selected {} rooms".format(query.data))
    lang_1 = InlineKeyboardButton(text="One \U00000031\U000020E3", callback_data='One')
    lang_2 = InlineKeyboardButton(text="Two \U00000032\U000020E3", callback_data="Two")
    lang_3 = InlineKeyboardButton(text="Three \U00000033\U000020E3", callback_data="Three")
    lang_4 = InlineKeyboardButton(text="Four \U00000034\U000020E3", callback_data="Four")

    lang_keyboard = InlineKeyboardMarkup([[lang_1, lang_2],[lang_3, lang_4]])

    context.bot.send_message(chat_id=update.effective_chat.id, text='How many bathrooms do you have?',
                reply_markup=lang_keyboard)

    return FOURTH

def area(update, context):
    query = update.callback_query
    query.edit_message_text(text="You selected {} bathrooms".format(query.data))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Enter the Area Please')

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps)
find_handler = ConversationHandler(
        entry_points=[CommandHandler('find', type_rs)],
        states={
            FIRST: [CallbackQueryHandler(stratum, pattern=r'\D')],
            SECOND: [CallbackQueryHandler(rooms, pattern=r'\D')],
            THIRD: [CallbackQueryHandler(bathrooms, pattern=r'\D')],
            FOURTH: [CallbackQueryHandler(area, pattern=r'\D')]
        },
        fallbacks=[CommandHandler('find', type_rs)]
    )
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(find_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling()