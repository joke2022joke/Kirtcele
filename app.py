import sys
from PyQt5.QtWidgets import QApplication

from ui.windows import LoginWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec())
