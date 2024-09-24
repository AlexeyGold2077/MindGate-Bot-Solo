from telebot import types
from telebot.types import LabeledPrice
import telebot
import mindgate
import _private

bot = telebot.TeleBot(_private.TOKEN)

prices = [
    [LabeledPrice(label='10 000 ⛽️', amount=25)],
    [LabeledPrice(label='25 000 ⛽️', amount=75)],
    [LabeledPrice(label='50 000 ⛽️', amount=125)],
    [LabeledPrice(label='100 000 ⛽️', amount=275)]
]


# # command handlers

# command handler - start
@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, '🤙 Привет! Просто напиши свой запрос и я на него отвечу!\n\n'
                          '/settings - изменить модель, пополнить баланс\n'
                          '/reset - сбросить контекст запросов')


# command handler - reset
@bot.message_handler(commands=['reset'])
def command_reset(message):
    mindgate.clearMessages(message.chat.id)
    bot.send_message(message.chat.id, "🫨 Память сброшена!")


# command handler - settings
@bot.message_handler(commands=['settings'])
def command_model(message):
    markup = types.InlineKeyboardMarkup()
    change_model_button = types.InlineKeyboardButton('Change 🤖', callback_data='change_model_button')
    add_balance_button = types.InlineKeyboardButton('Buy ⛽️', callback_data='add_balance_buttons')
    markup.add(change_model_button, add_balance_button)
    bot.send_message(message.chat.id,
                     f'🤖 Model - {mindgate.getModel(message.chat.id)['data']}\n'
                     f'⛽️ Balance - {mindgate.getBalance(message.chat.id)['data']}',
                     reply_markup=markup)


# text handler
@bot.message_handler(content_types=['text'])
def respond_to_text(message):
    user_message = message.text
    response = mindgate.sendMessageAsUser(message.chat.id, user_message)
    print(response)
    if response['status_code'] == 'SUCCESS':
        bot.send_message(message.chat.id,
                         f"{response['response_message']}\n\n"
                         f"⛽️ {response['spent_words']}/{mindgate.getBalance(message.chat.id)['data']}")
    elif response['status_code'] == 'INSUFFICIENT_BALANCE':
        markup = types.InlineKeyboardMarkup()
        add_balance_button = types.InlineKeyboardButton('Buy ⛽️', callback_data='add_balance_buttons')
        markup.add(add_balance_button)
        bot.send_message(message.chat.id, '⛔️ Insufficient balance', reply_markup=markup)


# # callback query handlers

# change_model_button
@bot.callback_query_handler(func=lambda call: call.data == 'change_model_button')
def callback_query_handler_change_model_button(call):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('GPT-4o', callback_data='change_model_button_gpt_4o')
    button2 = types.InlineKeyboardButton('GPT-4o-mini', callback_data='change_model_button_gpt_4o_mini')
    button4 = types.InlineKeyboardButton('GPT-4-turbo', callback_data='change_model_button_gpt_4_turbo')
    markup.add(button1, button2, button4)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='🛠️ Select model',
                          reply_markup=markup)


# add_balance_buttons
@bot.callback_query_handler(func=lambda call: call.data == 'add_balance_buttons')
def callback_query_handler_add_balance_buttons(call):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('10 000 ⛽️ - 25 ⭐️', callback_data='add_balance_button_10000')
    button2 = types.InlineKeyboardButton('25 000 ⛽️ - 75 ⭐️', callback_data='add_balance_button_25000')
    button3 = types.InlineKeyboardButton('50 000 ⛽️ - 125 ⭐️', callback_data='add_balance_button_50000')
    button4 = types.InlineKeyboardButton('100 000 ⛽️ - 275 ⭐️', callback_data='add_balance_button_100000')
    markup.add(button1, button2, button3, button4, row_width=1)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='How much to add?',
                          reply_markup=markup)


# add_balance_button_10000
@bot.callback_query_handler(func=lambda call: call.data == 'add_balance_button_10000')
def callback_query_handler_add_balance_button_10000(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_invoice(chat_id=call.message.chat.id,
                     title='💸 Purchase',
                     description='Buy some ⛽️',
                     invoice_payload='add_balance_button_10000_done',
                     provider_token='',
                     currency='XTR',
                     prices=prices[0])


# add_balance_button_25000
@bot.callback_query_handler(func=lambda call: call.data == 'add_balance_button_25000')
def callback_query_handler_add_balance_button_25000(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_invoice(chat_id=call.message.chat.id,
                     title='💸 Purchase',
                     description='Buy some ⛽️',
                     invoice_payload='add_balance_button_25000_done',
                     provider_token='',
                     currency='XTR',
                     prices=prices[1])


# add_balance_button_50000
@bot.callback_query_handler(func=lambda call: call.data == 'add_balance_button_50000')
def callback_query_handler_add_balance_button_50000(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_invoice(chat_id=call.message.chat.id,
                     title='💸 Purchase',
                     description='Buy some ⛽️',
                     invoice_payload='add_balance_button_50000_done',
                     provider_token='',
                     currency='XTR',
                     prices=prices[2])


# add_balance_button_100000
@bot.callback_query_handler(func=lambda call: call.data == 'add_balance_button_100000')
def callback_query_handler_add_balance_button_100000(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_invoice(chat_id=call.message.chat.id,
                     title='💸 Purchase',
                     description='Buy some ⛽️',
                     invoice_payload='add_balance_button_100000_done',
                     provider_token='',
                     currency='XTR',
                     prices=prices[3])


# answer_pre_checkout_query
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected"
                                                " your credentials, try to pay again in a few minutes, we need a small rest.")


# add_balance_button_*_done
@bot.message_handler(content_types=['successful_payment'])
def process_payment(message):
    payload = message.successful_payment.invoice_payload
    if payload == "add_balance_button_10000_done":
        mindgate.addBalance(message.chat.id, 10000)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, '✅ 10 000 ⛽️ added!')
    if payload == "add_balance_button_25000_done":
        mindgate.addBalance(message.chat.id, 25000)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, '✅ 25 000 ⛽️ added!')
    if payload == "add_balance_button_50000_done":
        mindgate.addBalance(message.chat.id, 50000)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, '✅ 50 000 ⛽️ added!')
    if payload == "add_balance_button_100000_done":
        mindgate.addBalance(message.chat.id, 100000)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, '✅ 100 000 ⛽️ added!')
    else:
        print("Unknown payload")


# change_model_button_gpt_4o
@bot.callback_query_handler(func=lambda call: call.data == 'change_model_button_gpt_4o')
def callback_query_handler_change_model_button_gpt_4o(call):
    mindgate.setModel(call.message.chat.id, 'gpt-4o')
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='✅ You selected GPT-4o')


# change_model_button_gpt_4o_mini
@bot.callback_query_handler(func=lambda call: call.data == 'change_model_button_gpt_4o_mini')
def callback_query_handler_change_model_button_gpt_4o_mini(call):
    mindgate.setModel(call.message.chat.id, 'gpt-4o-mini')
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='✅ You selected GPT-4o-mini')


# change_model_button_gpt_4_turbo
@bot.callback_query_handler(func=lambda call: call.data == 'change_model_button_gpt_4_turbo')
def callback_query_handler_change_model_button_gpt_4_turbo(call):
    mindgate.setModel(call.message.chat.id, 'gpt-4-turbo')
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='✅ You selected GPT-4-turbo')


bot.infinity_polling()
