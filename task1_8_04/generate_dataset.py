import random
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta

fake = Faker()

#все действия в логах
ACTIONS = [
    "первый заход на сайт",
    "регистрация",
    "логин",
    "логаут",
    "создание темы",
    "заход на тему",
    "удаление темы",
    "написание сообщения"
]


#функция для генерации пользователей
def generate_users(num_users):
    users = []
    for _ in range(num_users):
        user_entry = {
            'user_id': fake.uuid4(),
            'username': fake.user_name(),
            'email': fake.email(),
            'password_hash': fake.password(),
            'registered_at': fake.date_time_this_year()
        }
        users.append(user_entry)
    return users


#функция для генерации тем
def generate_topics(users, num_topics):
    topics = []
    for _ in range(num_topics):
        user_id = random.choice(users)['user_id']
        topic_entry = {
            'topic_id': fake.uuid4(),
            'title': fake.sentence(),
            'user_id': user_id,
            'created_at': fake.date_time_this_year()
        }
        topics.append(topic_entry)
    return topics


#функция для генерации сообщений
def generate_messages(topics, num_messages):
    messages = []
    for _ in range(num_messages):
        topic_id = random.choice(topics)['topic_id']
        user_id = random.choice(
            [fake.uuid4(), None])  #случайный выбор между залогиненным и незалогиненным пользователем
        message_entry = {
            'message_id': fake.uuid4(),
            'content': fake.text(),
            'topic_id': topic_id,
            'user_id': user_id,
            'created_at': fake.date_time_this_year()
        }
        messages.append(message_entry)
    return messages


#функция для генерации логов
def generate_logs(users, topics, start_date, num_days):
    logs = []

    for day in range(num_days):
        current_date = start_date + timedelta(days=day)

        #генерация действий за день
        actions_today = {
            "первый заход на сайт": 1,
            "регистрация": 1,
            "логин": random.randint(1, 5),
            "логаут": random.randint(1, 5),
            "создание темы": random.randint(2, 5),  #минимум 2 ошибки по отсутствию логина
            "заход на тему": random.randint(5, 10),
            "удаление темы": random.randint(1, 3),
            "написание сообщения": random.randint(3, 7)
        }

        for action, count in actions_today.items():
            for _ in range(count):
                user_id = None
                server_response = 'успех'
                action_id = None

                if action == "создание темы":
                    #проверяем, залогинен ли пользователь
                    if not users:  #если нет пользователей
                        server_response = 'ошибка'
                    else:
                        user_id = random.choice(users)['user_id']

                elif action in ["логин", "логаут"]:
                    user_id = random.choice(users)['user_id'] if action == "логин" else random.choice(users)['user_id']

                elif action == "написание сообщения":
                    #пример равного распределения между залогиненым и незалогиненым пользователем
                    if random.choice([True, False]):
                        user_id = random.choice(users)['user_id']  #залогиненный пользователь
                    else:
                        user_id = None  #незалогиненный пользователь
                        server_response = 'ошибка'
                elif action == "заход на тему":
                    if topics:
                        action_id = random.choice(topics)['topic_id']
                    else:
                        server_response = 'ошибка'

                elif action == "удаление темы":
                    if topics:
                        action_id = random.choice(topics)['topic_id']
                    else:
                        server_response = 'ошибка'

                else:
                    user_id = random.choice(users)['user_id'] if users else None

                log_entry = {
                    'log_id': len(logs) + 1,
                    'user_id': user_id,
                    'action': action,
                    'action_id': fake.uuid4(),  #генерируем уникальный ID действия
                    'server_response': server_response,
                    'current_period': current_date + timedelta(hours=random.randint(0, 23),
                                                               minutes=random.randint(0, 59))
                }

                logs.append(log_entry)

    return logs


#генерация данных за месяц (30 дней)
num_users = 20
num_topics_per_day = 10
num_messages_per_day = 15

start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30)

#генерация пользователей
users_data = generate_users(num_users)

#генерация тем (по количеству пользователей)
topics_data = generate_topics(users_data, num_topics_per_day * 30)

#генерация сообщений (по количеству сообщений за месяц)
messages_data = generate_messages(topics_data, num_messages_per_day * 30)

#генерация логов за месяц (30 дней)
logs_data = generate_logs(users_data, topics_data, start_date, num_days=30)

#создание DataFrame и сохранение в CSV файлы
df_users = pd.DataFrame(users_data)
df_topics = pd.DataFrame(topics_data)
df_messages = pd.DataFrame(messages_data)
df_logs = pd.DataFrame(logs_data)

df_users.to_csv('users_dataset.csv', index=False)
df_topics.to_csv('topics_dataset.csv', index=False)
df_messages.to_csv('messages_dataset.csv', index=False)
df_logs.to_csv('logs_dataset.csv', index=False)

print("Датасеты успешно сгенерированы и сохранены в файлы.")


