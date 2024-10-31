import sys
import csv
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox,
                             QFileDialog, QLabel)


class OlympiadResults(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Участники")
        self.setWindowIcon(QIcon('C:\qa'))
        self.setGeometry(100, 100, 800, 600)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Логин", "Имя", "Баллы", "Место"])

        self.table_header = QLabel("Результаты ")
        self.table_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_header.setStyleSheet("font-size: 16pt; font-weight: bold;")

        self.school_filter = QComboBox()
        self.school_filter.currentIndexChanged.connect(self.filter_results)

        self.class_filter = QComboBox()
        self.class_filter.currentIndexChanged.connect(self.filter_results)

        layout = QVBoxLayout()
        layout.addWidget(self.table_header)
        layout.addWidget(self.school_filter)
        layout.addWidget(self.class_filter)
        layout.addWidget(self.table)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.open_file()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.load_data(file_path)

    def load_data(self, file_path):
        self.data = []
        self.schools = set()
        self.classes = set()

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data.append(row)
                self.schools.add(row["login"].split("-")[1])
                self.classes.add(row["login"].split("-")[2])

        self.school_filter.addItems(sorted(self.schools))
        self.class_filter.addItems(sorted(self.classes))

        self.filter_results()

    def filter_results(self):
        school = self.school_filter.currentText()
        class_ = self.class_filter.currentText()

        filtered_data = [row for row in self.data if
                         row["login"].split("-")[1] == school and row["login"].split("-")[2] == class_]
        filtered_data.sort(key=lambda x: int(x["Score"]), reverse=True)

        self.table.setRowCount(len(filtered_data))

        places = {}
        prev_score = None
        place = 0

        for i, row in enumerate(filtered_data):
            if row["Score"] != prev_score:
                place = i + 1
                prev_score = row["Score"]

            places[row["login"]] = place

            self.table.setItem(i, 0, QTableWidgetItem(row["login"]))
            self.table.setItem(i, 1, QTableWidgetItem(row["user_name"]))
            self.table.setItem(i, 2, QTableWidgetItem(row["Score"]))
            self.table.setItem(i, 3, QTableWidgetItem(str(place)))

            if place == 1:
                for j in range(4):
                    self.table.item(i, j).setBackground(QColor(255, 215, 0))
            elif place == 2:
                for j in range(4):
                    self.table.item(i, j).setBackground(QColor(192, 192, 192))
            elif place == 3:
                for j in range(4):
                    self.table.item(i, j).setBackground(QColor(205, 127, 50))  #


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OlympiadResults()
    window.show()
    sys.exit(app.exec())