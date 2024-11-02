import sqlite3

DATABASE_FILE = "products.db"

def create_connection(db_file):
    """Создает соединение с базой данных SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(f"Ошибка при создании соединения: {e}")

def create_table(conn):
    """Создает таблицу в базе данных."""
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        """
        )
        conn.commit()
        print("Таблица успешно создана")
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")

def add_record(name, price):
    """Добавляет новую запись в таблицу."""
    conn = create_connection(DATABASE_FILE)
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price) VALUES (?, ?)", (name, price)
        )
        conn.commit()

def get_data():
    """Получает данные из таблицы."""
    conn = create_connection(DATABASE_FILE)
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        return [
            {"id": row[0], "name": row[1], "price": row[2]} for row in rows
        ]

def update_record(id, name, price):
    """Обновляет запись в таблице."""
    conn = create_connection(DATABASE_FILE)
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET name = ?, price = ? WHERE id = ?",
            (name, price, id),
        )
        conn.commit()

def delete_record(id):
    """Удаляет запись из таблицы."""
    conn = create_connection(DATABASE_FILE)
    with conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (id,))
        conn.commit()

conn = create_connection(DATABASE_FILE)
if conn is not None:
    create_table(conn)