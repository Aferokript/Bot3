import os 
import telebot
from dotenv import load_dotenv


load_dotenv()

telegram_token = os.getenv('TG_TOKEN')
bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start']) 
def start(message):
    chat_id = message.chat.id 
    bot.send_message(chat_id, 'Привет! Я эхо бот')
    user_text = message.text
    bot.send_message(chat_id, user_text)
    

bot.polling(none_stop=True)