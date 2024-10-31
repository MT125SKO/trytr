import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog,
                             QLabel, QLineEdit)


class TextEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("окно редактор")
        self.textEdit = QTextEdit()
        self.create_button = QPushButton("Создать новый")
        self.save_button = QPushButton("Сохранить файл")
        self.open_button = QPushButton("Открыть файл")
        self.file_name_edit = QLineEdit()

        self.char_count_label = QLabel("Количество символов")
        self.word_count_label = QLabel("Количество слов")
        self.longest_word_label = QLabel("Самое длинное слово ")
        self.shortest_word_label = QLabel("Самое короткое слово ")
        self.most_frequent_word_label = QLabel("самое частое слово")

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.create_button)
        hbox1.addWidget(self.save_button)
        hbox1.addWidget(self.open_button)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Имя файла для сохранения: "))
        hbox2.addWidget(self.file_name_edit)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.textEdit)
        vbox.addWidget(self.char_count_label)
        vbox.addWidget(self.word_count_label)
        vbox.addWidget(self.longest_word_label)
        vbox.addWidget(self.shortest_word_label)
        vbox.addWidget(self.most_frequent_word_label)
        self.setLayout(vbox)
        self.create_button.clicked.connect(self.create_new_file)
        self.save_button.clicked.connect(self.save_file)
        self.open_button.clicked.connect(self.open_file)

    def create_new_file(self):
        file_name = self.file_name_edit.text()
        if file_name:
            if not file_name.endswith(".txt"):
                file_name += ".txt"

            try:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(self.textEdit.toPlainText())
            except Exception as e:
                print(f"Ошибка создания файла {e}")

    def save_file(self):
        file_name = self.file_name_edit.text()
        if file_name:
            if not file_name.endswith(".txt"):
                file_name += ".txt"

            try:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(self.textEdit.toPlainText())
            except Exception as e:
                print(f"Ошибка сохранения файла {e}")

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Text Files (*.txt)"
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    self.textEdit.setText(text)
                    self.update_file_info(text)
            except Exception as e:
                print(f"Ошибка открытия файла {e}")

    def update_file_info(self, text=""):
        if text:
            self.char_count_label.setText(f"Количество символов {len(text)}")
            words = text.split()
            self.word_count_label.setText(f"Количество слов {len(words)}")

            longest_word = max(words, key=len)
            shortest_word = min(words, key=len)
            self.longest_word_label.setText(f"Самое длинное слово {longest_word}")
            self.shortest_word_label.setText(f"Самое короткое слово {shortest_word}")

            word_counts = {}
            for word in words:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

            most_frequent_word = max(word_counts, key=word_counts.get)
            self.most_frequent_word_label.setText(f"самое частое слово {most_frequent_word}")
        else:
            self.char_count_label.setText("Количество символов")
            self.word_count_label.setText("Количество слов")
            self.longest_word_label.setText("Самое длинное слово: ")
            self.shortest_word_label.setText("Самое короткое слово: ")
            self.most_frequent_word_label.setText("самое частое слово ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())
