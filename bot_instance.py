import os 
import telebot
from dotenv import load_dotenv


load_dotenv()

telegram_token = os.getenv('TG_TOKEN')
bot = telebot.TeleBot(telegram_token)




