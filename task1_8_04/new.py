import pandas as pd
import asyncpg
import asyncio

# Функция для загрузки данных из CSV в таблицу
async def load_data_from_csv(file_path, table_name, connection):
    try:
        # Чтение CSV файла
        data = pd.read_csv(file_path)

        # Получение названий колонок для SQL-запроса
        columns = ', '.join(data.columns)

        # Подготовка SQL-запроса для вставки данных
        for i, row in data.iterrows():
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({', '.join(['$' + str(j + 1) for j in range(len(row))])})"
            await connection.execute(sql, *row)

        print(f"Данные из {file_path} успешно загружены в таблицу {table_name}.")

    except Exception as e:
        print(f"Ошибка при загрузке данных из {file_path}: {e}")

# Основная асинхронная функция
async def main():
    # Подключение к базе данных
    try:
        connection = await asyncpg.connect(
            host='127.0.0.1',
            port=5432,
            user='user',
            password='1234',
            database='mydatabase'
        )
        print("Успешное подключение к базе данных.")

        # Загрузка данных из CSV файлов в соответствующие таблицы
        await load_data_from_csv('users_dataset.csv', 'users', connection)
        await load_data_from_csv('topics_dataset.csv', 'topics', connection)
        await load_data_from_csv('messages_dataset.csv', 'messages', connection)
        await load_data_from_csv('logs_dataset.csv', 'logs', connection)

    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")

    finally:
        await connection.close()
        print("Соединение с базой данных закрыто.")

# Запуск основной функции
if __name__ == '__main__':
    asyncio.run(main())