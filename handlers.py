from detect_intent import detect_intent_texts
from bot_instance import bot, project_id, language_code


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Я эхо бот')


@bot.message_handler(content_types=['text'])
def text_handler(message):
    session_id = str(message.chat.id)
    chat_id = message.chat.id
    user_text = detect_intent_texts(project_id, session_id, message.text, language_code=language_code)
    if user_text is not None:
        bot.send_message(chat_id, user_text)
    