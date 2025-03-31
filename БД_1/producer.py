import random
import string
import time
import redis
import json

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0)

while True:
    # Генерация случайного сообщения
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Создание словаря
    message_dict = {'message': message}

    # Сериализация словаря в строку JSON
    message_json = json.dumps(message_dict)

    # Отправка сериализованного сообщения в Redis
    r.lpush('messages', message_json)

    print(f"Sent: {message}")
    
    time.sleep(60)  # Ждать 1 минуту