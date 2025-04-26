import pandas as pd
from sqlalchemy import create_engine


#Создание подключения к базе данных
engine = create_engine('postgresql+psycopg2://user1:1234@127.0.0.1:5432/database')

#Функция для загрузки данных из CSV в таблицу
def load_data_from_csv(file_path, table_name):
    #Чтение CSV файла
    data = pd.read_csv(file_path)

    #Обработка NaN значений
    data['user_id'] = data['user_id'].apply(lambda x: str(x) if pd.notnull(x) else None)

    #Загрузка данных в таблицу
    data.to_sql(table_name, engine, if_exists='append', index=False)

#Загрузка данных из CSV файлов в соответствующие таблицы
load_data_from_csv('/Users/MAC/PycharmProjects/task1_8_04/users_dataset.csv', 'users')
load_data_from_csv('/Users/MAC/PycharmProjects/task1_8_04/topics_dataset.csv', 'topics')
load_data_from_csv('/Users/MAC/PycharmProjects/task1_8_04/messages_dataset.csv', 'messages')
load_data_from_csv('/Users/MAC/PycharmProjects/task1_8_04/logs_dataset.csv', 'logs')

print("Данные успешно загружены в базу данных.")







