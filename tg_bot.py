import os 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from detect_intent import detect_intent_texts
from dotenv import load_dotenv


def start(update, context):
    update.message.reply_text('Здравствуйте. Чем я могу вам помочь?')
    

def process_text(update, context):
    user_text = update.message.text
    project_id = context.bot_data['project_id']
    language_code = context.bot_data['language_code'] 
    bot_message = detect_intent_texts(project_id, f'tg_{update.message.chat_id}', user_text, language_code)
    update.message.reply_text(bot_message)
    

def main():
    load_dotenv()
    
    telegram_token = os.environ['TG_TOKEN']
    project_id = os.environ['GOOGLE_PROJECT_ID']
    language_code = 'ru'
    
    updater = Updater(telegram_token, use_context=True)
    dp = updater.dispatcher

    dp.bot_data['project_id'] = project_id
    dp.bot_data['language_code'] = language_code

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process_text))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()