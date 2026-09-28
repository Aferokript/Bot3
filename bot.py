import os 
import telebot
from dotenv import load_dotenv
from google.cloud import dialogflow


load_dotenv()

project_id = os.environ['GOOGLE_PROJECT_ID']
language_code = 'ru'
telegram_token = os.getenv('TG_TOKEN')
bot = telebot.TeleBot(telegram_token)


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))
    
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
    return response.query_result.fulfillment_text


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Я эхо бот')


@bot.message_handler(content_types=['text'])
def text_handler(message):
    session_id = str(message.chat.id)
    chat_id = message.chat.id
    user_text = detect_intent_texts(project_id, session_id, message.text, language_code)
    bot.send_message(chat_id, user_text)
    

bot.polling(none_stop=True)

