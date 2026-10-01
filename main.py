import sys 
from bot_instance import bot
import handlers
import requests


def main():
    try:
        sys.stdout.write('Запускаем бота...')
        bot.polling(none_stop=True)
    except requests.RequestException as error:
        sys.stderr.write(f'Ошибка {error}')
    
    

if __name__ == '__main__':
    main()