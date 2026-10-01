import os 
import telebot
from dotenv import load_dotenv


load_dotenv()

telegram_token = os.environ['TG_TOKEN']
project_id = os.environ['GOOGLE_PROJECT_ID']
language_code = 'ru'
bot = telebot.TeleBot(telegram_token)




