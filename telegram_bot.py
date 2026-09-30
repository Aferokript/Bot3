import os 
import json
import telebot
from dotenv import load_dotenv
from google.cloud import dialogflow


load_dotenv()

project_id = os.environ['GOOGLE_PROJECT_ID']
language_code = 'ru'
telegram_token = os.getenv('TG_TOKEN')
bot = telebot.TeleBot(telegram_token)


def load_intent():
    with open('answers.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    


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

