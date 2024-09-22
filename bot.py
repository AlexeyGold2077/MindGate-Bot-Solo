from telebot import types
import telebot
import mindgate
import _private

bot = telebot.TeleBot(_private.TOKEN)
SYSTEM_MESSAGE = "Be brief"


# command handlers

@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, '🤙 Привет! Я ваш AI помощник. Чем могу помочь?')


@bot.message_handler(commands=['reset'])
def command_reset(message):
    mindgate.clearMessages(message.chat.id)
    bot.send_message(message.chat.id, "🫨 Память сброшена!")


@bot.message_handler(commands=['settings'])
def command_model(message):
    markup = types.InlineKeyboardMarkup()
    change_model_button = types.InlineKeyboardButton('Change 🤖', callback_data='change_model_button_callback')
    add_balance_button = types.InlineKeyboardButton('Add ⛽️', callback_data='add_balance_button_callback')
    markup.add(change_model_button, add_balance_button)
    bot.send_message(message.chat.id, f'🤖 Model - {mindgate.getModel(message.chat.id)['data']}\n'
                                      f'⛽️ Balance - {mindgate.getBalance(message.chat.id)['data']}',
                     reply_markup=markup)


# text handler

@bot.message_handler(content_types=['text'])
def respond_to_text(message):
    user_message = message.text
    response = mindgate.sendMessageAsUser(message.chat.id, user_message)
    bot.send_message(message.chat.id,
                     response['response_message'] +
                     f'\n\n⛽️ {response['spent_words']}/{mindgate.getBalance(message.chat.id)['data']}', parse_mode="Markdown")


# callback query handlers

@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    if call.data == 'change_model_button_callback':
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('gpt-4o', callback_data='callback_query_model-gpt-4o')
        button2 = types.InlineKeyboardButton('gpt-4o-mini', callback_data='callback_query_model-gpt-4o-mini')
        button3 = types.InlineKeyboardButton('gpt-4', callback_data='callback_query_model-gpt-4')
        button4 = types.InlineKeyboardButton('gpt-4-turbo', callback_data='callback_query_model-gpt-4-turbo')
        markup.add(button1, button2)
        markup.add(button3, button4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🛠️ Select model',
                              reply_markup=markup)
    if call.data == 'add_balance_button_callback':
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Add 1000', callback_data='add_1000_button')
        markup.add(button1)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='How much to add?',
                              reply_markup=markup)
    if call.data == 'add_1000_button':
        mindgate.addBalance(call.message.chat.id, 1000)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, '✅ 1000 added!')
    if call.data == 'callback_query_model-gpt-4o':
        mindgate.setModel(call.message.chat.id, 'gpt-4o')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, '✅ You selected gpt-4o.')
    elif call.data == 'callback_query_model-gpt-4':
        mindgate.setModel(call.message.chat.id, 'gpt-4')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, '✅ You selected gpt-4.')
    elif call.data == 'callback_query_model-gpt-4-turbo':
        mindgate.setModel(call.message.chat.id, 'gpt-4-turbo')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, '✅ You selected gpt-4-turbo.')


bot.infinity_polling()
