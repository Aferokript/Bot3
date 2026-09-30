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
        answers_json = file.read()
    answers = json.loads(answers_json)
    return answers
    
        
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
    
    
intents = load_intent()
for intent_name, intent_answer in intents.items():
    create_intent(project_id, intent_name, intent_answer['questions'], [intent_answer['answer']])

    