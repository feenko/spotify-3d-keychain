from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from helpers.gui import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon("assets/images/icon.png"))

    window = MainWindow()
    app.exec()
