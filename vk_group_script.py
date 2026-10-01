import os
import sys
import random
import time
from google.cloud import dialogflow
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import requests


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))
    
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
                request={"session": session, "query_input": query_input}
            )
    is_fallback = response.query_result.intent.is_fallback
    
    if is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text
        

def send_vk_message(vk, longpoll, project_id, language_code):
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user_message = detect_intent_texts(project_id, str(event.user_id), event.text, language_code)
                if user_message is not None:
                    vk.messages.send(
                        user_id=event.user_id,
                        message=user_message,
                        random_id=random.randint(1, 2**31 - 1)
                    )
                    sys.stdout.write(f'От меня для {user_message}\n')
            else:
                sys.stdout.write(f'От меня для: {event.user_id}\n')
                    

def main():
    load_dotenv()
    
    vk_group_token = os.environ['VK_GROUP_TOKEN']
    project_id = os.environ['GOOGLE_PROJECT_ID']
    
    language_code = 'ru'
    vk_session = vk_api.VkApi(token=vk_group_token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    
    while True:
        try:
            send_vk_message(vk, longpoll, project_id, language_code)
        except requests.RequestException as connection_error:
            time.sleep(5)
            sys.stderr.write(f'Ошибка {connection_error}\n')
    
    
if __name__ == '__main__':
    main()
        


