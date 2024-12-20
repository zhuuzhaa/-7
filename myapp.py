import sqlite3
from flask import Flask, render_template


app = Flask(__name__)


# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('gifts.db')
    conn.row_factory = sqlite3.Row
    return conn


# Проверяет существование таблицы и создает ее, если нет
def check_create_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name='gifts'
        """
    )
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute('''
            CREATE TABLE gifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                gift_name TEXT NOT NULL,
                price REAL NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        conn.commit()
        
        print("Table 'gifts' created.")
    else:
        print("Table 'gifts' already exists.")


# Заполняет базу данных данными, если таблица пустая
def fill_database_if_empty(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM gifts')
    count = cursor.fetchone()[0]
    
    if count == 0:
        data = [
            ('Иванов Иван', 'Книга', 500, 'Не куплено'),
            ('Петров Петр', 'Шарф', 1000, 'Куплено'),
            ('Сидоров Сидор', 'Часы', 2000, 'Не куплено'),
            ('Кузнецова Мария', 'Украшение', 1500, 'Куплено'),
            ('Васильев Василий', 'Набор для рисования', 800, 'Не куплено'),
            ('Николаева Анна', 'Парфюм', 2500, 'Куплено'),
            ('Федоров Федор', 'Кофейная кружка', 300, 'Не куплено'),
            ('Орлова Ольга', 'Шаль', 1200, 'Куплено'),
            ('Сергеев Сергей', 'Брелок', 400, 'Не куплено'),
            ('Александров Александр', 'Подарочный сертификат', 3500, 'Куплено')
        ]
        
        cursor.executemany('INSERT INTO gifts (full_name, gift_name, price, status) VALUES (?, ?, ?, ?)', data)
        conn.commit()
        
        print("Database filled with initial data.")
    else:
        print("Database is not empty. Skipping insertion of initial data.")


# Главная страница
@app.route('/')
def index():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM gifts')
            rows = cursor.fetchall()
            return render_template('index.html', rows=rows)
            
    except sqlite3.Error as e:
        return f"Error fetching data from database: {e}"


if __name__ == '__main__':
    with get_db_connection() as conn:
        check_create_table(conn)
        fill_database_if_empty(conn)
        
    app.run(debug=True)
    #app.run(host='0.0.0.0')