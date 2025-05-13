import psycopg2
from configparser import ConfigParser
import os

def load_config(filename='config/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}

def connect_to_db():
    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        return conn
    except (psycopg2.DatabaseError, Exception) as e:
        print(f"Ошибка подключения: {e}")
        return None

def init_db():
    """Создаёт таблицы и заполняет их данными из SQL-файла"""
    conn = connect_to_db()
    if not conn:
        return False
    
    try:
        with open("data/init_db.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()
        
        cursor = conn.cursor()
        cursor.execute(sql_script)
        conn.commit()
        print("База данных успешно инициализирована!")
        return True
    except Exception as e:
        print(f"Ошибка при загрузке SQL: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()