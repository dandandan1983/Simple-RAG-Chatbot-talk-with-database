import sqlite3

def get_ddl_list(database_path):
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
