import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QToolTip, QMessageBox, QLabel)
from PyQt5.QtGui import QIcon, QPixmap

class Tools(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("major Bazinga")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)