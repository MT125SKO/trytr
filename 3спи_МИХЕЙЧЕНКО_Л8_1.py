import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider,
                             QFileDialog, )
from PyQt6.QtGui import QTransform
from PyQt6.QtGui import QImage, QPixmap, QColor
from PyQt6.QtCore import Qt


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("окно")
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(0, 255)
        self.opacity_slider.setValue(255)
        self.opacity_slider.valueChanged.connect(self.change_opacity)

        self.open_button = QPushButton("Открыть файл")
        self.open_button.clicked.connect(self.open_image)

        self.rotate_left_button = QPushButton("влево")
        self.rotate_left_button.clicked.connect(self.rotate_left)
        self.rotate_right_button = QPushButton("вправо")
        self.rotate_right_button.clicked.connect(self.rotate_right)
        self.red_button = QPushButton("R")
        self.red_button.clicked.connect(lambda: self.change_color_channel('R'))
        self.green_button = QPushButton("G")
        self.green_button.clicked.connect(lambda: self.change_color_channel('G'))
        self.blue_button = QPushButton("B")
        self.blue_button.clicked.connect(lambda: self.change_color_channel('B'))

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.opacity_slider)
        hbox1.addWidget(self.open_button)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.rotate_left_button)
        hbox2.addWidget(self.rotate_right_button)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.red_button)
        hbox3.addWidget(self.green_button)
        hbox3.addWidget(self.blue_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)

        self.pixmap = None
        self.angle = 0

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.pixmap = QPixmap(file_path)
            self.image_label.setPixmap(self.pixmap)

    def change_opacity(self):
        if self.pixmap:
            image = self.pixmap.toImage().convertToFormat(QImage.Format.Format_ARGB32)
            new_image = QImage(image.size(), QImage.Format.Format_ARGB32)
            for x in range(image.width()):
                for y in range(image.height()):
                    color = image.pixelColor(x, y)
                    new_color = QColor(color.red(), color.green(), color.blue(), self.opacity_slider.value())
                    new_image.setPixelColor(x, y, new_color)

            self.image_label.setPixmap(QPixmap.fromImage(new_image))

    def rotate_left(self):
        if self.pixmap:
            self.angle -= 90
            transform = QTransform().rotate(self.angle)
            self.image_label.setPixmap(self.pixmap.transformed(transform))

    def rotate_right(self):
        if self.pixmap:
            self.angle += 90
            transform = QTransform().rotate(self.angle)
            self.image_label.setPixmap(self.pixmap.transformed(transform))

    def change_color_channel(self, channel):
        if self.pixmap:
            image = self.pixmap.toImage()
            if image.format() == QImage.Format.Format_RGB32:
                new_image = QImage(image.size(), QImage.Format.Format_RGB32)
                for x in range(image.width()):
                    for y in range(image.height()):
                        color = image.pixelColor(x, y)
                        if channel == 'R':
                            new_image.setPixelColor(x, y, QColor(color.red(), 0, 0))
                        elif channel == 'G':
                            new_image.setPixelColor(x, y, QColor(0, color.green(), 0))
                        elif channel == 'B':
                            new_image.setPixelColor(x, y, QColor(0, 0, color.blue()))

                self.image_label.setPixmap(QPixmap.fromImage(new_image))

    def reset_color_channel(self):
        if self.pixmap:
            self.image_label.setPixmap(self.pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec())