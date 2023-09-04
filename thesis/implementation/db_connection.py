import psycopg2
from io import StringIO
import pandas as pd

class Connection():
    def __init__(self):
        # Подключение к БД отеля
        self.conn = psycopg2.connect(
            host="host",
            database="database",
            user="username",
            password="password"
        )

    def collect_data_from_database(self, where=''):

        # Создание курсора для взаимодействия с таблицой БД
        cursor = self.conn.cursor()

        try:
            # Выполнение SQL запроса
            query = f"SELECT * FROM bookings_table {where}"
            cursor.execute(query)

            # Забор всех записей из БД по запросу
            booking_data = cursor.fetchall()

            # Закрытие курсора
            cursor.close()

            return booking_data

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error occurred while fetching data from the database:", error)

            # В случае ошибки закрытие курсора
            cursor.close()

            return None


    def collect_demand_train_data(self, select='*', where=''):

        # Создание курсора для взаимодействия с БД
        cursor = self.conn.cursor()

        try:
            # Выполенение запроса для забора данных о спросе
            query = f"SELECT {select} FROM occupancy_rate_predictions {where}"
            cursor.execute(query)

            # Забор всех записей, соответствующих запросу
            occupancy_rate_data = cursor.fetchall()

            # Закрытие курсора и возврат ответа
            cursor.close()

            return occupancy_rate_data

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error occurred while fetching data from the database:", error)

            # В случае ошибки закрытие курсора
            cursor.close()

            return None
    
    
    def upload_predictions(id_numbers, column_values):
        cursor = self.conn.cursor()

        # Подготовка SQL-запроса
        update_query = "UPDATE bookings_table SET predicted_cancellations = %s WHERE id = %s"
        try:
            # Итерации по записям для обновления полей
            for id_num, value in zip(id_numbers, column_values):
                # Выполение запроса на обновление таблицы
                cursor.execute(update_query, (value, id_num))

            # Сохранение изменений в БД и закрытие курсора
            conn.commit()
            cursor.close()
        
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error occurred while fetching data from the database:", error)

            # CВ случае ошибки закрытие курсора
            cursor.close()

            return None
    
    
    def upload_demand(df):
        cursor = conn.cursor()

        # Определение названия таблицы в БД
        table_name = "occupancy_rate_predictions"

        # Определение название колонок
        df_columns = df.columns.to_list()  

        # Подготовка запроса SQL для массовой вставки
        copy_query = f"COPY {table_name} ({', '.join(df_columns)}) FROM STDIN WITH CSV HEADER DELIMITER ','"

        # Создание буфера для хранения содержимого
        buffer = StringIO()
        df.to_csv(buffer, index=False, header=True, sep=',')
        
        try:
            # Сдвиг курсора буфера в начало
            buffer.seek(0)

            # Выполнение запроса для загрузки информации из буфера
            cursor.copy_expert(copy_query, buffer)

            # Сохранение изменений в БД и закрытие курсора
            conn.commit()
            cursor.close()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error occurred while fetching data from the database:", error)

            # В случае ошибки закрытие курсора
            cursor.close()

            return None
    
    def close(self):
        # Закрытие соединения с БД
        self.conn.close()
        