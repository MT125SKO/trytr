import pytest
import sqlite3

@pytest.fixture
def database():

    db_file = "сервис.db"
    conn = sqlite3.connect(db_file)


    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS пользователи (
            id INTEGER PRIMARY KEY,
            имена TEXT NOT NULL,
            почта TEXT NOT NULL
        )
    """)
    conn.commit()
    yield conn
    conn.close()
    import os
    os.remove(db_file)

def test_insert_data(database):

    cursor = database.cursor()
    cursor.execute("INSERT INTO пользователи (имена, почта) VALUES ('камень', 'африка@.com')")
    database.commit()

    cursor.execute("SELECT * FROM пользователи WHERE имена='камень'")
    result = cursor.fetchone()

    assert result is not None

#######################################
import pytest
import sqlite3

@pytest.fixture
def database():
    db_file = "test_database.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    yield conn
    conn.close()
    import os
    if os.path.exists(db_file):
        os.remove(db_file)

def test_insert_data(database):
    cursor = database.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES ('Item 1', 100.0)")
    database.commit()

    cursor.execute("SELECT * FROM items WHERE name='Item 1'")
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == 'Item 1'
    assert result[2] == 100.0

@pytest.mark.parametrize("name, price", [
    ('Item 2', 1.0),
    ('Item 3', 300.0),
    ('Item 4', 3430.0),
    ('Item 5', 30.0),
])
def test_insert_data_parametrized(database, name, price):
    cursor = database.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, price))
    database.commit()

    cursor.execute("SELECT * FROM items WHERE name=?", (name,))
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == name
    assert result[2] == price

def test_update_data(database):
    cursor = database.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES ('Item 1', 100.0)")
    database.commit()

    cursor.execute("UPDATE items SET price=150.0 WHERE name='Item 1'")
    database.commit()

    cursor.execute("SELECT * FROM items WHERE name='Item 1'")
    result = cursor.fetchone()

    assert result is not None
    assert result[2] == 150.0

def test_delete_data(database):
    cursor = database.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES ('Item 1', 100.0)")
    database.commit()

    cursor.execute("DELETE FROM items WHERE name='Item 1'")
    database.commit()

    cursor.execute("SELECT * FROM items WHERE name='Item 1'")
    result = cursor.fetchone()

    assert result is None

def test_get_all_data(database):
    cursor = database.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES ('Item 1', 100.0)")
    cursor.execute("INSERT INTO items (name, price) VALUES ('Item 2', 200.0)")
    database.commit()

    cursor.execute("SELECT * FROM items")
    results = cursor.fetchall()

    assert len(results) == 2
###########################################################MainWindow

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
                             QPushButton, QVBoxLayout, QLineEdit)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("окно")

        self.label = QLabel("вход")
        self.label.setObjectName("label")
        self.button = QPushButton("жми")
        self.button.setObjectName("button")
        self.input_field = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        text = self.input_field.text()
        self.label.setText(f"Вы ввели: {text}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

#####################################   test_mainWin.ry
import pytest
from PyQt6.QtWidgets import QApplication, QWidget
from mainWin import MainWindow

@pytest.fixture
def main_window():

    app = QApplication([])
    window = MainWindow()
    yield window
    app.quit()

def test_widget_presence(main_window):
    assert main_window.findChild(QWidget, "label") is not None
    assert main_window.findChild(QWidget, "button") is not None

def test_button_click(main_window):
    button = main_window.findChild(QWidget, "button")
    assert button is not None
    button.click()

    expected_text = f"Вы ввели: {main_window.input_field.text()}"
    assert main_window.label.text() == expected_text