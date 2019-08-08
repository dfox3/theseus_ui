import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QToolTip, QMessageBox, QLabel, QWidget)
from PyQt5.QtGui import QIcon, QPixmap

class MakeLibraries(QWidget):
    def __init__(self, parent=None):
        super(MakeLibraries, self).__init__()
        self.style = "background-color: #000000"
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #self.setupUi(self)