import sqlite3
from prettytable import PrettyTable


def get_ddl_dict(database_path):
    """
    Получает DDL всех таблиц и представлений из базы данных SQLite.

    :param database_path: Путь к SQLite базе данных.
    :return: Словарь с DDL таблиц и представлений.
    """
    ddl = {"tables": {}, "views": {}}

    # Подключение к базе данных
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()

        # Получение DDL для таблиц
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        for name, sql in cursor.fetchall():
            ddl["tables"][name] = sql

        # Получение DDL для представлений
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='view';")
        for name, sql in cursor.fetchall():
            ddl["views"][name] = sql

    return ddl


def execute_query(database_path, query):
    """
    Выполняет SQL запрос и возвращает результат в виде текста таблицы.

    :param database_path: Путь к SQLite базе данных.
    :param query: SQL запрос для выполнения.
    :return: Результат запроса в виде текста таблицы.
    """
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            # Получение данных
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]

            # Формирование таблицы
            table = PrettyTable()
            table.field_names = column_names
            for row in rows:
                table.add_row(row)

            return table.get_string()
        except sqlite3.Error as e:
            return f"Ошибка выполнения запроса: {e}"
