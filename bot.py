from telebot import types
import telebot
from telebot.types import LabeledPrice

import mindgate
import _private

bot = telebot.TeleBot(_private.TOKEN)

last_buttoned_message = None

prices = [
    [LabeledPrice(label='10 000 ⛽️', amount=10000)],
    [LabeledPrice(label='25 000 ⛽️', amount=25000)],
    [LabeledPrice(label='50 000 ⛽️', amount=50000)],
    [LabeledPrice(label='100 000 ⛽️', amount=100000)]
]


# command handlers

@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, '🤙 Привет! Просто напиши свой запрос и я на него отвечу!\n\n'
                          '/settings - изменить модель, пополнить баланс\n'
                          '/reset - сбросить контекст запросов')


@bot.message_handler(commands=['reset'])
def command_reset(message):
    mindgate.clearMessages(message.chat.id)
    bot.send_message(message.chat.id, "🫨 Память сброшена!")


@bot.message_handler(commands=['settings'])
def command_model(message):
    global last_buttoned_message
    markup = types.InlineKeyboardMarkup()
    change_model_button = types.InlineKeyboardButton('Change 🤖', callback_data='change_model_button_callback')
    add_balance_button = types.InlineKeyboardButton('Buy ⛽️', callback_data='add_balance_button_callback')
    markup.add(change_model_button, add_balance_button)
    if last_buttoned_message != None: bot.delete_message(message.chat.id, last_buttoned_message.message_id)
    last_buttoned_message = bot.send_message(message.chat.id, f'🤖 Model - {mindgate.getModel(message.chat.id)['data']}\n'
                                      f'⛽️ Balance - {mindgate.getBalance(message.chat.id)['data']}',
                     reply_markup=markup)


# text handler

@bot.message_handler(content_types=['text'])
def respond_to_text(message):
    global last_buttoned_message
    user_message = message.text
    response = mindgate.sendMessageAsUser(message.chat.id, user_message)
    print(response)
    if response['status_code'] == 'SUCCESS':
        bot.send_message(message.chat.id,
                         f"{response['response_message']}\n\n⛽️ {response['spent_words']}/{mindgate.getBalance(message.chat.id)['data']}",
                         parse_mode="Markdown")
    elif response['status_code'] == 'INSUFFICIENT_BALANCE':
        markup = types.InlineKeyboardMarkup()
        add_balance_button = types.InlineKeyboardButton('Buy ⛽️', callback_data='add_balance_button_callback')
        markup.add(add_balance_button)
        if last_buttoned_message != None: bot.delete_message(message.chat.id, last_buttoned_message.message_id)
        last_buttoned_message = bot.send_message(message.chat.id, '⛔️ Insufficient balance', reply_markup=markup)


# callback query handlers

@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    global last_buttoned_message
    if call.data == 'change_model_button_callback':
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('gpt-4o', callback_data='callback_query_model-gpt-4o')
        button2 = types.InlineKeyboardButton('gpt-4o-mini', callback_data='callback_query_model-gpt-4o-mini')
        button4 = types.InlineKeyboardButton('gpt-4-turbo', callback_data='callback_query_model-gpt-4-turbo')
        markup.add(button1, button2, button4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🛠️ Select model',
                              reply_markup=markup)
    if call.data == 'add_balance_button_callback':
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('10 000 ⛽️ - 100₽', callback_data='add_10000_button')
        button2 = types.InlineKeyboardButton('25 000 ⛽️ - 250₽', callback_data='add_25000_button')
        button3 = types.InlineKeyboardButton('50 000 ⛽️ - 500₽', callback_data='add_50000_button')
        button4 = types.InlineKeyboardButton('100 000 ⛽️ - 1000₽', callback_data='add_100000_button')
        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        markup.add(button4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='How much to add?',
                              reply_markup=markup)

    if call.data == 'add_10000_button':
        if last_buttoned_message != None: bot.delete_message(call.message.chat.id, last_buttoned_message.message_id)
        last_buttoned_message = bot.send_invoice(chat_id=call.message.chat.id,
                                                 title='Add balance',
                                                 description='Buy some ⛽️',
                                                 invoice_payload='add_balance',
                                                 provider_token=_private.YKASSA_TOKEN,
                                                 currency='RUB',
                                                 prices=prices[0])
    if call.data == 'add_balance_10000':
        mindgate.addBalance(call.message.chat.id, 10000)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, '✅ 10 000 ⛽️ added!')

    if call.data == 'add_25000_button':
        if last_buttoned_message != None: bot.delete_message(call.message.chat.id, last_buttoned_message.message_id)
        last_buttoned_message = bot.send_invoice(chat_id=call.message.chat.id,
                                                 title='Add balance',
                                                 description='Buy some ⛽️',
                                                 invoice_payload='add_balance_25000',
                                                 provider_token=_private.YKASSA_TOKEN,
                                                 currency='RUB',
                                                 prices=prices[1])
    if call.data == 'add_balance_25000':
        mindgate.addBalance(call.message.chat.id, 25000)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, '✅ 25 000 ⛽️ added!')

    if call.data == 'add_50000_button':
        if last_buttoned_message != None: bot.delete_message(call.message.chat.id, last_buttoned_message.message_id)
        last_buttoned_message = bot.send_invoice(chat_id=call.message.chat.id,
                                                 title='Add balance',
                                                 description='Buy some ⛽️',
                                                 invoice_payload='add_balance_50000',
                                                 provider_token=_private.YKASSA_TOKEN,
                                                 currency='RUB',
                                                 prices=prices[2])
    if call.data == 'add_balance_50000':
        mindgate.addBalance(call.message.chat.id, 50000)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, '✅ 50 000 ⛽️ added!')

    if call.data == 'add_100000_button':
        if last_buttoned_message != None: bot.delete_message(call.message.chat.id, last_buttoned_message.message_id)
        last_buttoned_message = bot.send_invoice(chat_id=call.message.chat.id,
                                                 title='Add balance',
                                                 description='Buy some ⛽️',
                                                 invoice_payload='add_balance_100000',
                                                 provider_token=_private.YKASSA_TOKEN,
                                                 currency='RUB',
                                                 prices=prices[3])
    if call.data == 'add_balance_100000':
        mindgate.addBalance(call.message.chat.id, 100000)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, '✅ 100 000 ⛽️ added!')

    if call.data == 'callback_query_model-gpt-4o':
        mindgate.setModel(call.message.chat.id, 'gpt-4o')
        if last_buttoned_message != None: bot.delete_message(call.message.chat.id, last_buttoned_message.message_id)
        last_buttoned_message = bot.send_message(call.message.chat.id, '✅ You selected gpt-4o.')
    if call.data == 'callback_query_model-gpt-4o-mini':
        mindgate.setModel(call.message.chat.id, 'gpt-4o-mini')
        if last_buttoned_message != None: bot.delete_message(call.message.chat.id, last_buttoned_message.message_id)
        last_buttoned_message = bot.send_message(call.message.chat.id, '✅ You selected gpt-4o-mini.')
    elif call.data == 'callback_query_model-gpt-4-turbo':
        mindgate.setModel(call.message.chat.id, 'gpt-4-turbo')
        if last_buttoned_message != None: bot.delete_message(call.message.chat.id, last_buttoned_message.message_id)
        last_buttoned_message = bot.send_message(call.message.chat.id, '✅ You selected gpt-4-turbo.')


bot.infinity_polling()
