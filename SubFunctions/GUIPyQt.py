import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyqt5_tools import *

class GUIPyQt:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.window()

    def window(self):
        app = QApplication(sys.argv)
        w = QWidget()
        b = QLabel(w)
        button = QPushButton(w)
        button.setText("Test Button")
        button.move(50, 20)
        b.setText("Hello World")
        w.setGeometry(100, 100, 200, 50)
        b.move(20, 20)
        w.setWindowTitle("PyQt5")
        w.show()
        sys.exit(app.exec_())

    def UILoad(self):
        app = QApplication(sys.argv)
        ui_file = QFile("TestUI.ui")
        # loader = QUiLoader()