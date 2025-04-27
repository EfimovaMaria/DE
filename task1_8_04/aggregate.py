import psycopg2
import pandas as pd
from datetime import datetime
import sys

#подключение к базе данных
def create_connection():
    try:
        conn = psycopg2.connect(
            dbname="database",
            user="user",
            password="1234",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        sys.exit(1)

#получение периода от пользователя
period = input("Введите период в формате YYYY-MM-DD:YYYY-MM-DD: ").strip()
start_str, end_str = period.split(":")
start_date = datetime.strptime(start_str, "%Y-%m-%d")
end_date = datetime.strptime(end_str, "%Y-%m-%d")

#подключение к базе данных
conn = create_connection()

#запрос для получения логов
query = """
SELECT l.current_period, l.user_id, l.action, l.action_id, 
       m.content, t.title
FROM logs l
LEFT JOIN messages m ON l.action_id = m.message_id
LEFT JOIN topics t ON l.action_id = t.topic_id
WHERE l.current_period::date BETWEEN %s AND %s;
"""

#чтение данных в DataFrame
df = pd.read_sql(query, conn, params=[start_date.date(), end_date.date()])
conn.close()


df['date'] = pd.to_datetime(df['current_period']).dt.date

#количество новых аккаунтов
registrations = df[df['action'] == 'регистрация'].groupby('date').size().rename("new_accounts")

#количество сообщений всего и анонимных
messages = df[df['action'] == 'написание сообщения']
total_messages = messages.groupby('date').size().rename("total_messages")
anon_messages = messages[messages['user_id'].isna()].groupby('date').size().rename("anon_messages")

#% анонимных сообщений
anon_pct = (anon_messages / total_messages * 100).rename("anon_message_pct").fillna(0)

#количество созданных тем по дням
topics_created = df[df['action'] == 'создание темы']
daily_topics = topics_created.groupby('date').size().rename("new_topics")

#кумулятивное количество тем
cumulative_topics = daily_topics.cumsum()

#% прироста количества тем относительно предыдущего дня
topic_change_pct = cumulative_topics.pct_change().fillna(0) * 100
topic_change_pct = topic_change_pct.rename("topic_change_pct")

#объединение результатов
result = pd.concat([registrations, anon_pct, total_messages, topic_change_pct], axis=1).fillna(0)
result = result.round(2).reset_index().rename(columns={"date": "day"})

#сохранение результата
result.to_csv("aggregated_logs.csv", index=False)