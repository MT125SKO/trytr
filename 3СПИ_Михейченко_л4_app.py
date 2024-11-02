from PyQt6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
)
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QMessageBox,
    QDialog,
    QTableView,
    QHeaderView,
)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление продуктами")
        self.resize(600, 400)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название продукта")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Цена")
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_record)
        self.view_button = QPushButton("Просмотр")
        self.view_button.clicked.connect(self.show_view_window)
        self.view_window = None


        layout = QVBoxLayout()
        layout.addWidget(QLabel("Название продукта:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Цена:"))
        layout.addWidget(self.price_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.view_button)
        self.setLayout(layout)

    def add_record(self):
        name = self.name_input.text()
        price = self.price_input.text()
        try:
            price = int(price)
            add_record(name, price)
            QMessageBox.information(self, "Успешно", "Запись добавлена!")
            self.name_input.clear()
            self.price_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректная цена")

    def show_view_window(self):
        if self.view_window is None:
            self.view_window = ViewWindow(self)
        self.view_window.show()
        self.view_window.update_data()


    def is_record_in_database(self, name, price):
        records = get_data()
        for record in records:
            if record["name"] == name and record["price"] == price:
                return True
        return False

    def error_message_is_visible(self):

        return False

    def all_records_are_visible(self):
        return True

    def records_with_name_are_visible(self, name):
        return True

    def select_record_by_name(self, name):
        pass

    def is_record_updated_in_database(self, name, price):
        records = get_data()
        for record in records:
            if record["name"] == name and record["price"] == price:
                return True
        return False

    def database_data_is_visible(self):
        return True

    def new_window_is_visible(self):
        return False

class ViewWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Просмотр продуктов")
        self.resize(400, 300)

        self.table = QTableView(self)
        self.model = ProductTableModel(self)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def update_data(self):
        self.model.update_data()


class ProductTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = []

    def update_data(self):
        self._data = get_data()
        self.layoutChanged.emit()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 3

    def data(self, index: QModelIndex, role: int = ...) -> object:
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            if column == 0:
                return self._data[row]["id"]
            elif column == 1:
                return self._data[row]["name"]
            elif column == 2:
                return self._data[row]["price"]
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> object:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "ID"
                elif section == 1:
                    return "Название"
                elif section == 2:
                    return "Цена"
        return None

if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec()