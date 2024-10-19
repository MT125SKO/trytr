import traceback
from PyQt6.QtWidgets import QApplication
from app.mainWin import MainWin
import sys


def handly_except_hook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)


sys.excepthook = handly_except_hook

def main():
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
