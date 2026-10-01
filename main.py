import sys
import time
from bot_instance import bot
import handlers
import requests


def main():
    try:
        bot.polling(none_stop=True)
    except requests.RequestException as error:
        time.sleep(5)
        sys.stderr.write(f'Ошибка {error}')
    
    

if __name__ == '__main__':
    main()