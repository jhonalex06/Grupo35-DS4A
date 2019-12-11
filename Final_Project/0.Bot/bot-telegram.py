import logging
import json
import pandas as pd
import numpy as np
import requests

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

ZERO, FIRST, SECOND, THIRD, FOURTH, FIFTH, SIXTH, SEVEN = range(8)
prediction = {}

df = pd.read_csv('data_to_train.zip')

def transfor(dato):
    if dato == 'One':
        return 1
    if dato == 'Two':
        return 2
    if dato == 'Three':
        return 3
    if dato == 'Four':
        return 4
    if dato == 'Five':
        return 5
    if dato == 'Six':
        return 6
    

def start(update, context):
    update.message.reply_text("Welcome to my awesome bot!")

def echo(update, context):
    context.user_data['area'] = update.message.text
    print (context.user_data.keys())
    print (context.user_data['area'])
    message = 'You enter this Area: {}'.format(update.message.text)

    estrato = transfor(context.user_data['estrato'])
    zona = context.user_data['zona']
    area = float(context.user_data['area'])
    banos = transfor(context.user_data['rooms'])
    hab = transfor(context.user_data['bathrooms'])
    garajes = transfor(context.user_data['garages'])
    countah = 0
    countcp = 0
    countms = 0
    piso_int = 1
    lat = context.user_data['lat']
    long = context.user_data['long']
    tip_inmu = context.user_data['tipo']
    loc = context.user_data['localidad']

    param = {
    'estrato':[estrato], 
    'zona':[zona], 
    'log_area':[np.log(area)],
    'numero_habitaciones':[hab], 
    'num_banos':[banos], 
    'num_garages':[garajes], 
    'Count_loc_AlojamientoHospedaje':[countah], 
    'Count_loc_CicloParqueadero':[countcp], 
    'Count_loc_Museos':[countms],
    'piso_interior':[piso_int],
    'latitude':[lat],
    'longitude':[long],
    'tipo_inmueble':[tip_inmu],
    'Locnombre':[loc]}

    URL2 = 'http://3.17.210.131:8000/datos_compuestos/'
    r = requests.post(url = URL2, json = param)
    print (r.json())
    result = r.json()

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    context.bot.send_message(chat_id=update.effective_chat.id, text='The price of your property is: COP {} Aprox'.format(result[0]['Predicción'][0]))

def caps(update, context):
    print (update.callback_query)
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def type_rs(update, context):

    names = df['zona'].unique() 
    lan = []
    lan_group = []
    count = 0

    for i in names:
        lan.append(InlineKeyboardButton(text=i, callback_data=i))
        count = count + 1
        if count == 2:
            lan_group.append(lan)
            lan = []
            count = 0

    lang_keyboard = InlineKeyboardMarkup(lan_group)

    context.bot.send_message(chat_id=update.effective_chat.id, text='Where do you want your new house?',
                reply_markup=lang_keyboard)

    return ZERO

def zone(update, context):
    query = update.callback_query
    query.edit_message_text(text="You selected type: {}".format(query.data))
    context.user_data['zona'] = query.data

    names = df[df['zona'] == '{}'.format(query.data)]['LocNombre'].unique() 
    lan = []
    lan_group = []
    count = 0

    for i in names:
        lan.append(InlineKeyboardButton(text=i, callback_data=i))
        count = count + 1
        if count == 2:
            lan_group.append(lan)
            lan = []
            count = 0

    lang_keyboard = InlineKeyboardMarkup(lan_group)

    context.bot.send_message(chat_id=update.effective_chat.id, text='Where do you want your new house?',
                reply_markup=lang_keyboard)

    return FIRST

def stratum(update, context):
    query = update.callback_query
    query.edit_message_text(text="You selected type: {}".format(query.data))
    context.user_data['localidad'] = query.data


    names = df[df['LocNombre'] == '{}'.format(query.data)]['sector_catastral'].unique() 

    lan = []
    lan_group = []
    count = 0

    for i in names:
        lan.append(InlineKeyboardButton(text=i, callback_data=i))
        count = count + 1
        if count == 2:
            lan_group.append(lan)
            lan = []
            count = 0

    lang_keyboard = InlineKeyboardMarkup(lan_group)

    context.bot.send_message(chat_id=update.effective_chat.id, text='What localities do you have?',
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

    with open('All_loc_geo.json') as f:
        geojson = json.loads(f.read())

    sectors = '{}'.format(query.data)

    lon = ''
    lat = ''

    for i in geojson['features']:
        if i['properties']['SCaNombre'] == sectors.upper():
            lon = i['geometry']['coordinates'][0][0][0][0]
            lat = i['geometry']['coordinates'][0][0][0][1]

    print (lon)
    print (lat)

    context.user_data['long'] = query.data
    context.user_data['lat'] = query.data

    return THIRD

def bathrooms(update, context):
    query = update.callback_query
    query.edit_message_text(text="You selected {} rooms".format(query.data))
    context.user_data['rooms'] = query.data
    lang_1 = InlineKeyboardButton(text="One \U00000031\U000020E3", callback_data='One')
    lang_2 = InlineKeyboardButton(text="Two \U00000032\U000020E3", callback_data="Two")
    lang_3 = InlineKeyboardButton(text="Three \U00000033\U000020E3", callback_data="Three")
    lang_4 = InlineKeyboardButton(text="Four \U00000034\U000020E3", callback_data="Four")

    lang_keyboard = InlineKeyboardMarkup([[lang_1, lang_2],[lang_3, lang_4]])

    context.bot.send_message(chat_id=update.effective_chat.id, text='How many bathrooms do you have?',
                reply_markup=lang_keyboard)

    return FOURTH

def garages(update, context):
    query = update.callback_query
    query.edit_message_text(text="You selected {} bathrooms".format(query.data))
    context.user_data['bathrooms'] = query.data
    lang_1 = InlineKeyboardButton(text="One \U00000031\U000020E3", callback_data='One')
    lang_2 = InlineKeyboardButton(text="Two \U00000032\U000020E3", callback_data="Two")
    lang_3 = InlineKeyboardButton(text="Three \U00000033\U000020E3", callback_data="Three")
    lang_4 = InlineKeyboardButton(text="Four \U00000034\U000020E3", callback_data="Four")

    lang_keyboard = InlineKeyboardMarkup([[lang_1, lang_2],[lang_3, lang_4]])

    context.bot.send_message(chat_id=update.effective_chat.id, text='How many garages do you have?',
                reply_markup=lang_keyboard)

    return FIFTH

def estrato(update, context):
    query = update.callback_query
    query.edit_message_text(text="You selected {} garages".format(query.data))
    context.user_data['garages'] = query.data
    lang_1 = InlineKeyboardButton(text="One \U00000031\U000020E3", callback_data='One')
    lang_2 = InlineKeyboardButton(text="Two \U00000032\U000020E3", callback_data="Two")
    lang_3 = InlineKeyboardButton(text="Three \U00000033\U000020E3", callback_data="Three")
    lang_4 = InlineKeyboardButton(text="Four \U00000034\U000020E3", callback_data="Four")
    lang_5 = InlineKeyboardButton(text="Five \U00000033\U000020E3", callback_data="Five")
    lang_6 = InlineKeyboardButton(text="Six \U00000034\U000020E3", callback_data="Six")

    lang_keyboard = InlineKeyboardMarkup([[lang_1, lang_2],[lang_3, lang_4],[lang_5, lang_6]])

    context.bot.send_message(chat_id=update.effective_chat.id, text='How many stratums do you have?',
                reply_markup=lang_keyboard)

    return SIXTH

def tipo(update, context):
    query = update.callback_query
    query.edit_message_text(text="You selected {} stratum".format(query.data))
    context.user_data['estrato'] = query.data
    names = df['tipo_inmueble'].unique() 
    lan = []
    lan_group = []
    count = 0

    for i in names:
        lan.append(InlineKeyboardButton(text=i, callback_data=i))
        count = count + 1
        if count == 2:
            lan_group.append(lan)
            lan = []
            count = 0

    lang_keyboard = InlineKeyboardMarkup(lan_group)

    context.bot.send_message(chat_id=update.effective_chat.id, text='What type of house do you want?',
                reply_markup=lang_keyboard)

    return SEVEN

def area(update, context):
    query = update.callback_query
    context.user_data['tipo'] = query.data
    query.edit_message_text(text="You selected {} bathrooms".format(query.data))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Enter the Area Please')

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps)
find_handler = ConversationHandler(
        entry_points=[CommandHandler('find', type_rs)],
        states={
            ZERO: [CallbackQueryHandler(zone, pattern=r'\D')],
            FIRST: [CallbackQueryHandler(stratum, pattern=r'\D')],
            SECOND: [CallbackQueryHandler(rooms, pattern=r'\D')],
            THIRD: [CallbackQueryHandler(bathrooms, pattern=r'\D')],
            FOURTH: [CallbackQueryHandler(garages, pattern=r'\D')],
            FIFTH: [CallbackQueryHandler(estrato, pattern=r'\D')],
            SIXTH: [CallbackQueryHandler(tipo, pattern=r'\D')],
            SEVEN: [CallbackQueryHandler(area, pattern=r'\D')]
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