import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QLabel, QButtonGroup, QHBoxLayout, QLabel, QMessageBox
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from functools import partial
from time import sleep
import datetime

MAKE_LIBRARIES = 1
RESULTS = 2
TOOLS = 3
HOME = -1
LIBRARY = -1
BARCODE = DNA_SEQ = 1
CARTRIDGE = RNA_SEQ = 2
REAGENT = PG_SEQ = 3

LIGHTEST_GREY = QColor()
LIGHTEST_GREY.setNamedColor('#f9f9f9')
RED = QColor()
RED.setNamedColor('#CF6464')
BLUE = QColor()
BLUE.setNamedColor('#287acc')

WAIT = 5

WELLS = ["A1", "C1", "E1", "G1", "I1", "K1", "L1", "M1"]

LIBRARIES = ["DNA-Seq", "RNA-Seq", "PG-Seq"]

GREYED_STYLE = "QPushButton { border-style: outset;\
                                         border-width: 1px;\
                                         border-radius: 7px;\
                                         border-color: #363636;\
                                         padding: 4px;\
                                         font-size: 20px;\
                                         color: #1F1F1F;\
                                         background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #E9E9E9, stop:0.7 #CACACA, stop:1 #D5D5D5)}\
                           QPushButton:pressed { background-color: #CACACA;\
                                                 border-style: inset;\
                                                 border-color: gray}"
GREYED_STYLE_UNCLICK = "QPushButton { border-style: outset;\
                                         border-width: 1px;\
                                         border-radius: 7px;\
                                         border-color: #363636;\
                                         padding: 4px;\
                                         font-size: 20px;\
                                         color: gray;\
                                         background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #E9E9E9, stop:0.7 #CACACA, stop:1 #D5D5D5)}\
                           QPushButton:pressed { background-color: #CACACA;\
                                                 border-style: inset;\
                                                 border-color: gray}"
GREYED_STYLE_SMALL_FONT = "QPushButton { border-style: outset;\
                                         border-width: 1px;\
                                         border-radius: 3px;\
                                         border-color: #363636;\
                                         padding: 4px;\
                                         font-size: 16px;\
                                         color: #1F1F1F;\
                                         background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #E9E9E9, stop:0.7 #CACACA, stop:1 #D5D5D5)}\
                           QPushButton:pressed { background-color: #CACACA;\
                                                 border-style: inset;\
                                                 border-color: gray}"
GREYED_STYLE_UNCLICK_SMALL_FONT = "QPushButton { border-style: outset;\
                                         border-width: 1px;\
                                         border-radius: 3px;\
                                         border-color: #363636;\
                                         padding: 4px;\
                                         font-size: 16px;\
                                         color: gray;\
                                         background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #E9E9E9, stop:0.7 #CACACA, stop:1 #D5D5D5)}\
                           QPushButton:pressed { background-color: #CACACA;\
                                                 border-style: inset;\
                                                 border-color: gray}"
SMALL_GREYED_STYLE = "QPushButton { border-style: outset;\
                                         border-width: 1px;\
                                         border-radius: 3px;\
                                         border-color: #363636;\
                                         padding: 4px;\
                                         font-size: 14px;\
                                         color: #1F1F1F;\
                                         background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #E9E9E9, stop:0.7 #CACACA, stop:1 #D5D5D5)}\
                           QPushButton:pressed { background-color: #CACACA;\
                                                 border-style: inset;\
                                                 border-color: gray}"

GREEN_STYLE = "QPushButton { border-style: outset;\
                                         border-width: 1px;\
                                         border-radius: 7px;\
                                         border-color: #363636;\
                                         padding: 4px;\
                                         font-size: 20px;\
                                         color: #1F1F1F;\
                                         background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #9AFF9A, stop:0.7 #5AB45A, stop:1 #60C260)}\
                           QPushButton:pressed { background-color: #5AB45A;\
                                                 border-style: inset;\
                                                 border-color: gray}"
YELLOW_STYLE = "QPushButton {  border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 7px;\
                                             border-color: #363636;\
                                             padding: 4px;\
                                             font-size: 20px;\
                                             color: #1F1F1F;\
                                             background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #F8FF8E, stop:0.7 #D3DB58, stop:1 #DEE65D)}\
                                QPushButton:pressed { background-color: #D3DB58;\
                                                      border-style: inset;\
                                                      border-color: gray}"
RED_STYLE = "QPushButton {  border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 7px;\
                                             border-color: #363636;\
                                             padding: 4px;\
                                             font-size: 20px;\
                                             color: #1F1F1F;\
                                             background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #FF9393, stop:0.7 #CF6464, stop:1 #DA6A6A)}\
                                QPushButton:pressed { background-color: #CF6464;\
                                                      border-style: inset;\
                                                      border-color: gray}"
RED_STYLE_SMALL_FONT = "QPushButton {  border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 3px;\
                                             border-color: #363636;\
                                             padding: 4px;\
                                             font-size: 16px;\
                                             color: #1F1F1F;\
                                             background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #FF9393, stop:0.7 #CF6464, stop:1 #DA6A6A)}\
                                QPushButton:pressed { background-color: #CF6464;\
                                                      border-style: inset;\
                                                      border-color: gray}"
BG_STYLE_SMALL_FONT = "QPushButton {  border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 3px;\
                                             border-color: #363636;\
                                             padding: 4px;\
                                             font-size: 16px;\
                                             color: gray;\
                                             background-color: #1F1F1F}\
                           QPushButton:pressed { border-style: inset;\
                                                      border-color: gray}"


RED_CIRCLE_STYLE = "QPushButton {    border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 60px;\
                                             border-color: #363636;\
                                             padding: 4px;\
                                             font-size: 20px;\
                                             color: #1F1F1F;\
                                             background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #FF9393, stop:0.7 #CF6464, stop:1 #DA6A6A)}\
                                QPushButton:pressed { background-color: #CF6464;\
                                                      border-style: inset;\
                                                      border-color: gray}"
BLUE_STYLE = "QPushButton {    border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 7px;\
                                             border-color: #363636;\
                                             padding: 4px;\
                                             font-size: 20px;\
                                             color: #1F1F1F;\
                                            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #3399FF, stop:0.7 #287acc, stop:1 #2d89e5)}\
                                QPushButton:pressed { background-color: #287acc;\
                                                      border-style: inset;\
                                                      border-color: gray}"

GREYED_CIRCLE_STYLE = "QPushButton {    border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 60px;\
                                             border-color: #363636;\
                                             padding: 4px;\
                                             font-size: 20px;\
                                             color: #1F1F1F;\
                                             background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #E9E9E9, stop:0.7 #CACACA, stop:1 #D5D5D5)}\
                           QPushButton:pressed { background-color: #CACACA;\
                                                      border-style: inset;\
                                                      border-color: gray}"
GREYED_CIRCLE_UNCLICK_STYLE = "QPushButton {    border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 60px;\
                                             border-color: #363636;\
                                             padding: 4px;\
                                             font-size: 20px;\
                                             color: gray;\
                                             background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #E9E9E9, stop:0.7 #CACACA, stop:1 #D5D5D5)}\
                           QPushButton:pressed { background-color: #CACACA;\
                                                      border-style: inset;\
                                                      border-color: gray}"
YELLOW_LIGHT_STYLE = "border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 15px;\
                                             border-color: #363636;\
                                             padding: 10px;\
                                             background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #F8FF8E, stop:0.7 #D3DB58, stop:1 #DEE65D)}"
RED_LIGHT_STYLE = "border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 15px;\
                                             border-color: #363636;\
                                             padding: 10px;\
                                             background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #FF9393, stop:0.7 #CF6464, stop:1 #DA6A6A)}"
BLUE_LIGHT_STYLE = "border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 15px;\
                                             border-color: #363636;\
                                             padding: 10px;\
                                             background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #3399FF, stop:0.7 #287acc, stop:1 #2d89e5)}"
GREY_LIGHT_STYLE = "border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 15px;\
                                             border-color: #363636;\
                                             padding: 10px;\
                                             background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #E9E9E9, stop:0.7 #CACACA, stop:1 #D5D5D5)}"
CHECK_BUTTON_GREY_STYLE = "QPushButton {    border-style: outset;\
                                             border-width: 1px;\
                                             border-radius: 20px;\
                                             border-color: #363636;\
                                             padding: 10px;\
                                             background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #E9E9E9, stop:0.7 #CACACA, stop:1 #D5D5D5)}\
                           QPushButton:pressed { background-color: #CACACA;\
                                                      border-style: inset;\
                                                      border-color: gray}"
DROPDOWN = "QComboBox {\
                                            border: 1px solid gray;\
                                            border-radius: 3px;\
                                            padding: 1px 18px 1px 3px;\
                                            min-width: 6em;\
                                            color: white;\
                                        }\
\
                                        QComboBox:!editable, QComboBox::drop-down:editable {\
                                             background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                                                         stop: 0 #1F1F1F, stop: 0.4 #1F1F1F,\
                                                                         stop: 0.5 #1F1F1F, stop: 1.0 #1F1F1F);\
                                        }\
\
                                        QComboBox:!editable:on, QComboBox::drop-down:editable:on {\
                                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                                                        stop: 0 #1F1F1F, stop: 0.4 #1F1F1F,\
                                                                        stop: 0.5 #1F1F1F, stop: 1.0 #1F1F1F);\
                                        }\
\
                                        QComboBox:on {\
                                            padding-top: 3px;\
                                            padding-left: 4px;\
                                        }\
\
                                        QComboBox::drop-down {\
                                            subcontrol-origin: padding;\
                                            subcontrol-position: top right;\
                                            width: 30px;\
\
                                            border-left-width: 1px;\
                                            border-left-color: darkgray;\
                                            border-left-style: solid; \
                                            border-top-right-radius: 3px; \
                                            border-bottom-right-radius: 3px;\
                                            color: white;\
                                        }\
\
                                        QComboBox::down-arrow:on { \
                                            top: 1px;\
                                            left: 1px;}\
                                        QComboBox QAbstractItemviewResults {\
                                            border: 2px solid darkgray;\
                                            selection-background-color: lightgray;\
                                        }"
DROPDOWN_GREYED = "QComboBox {\
                                            border: 0px solid gray;\
                                            border-radius: 3px;\
                                            padding: 1px 18px 1px 3px;\
                                            min-width: 6em;\
                                            color: white;\
                                        }\
\
                                        QComboBox:!editable, QComboBox::drop-down:editable {\
                                             background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                                                         stop: 0 #1F1F1F, stop: 0.4 #1F1F1F,\
                                                                         stop: 0.5 #1F1F1F, stop: 1.0 #1F1F1F);\
                                        }\
\
                                        QComboBox:!editable:on, QComboBox::drop-down:editable:on {\
                                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                                                        stop: 0 #1F1F1F, stop: 0.4 #1F1F1F,\
                                                                        stop: 0.5 #1F1F1F, stop: 1.0 #1F1F1F);\
                                        }\
\
                                        QComboBox:on {\
                                            padding-top: 3px;\
                                            padding-left: 4px;\
                                        }\
\
                                        QComboBox::drop-down {\
                                            subcontrol-origin: padding;\
                                            subcontrol-position: top right;\
                                            width: 30px;\
\
                                            border-left-width: 0px;\
                                            border-left-color: darkgray;\
                                            border-left-style: solid; \
                                            border-top-right-radius: 3px; \
                                            border-bottom-right-radius: 3px;\
                                            color: white;\
                                        }\
\
                                        QComboBox::down-arrow:off { \
                                            top: 0px;\
                                            left: 0px;}\
                                        QComboBox QAbstractItemviewResults {\
                                            border: 0px solid darkgray;\
                                            selection-background-color: lightgray;\
                                        }"

LABELS = "QLabel {font: bold 18px;\
                border: 0px solid gray;}"
GREY_LABELS = "QLabel {font: bold 18px;\
                border: 0px solid gray;\
                color: #E9E9E9}"
GREEN_LABELS = "QLabel {font: bold 18px;\
                border: 0px solid #9AFF9A;\
                color: #9AFF9A}"
BLUE_LABELS = "QLabel {font: bold 18px;\
                border: 0px solid #3399FF;\
                color: #3399FF}"
YELLOW_LABELS = "QLabel {font: bold 18px;\
                border: 0px solid #F8FF8E;\
                color: #F8FF8E}"

UNCHECKED_GREY_BUTTON = "QPushButton { border-style: outset;\
                                         border-width: 1px;\
                                         border-radius: 7px;\
                                         border-color: #363636;\
                                         padding: 4px;\
                                         font-size: 20px;\
                                         color: #1F1F1F;\
                                         background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #E9E9E9, stop:0.7 #CACACA, stop:1 #D5D5D5)}\
                           QPushButton:pressed { background-color: #CACACA;\
                                                 border-style: inset;\
                                                 border-color: gray}"
CHECK_BUTTON_STYLE = "QPushButton { border-style: outset;\
                                         border-width: 1px;\
                                         border-radius: 7px;\
                                         border-color: #363636;\
                                         padding: 4px;\
                                         font-size: 20px;\
                                         color: #1F1F1F;\
                                         background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #9AFF9A, stop:0.7 #5AB45A, stop:1 #60C260)}\
                           QPushButton:pressed { background-color: #5AB45A;\
                                                 border-style: inset;\
                                                 border-color: gray}"

TABLE_STYLE = "QTableWidget\
    {\
    border:2px groove #96A8A8;\
    border-radius:3px;\
    selection-background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                             stop: 0 #D7F4F7, stop: 0.4 #CEECF0,\
                             stop: 0.6 #C5E4E8, stop: 1.0 #D7F4F7);\
    selection-color:black;\
    }\
    QTableWidget QHeaderView::section\
    {\
    border-bottom:0px groove #8BA6D9;\
    border-left:0px groove #8BA6D9;\
    border-right:2px groove #8BA6D9;\
    border-top:0px;\
    padding:5px;\
    background:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                             stop: 0 #F8FCFE, stop: 0.4 #EBEEF2,\
                             stop: 0.5 #E0E5EA, stop: 1.0 #DADEEA);\
    color:black;\
    outline:0px;\
    }\
    QTableWidget::item\
    {\
    padding:5px;\
    outline:0px;\
    }"

class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.library = -1

        self.title = "Theseus UI"
        self.top = 100
        self.left = 100
        self.width = 1000
        self.height = 750 
        self.icon_name = "icon.png"
        self.logo_name = "logo2.png"
        self.plate_name = "plate.png"

        self.style = "background-color: #1F1F1F"
        self.widget_style = "background-color: #1F1F1F; border: 1px solid gray; border-radius: 3px; color: white; font: 12px"
        self.widget_style2 = "background-color: #1F1F1F; border: 0px solid gray; border-radius: 3px; color: white; font: 12px"
        self.widget_style3 = "background-color: #ffffff; border: 0px solid gray; border-radius: 3px; color: black; font: 12px"

        self.button_width_1 = 120
        self.button_height_1 = 100 
        self.button_width_2 = 120
        self.button_height_2 = 120 

        self.check_button_w = 30
        self.check_button_h = 30 
        self.check_button_margins = 10
        
        self.home_margins = 50
        self.greyed_style = GREYED_STYLE_UNCLICK
        self.home_styles = [GREEN_STYLE, YELLOW_STYLE, RED_CIRCLE_STYLE]
        self.greyed_circle_style = GREYED_CIRCLE_UNCLICK_STYLE
        #self.check_button_style = CHECK_BUTTON_STYLE
        #self.check_button_grey_style = CHECK_BUTTON_GREY_STYLE

        self.light_state1 = GREY_LIGHT_STYLE
        self.light_state2 = BLUE_LIGHT_STYLE

        self.barcode_button_style = [GREEN_STYLE, GREEN_LABELS]
        self.cartridge_button_style = [GREYED_STYLE, GREY_LABELS]
        self.reagent_button_style = [GREYED_STYLE_UNCLICK, GREY_LABELS]

        
        self.time = WAIT
        self.timer = self.getTime()

        self.initWindow()



    def initWindow(self):
        
        self.setWindowIcon(QtGui.QIcon(self.icon_name))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        self.setStyleSheet(self.style)
        self.loadLibraryWidgets()
        self.loadHomePanel()
        self.show()



    def loadHomePanel(self):
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(self.logo_name))
        self.label.setGeometry(QRect(self.home_margins,
                                 self.home_margins/2,
                                 self.button_width_2,
                                 self.button_height_2))
        self.label.setToolTip("For the Better")


        self.parent_hbox = QHBoxLayout()
        
        self.make_button = QPushButton("Make\nLibraries",self)
        self.make_button.setStyleSheet(self.home_styles[MAKE_LIBRARIES-1])
        self.make_button.setGeometry(QRect(self.home_margins,
                                 self.height-self.home_margins-(3*self.button_height_1+2*self.home_margins)-100,
                                 self.button_width_1,
                                 self.button_height_1))
        self.make_button.setToolTip("Begin Theseus initializing process.")
        self.parent_hbox.addWidget(self.make_button)
        self.make_button.clicked.connect(partial(self.display,MAKE_LIBRARIES))

        self.viewResults_button = QPushButton("View\nResults",self)
        self.viewResults_button.setStyleSheet(self.home_styles[RESULTS-1])
        self.viewResults_button.setGeometry(QRect(self.home_margins,
                                 self.height-self.home_margins-(2*self.button_height_1+self.home_margins)-100,
                                 self.button_width_1,
                                 self.button_height_1))
        self.viewResults_button.setToolTip("View results of previous Theseus runs.")
        self.parent_hbox.addWidget(self.viewResults_button)
        self.viewResults_button.clicked.connect(partial(self.display,RESULTS))

        self.tools_button = QPushButton("Tools",self)
        self.tools_button.setStyleSheet(self.home_styles[TOOLS-1])
        self.tools_button.setGeometry(QRect(self.home_margins,
                                 self.height-self.home_margins-self.button_height_1-100,
                                 self.button_width_2,
                                 self.button_height_2))
        self.tools_button.setToolTip("Configure Theseus")
        self.parent_hbox.addWidget(self.tools_button)
        self.tools_button.clicked.connect(partial(self.display,TOOLS))



    
    def display(self, current_pane):
        if current_pane == MAKE_LIBRARIES:
            if self.viewResults_button.isEnabled():
                self.make_button.setStyleSheet(self.home_styles[MAKE_LIBRARIES-1])
                self.viewResults_button.setStyleSheet(self.greyed_style)
                self.tools_button.setStyleSheet(self.greyed_circle_style)
                self.viewResults_button.setDisabled(True)
                self.tools_button.setDisabled(True)
                self.lib_widget1.show()
                if self.time == 0:
                    self.lib_widget3.show()
                else:
                    if self.combo_box1.currentText() != "-":
                        self.lib_widget2.show()
            else:
                self.make_button.setStyleSheet(self.home_styles[MAKE_LIBRARIES-1])
                self.viewResults_button.setStyleSheet(self.home_styles[viewResults_RESULTS-1])
                self.tools_button.setStyleSheet(self.home_styles[tools-1])
                self.viewResults_button.setDisabled(False)
                self.tools_button.setDisabled(False)
                self.lib_widget1.hide()
                self.lib_widget2.hide()
                self.lib_widget3.hide()
            #self.Library()
        elif current_pane == viewResults_RESULTS:
            if self.viewResults_button.isEnabled():
                self.make_button.setStyleSheet(self.greyed_style)
                self.viewResults_button.setStyleSheet(self.home_styles[viewResults_RESULTS-1])
                self.tools_button.setStyleSheet(self.greyed_circle_style)
                self.make_button.setDisabled(True)
                self.tools_button.setDisabled(True)
            else:
                self.make_button.setStyleSheet(self.home_styles[MAKE_LIBRARIES-1])
                self.viewResults_button.setStyleSheet(self.home_styles[viewResults_RESULTS-1])
                self.tools_button.setStyleSheet(self.home_styles[tools-1])
                self.make_button.setDisabled(False)
                self.tools_button.setDisabled(False)
            self.viewResults()
        elif current_pane == tools:
            if self.viewResults_button.isEnabled():
                self.make_button.setStyleSheet(self.greyed_style)
                self.viewResults_button.setStyleSheet(self.greyed_style)
                self.tools_button.setStyleSheet(self.home_styles[tools-1])
                self.make_button.setDisabled(True)
                self.viewResults_button.setDisabled(True)
            else:
                self.make_button.setStyleSheet(self.home_styles[MAKE_LIBRARIES-1])
                self.viewResults_button.setStyleSheet(self.home_styles[viewResults_RESULTS-1])
                self.tools_button.setStyleSheet(self.home_styles[tools-1])
                self.make_button.setDisabled(False)
                self.viewResults_button.setDisabled(False)
            self.tools()
        elif current_pane == HOME:
            print("home is where you make it")

    

    def loadLibraryWidgets(self):
        #-----------------------------------------------
        # widget1

        self.lib_widget1 = QWidget(self)
        self.lib_widget1.hide()
        self.lib_widget1.setGeometry(self.left+120, 10, self.width, self.height)
        self.lib_widget1.setStyleSheet(self.widget_style)

        self.lib_light1 = QWidget(self.lib_widget1)
        self.lib_light1.setStyleSheet(self.light_state1)
        self.lib_light1.setGeometry(QRect(37, 60, self.check_button_w, self.check_button_h))

        self.combo_box1 = QtWidgets.QComboBox(self.lib_widget1)
        self.combo_box1.setGeometry(QRect(80, 60, 200, 30))
        self.combo_box1.setObjectName("combo_box1")
        self.combo_box1.addItem("-")
        self.combo_box1.addItem("DNA-Seq")
        self.combo_box1.addItem("RNA-Seq")
        self.combo_box1.addItem("PG-Seq")
        self.combo_box1.setStyleSheet(DROPDOWN)

        self.lib_label1 = QLabel(self.lib_widget1)
        self.lib_label1.setText("Library:")
        self.lib_label1.setGeometry(QRect(80, 30, 200, 25))
        self.lib_label1.setStyleSheet(LABELS)

        self.lib_light2 = QWidget(self.lib_widget1)
        self.lib_light2.setStyleSheet(self.light_state2)
        self.lib_light2.setGeometry(QRect(427, 60, self.check_button_w, self.check_button_h))

        self.combo_box2 = QtWidgets.QComboBox(self.lib_widget1)
        self.combo_box2.setGeometry(QRect(470, 60, 200, 30))
        self.combo_box2.setObjectName("combo_box2")
        self.combo_box2.addItem("Genomic DNA")
        self.combo_box2.addItem("10 uL Blood")
        self.combo_box2.setStyleSheet(DROPDOWN)

        self.lib_label2 = QLabel(self.lib_widget1)
        self.lib_label2.setText("Sample Type:")
        self.lib_label2.setGeometry(QRect(470, 30, 200, 25))
        self.lib_label2.setStyleSheet(LABELS)

        self.combo_box1.currentIndexChanged.connect(self.updateLight)
        self.combo_box2.currentIndexChanged.connect(self.updateLight)

        # reset button
        self.reset_button = QPushButton("Reset",self.lib_widget1)
        self.reset_button.setStyleSheet(RED_STYLE_SMALL_FONT)
        self.reset_button.setGeometry(QRect(37,700,60,30))
        self.reset_button.clicked.connect(self.reset)
        # question button
        self.question_button = QPushButton("?",self.lib_widget1)
        self.question_button.setStyleSheet(BG_STYLE_SMALL_FONT)
        self.question_button.setGeometry(QRect(self.width - (self.left+120) - 37,700,30,30))
        self.question_button.clicked.connect(self.question)

        # forwards and backwards buttons
        '''
        self.forward_backward_widget = QWidget(self.lib_widget1)
        self.forward_backward_widget.hide()
        self.forward_backward_widget.setGeometry(QRect((self.width/2)-50-120,700,100,30))
        self.forward_backward_widget.setStyleSheet(self.widget_style2)
        self.back_button = QPushButton("Back",self.forward_backward_widget)
        self.back_button.setStyleSheet(GREYED_STYLE_UNCLICK_SMALL_FONT)
        self.back_button.setGeometry(QRect(0,0,40,30))
        self.back_button.clicked.connect(self.back)
        self.next_button = QPushButton("Next",self.forward_backward_widget)
        self.next_button.setStyleSheet(GREYED_STYLE_SMALL_FONT)
        self.next_button.setGeometry(QRect(60,0,40,30))
        self.next_button.clicked.connect(self.back)
        '''

        #-----------------------------------------------
        # widget2

        self.lib_widget2 = QWidget(self)
        self.lib_widget2.hide()
        self.lib_widget2.setGeometry(self.left+121,100, self.width, self.height-300)
        self.lib_widget2.setStyleSheet(self.widget_style2)

        # edit barcode button when barcode scanner is implemented
        self.barcode_button = QPushButton("",self.lib_widget2)
        self.barcode_button.setStyleSheet(self.barcode_button_style[0])
        self.barcode_button.setGeometry(QRect(self.home_margins,self.home_margins,40,40))
        self.barcode_button.clicked.connect(partial(self.loadingStep,BARCODE))
        
        self.barcode_button_label = QLabel(self.lib_widget2)
        self.barcode_button_label.setText("Open microfluidic chip and scan barcode.\nPlace the chip in Theseus.")
        self.barcode_button_label.setGeometry(QRect(self.home_margins + 50 + 25,self.home_margins,400,40))
        self.barcode_button_label.setStyleSheet(self.barcode_button_style[1])

        # edit cartridge button when cartridge scanner is implemented
        self.cartridge_button = QPushButton("",self.lib_widget2)
        self.cartridge_button.setStyleSheet(self.cartridge_button_style[0])
        self.cartridge_button.setGeometry(QRect(self.home_margins,self.home_margins*3,40,40))
        self.cartridge_button.setDisabled(True)
        self.cartridge_button.clicked.connect(partial(self.loadingStep,CARTRIDGE))
        
        self.cartridge_button_label = QLabel(self.lib_widget2)
        self.cartridge_button_label.setText("Open PCR cartridge and place in Theseus.")
        self.cartridge_button_label.setGeometry(QRect(self.home_margins + 50 + 25,self.home_margins*3,400,40))
        self.cartridge_button_label.setStyleSheet(self.cartridge_button_style[1])

        # edit reagent button when reageny scanner is implemented
        self.reagent_button = QPushButton("",self.lib_widget2)
        self.reagent_button.setStyleSheet(self.reagent_button_style[0])
        self.reagent_button.setGeometry(QRect(self.home_margins,self.home_margins*5,40,40))
        self.reagent_button.setDisabled(True)
        self.reagent_button.clicked.connect(partial(self.loadingStep,REAGENT))
        
        self.reagent_button_label = QLabel(self.lib_widget2)
        self.reagent_button_label.setText("Open reagent plate and scan.\nPlace it on lab bench.\nClick Timer.")
        self.reagent_button_label.setGeometry(QRect(self.home_margins + 50 + 25,self.home_margins*5,400,60))
        self.reagent_button_label.setStyleSheet(self.reagent_button_style[1])

        #add timer
        self.timer_button = QPushButton(str(self.timer),self.lib_widget2)
        self.timer_button.setStyleSheet(self.reagent_button_style[0])
        self.timer_button.setGeometry(QRect(self.home_margins + 50 + 25,self.home_margins*7,125,80))
        self.timer_button.setDisabled(True)
        self.timer_button.clicked.connect(partial(self.loadingStep,REAGENT))

        self.my_qtimer = QtCore.QTimer(self)
        self.my_qtimer.timeout.connect(self.timerTimeout)


        #-----------------------------------------------
        # widget3.1 - plate
        self.lib_widget3 = QWidget(self)
        self.lib_widget3.hide()
        self.lib_widget3.setGeometry(self.left+121,100, self.width, self.height-150)
        self.lib_widget3.setStyleSheet(self.widget_style2)

        self.barcode_button_shell = QPushButton(u'\u2713',self.lib_widget3)
        self.barcode_button_shell.setStyleSheet(GREEN_STYLE)
        self.barcode_button_shell.setGeometry(QRect(37,20,40,40))
        self.barcode_button_shell.setDisabled(True)

        self.cartridge_button_shell = QPushButton(u'\u2713',self.lib_widget3)
        self.cartridge_button_shell.setStyleSheet(BLUE_STYLE)
        self.cartridge_button_shell.setGeometry(QRect(37+self.home_margins,20,40,40))
        self.cartridge_button_shell.setDisabled(True)

        self.reagent_button_shell = QPushButton(u'\u2713',self.lib_widget3)
        self.reagent_button_shell.setStyleSheet(YELLOW_STYLE)
        self.reagent_button_shell.setGeometry(QRect(37+self.home_margins*2,20,40,40))
        self.reagent_button_shell.setDisabled(True)

        self.lib_widget3_mini1 = QWidget(self.lib_widget3)
        self.lib_widget3_mini1.setGeometry(37,80,680,488)
        self.lib_widget3_mini1.setStyleSheet(self.widget_style2)

        self.plate_label = QLabel(self.lib_widget3_mini1)
        self.plate_label.setText("Load 10uL DNA (A1, C1, E1, G1, I1, K1, M1, O1).")
        self.plate_label.setGeometry(QRect(0,0,680,20))
        self.plate_label.setStyleSheet(LABELS)

        self.plate = QLabel(self.lib_widget3_mini1)
        self.plate.setPixmap(QPixmap(self.plate_name))
        self.plate.setGeometry(QRect(0,20,680,468))
        self.plate.setToolTip("Reagent plate map")

        self.a1_button = QPushButton("",self.lib_widget3_mini1)
        self.a1_button.setStyleSheet(SMALL_GREYED_STYLE)
        self.a1_button.setGeometry(QRect(self.home_margins+31-37,135-80,20,20))
        self.a1_button.clicked.connect(partial(self.clickPlateButton,0))

        self.c1_button = QPushButton("",self.lib_widget3_mini1)
        self.c1_button.setStyleSheet(SMALL_GREYED_STYLE)
        self.c1_button.setGeometry(QRect(self.home_margins+31-37,185-80,20,20))
        self.c1_button.clicked.connect(partial(self.clickPlateButton,1))

        self.e1_button = QPushButton("",self.lib_widget3_mini1)
        self.e1_button.setStyleSheet(SMALL_GREYED_STYLE)
        self.e1_button.setGeometry(QRect(self.home_margins+31-37,235-80,20,20))
        self.e1_button.clicked.connect(partial(self.clickPlateButton,2))

        self.g1_button = QPushButton("",self.lib_widget3_mini1)
        self.g1_button.setStyleSheet(SMALL_GREYED_STYLE)
        self.g1_button.setGeometry(QRect(self.home_margins+31-37,285-80,20,20))
        self.g1_button.clicked.connect(partial(self.clickPlateButton,3))

        self.i1_button = QPushButton("",self.lib_widget3_mini1)
        self.i1_button.setStyleSheet(SMALL_GREYED_STYLE)
        self.i1_button.setGeometry(QRect(self.home_margins+31-37,335-80,20,20))
        self.i1_button.clicked.connect(partial(self.clickPlateButton,4))

        self.k1_button = QPushButton("",self.lib_widget3_mini1)
        self.k1_button.setStyleSheet(SMALL_GREYED_STYLE)
        self.k1_button.setGeometry(QRect(self.home_margins+31-37,385-80,20,20))
        self.k1_button.clicked.connect(partial(self.clickPlateButton,5))

        self.m1_button = QPushButton("",self.lib_widget3_mini1)
        self.m1_button.setStyleSheet(SMALL_GREYED_STYLE)
        self.m1_button.setGeometry(QRect(self.home_margins+31-37,435-80,20,20))
        self.m1_button.clicked.connect(partial(self.clickPlateButton,6))

        self.o1_button = QPushButton("",self.lib_widget3_mini1)
        self.o1_button.setStyleSheet(SMALL_GREYED_STYLE)
        self.o1_button.setGeometry(QRect(self.home_margins+31-37,485-80,20,20))
        self.o1_button.clicked.connect(partial(self.clickPlateButton,7))
        
        #-----------------------------------------------
        # widget3.2 sample spreadsheet
        
        self.lib_widget3_mini2 = QWidget(self.lib_widget3)
        self.lib_widget3_mini2.hide()
        self.lib_widget3_mini2.setGeometry(37,80,680,488)
        self.lib_widget3_mini2.setStyleSheet(self.widget_style2)        
        

        # spreadsheet
        self.lib_widget3_mini2_1 = QWidget(self.lib_widget3_mini2)
        self.lib_widget3_mini2_1.show()
        self.lib_widget3_mini2_1.setGeometry(0,40,680,325)
        self.lib_widget3_mini2_1.setStyleSheet(self.widget_style3)
        
        self.sample_table_label = QLabel(self.lib_widget3_mini2)
        self.sample_table_label.setText("Place plate in Theseus and enter information into sheet below.")
        self.sample_table_label.setGeometry(QRect(0,0,680,20))
        self.sample_table_label.setStyleSheet(LABELS)

        self.sample_table = QTableWidget(8,5,self.lib_widget3_mini2_1)
        self.sample_table.setStyleSheet(TABLE_STYLE)
        self.sample_table.setGeometry(QRect(0,0,680,325))
        self.sample_table.setHorizontalHeaderItem(0,QTableWidgetItem("Well"))
        self.sample_table.setHorizontalHeaderItem(1,QTableWidgetItem("Sample"))
        self.sample_table.setHorizontalHeaderItem(2,QTableWidgetItem("Database"))
        self.sample_table.setHorizontalHeaderItem(3,QTableWidgetItem("Date"))
        self.sample_table.setHorizontalHeaderItem(4,QTableWidgetItem("Notes"))
        self.sample_table_header = self.sample_table.horizontalHeader()       
        self.sample_table_header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.sample_table_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.sample_table_header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.sample_table_header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.sample_table_header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        self.sample_table_rows = self.sample_table.verticalHeader()   
        for i in range(8):
            item = QTableWidgetItem(WELLS[i])
            item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            self.sample_table.setItem(i,0,item)
            self.sample_table.item(i,0).setBackground(LIGHTEST_GREY)
            self.sample_table.item(i,0).setForeground(RED)
            item = QTableWidgetItem("Database update")
            item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            self.sample_table.setItem(i,2,item)
            self.sample_table.item(i,2).setBackground(LIGHTEST_GREY)
            self.sample_table.item(i,2).setForeground(BLUE)
            item = QTableWidgetItem(str(datetime.date.today()))
            item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            self.sample_table.setItem(i,3,item)
            self.sample_table.item(i,3).setBackground(LIGHTEST_GREY)
            self.sample_table_rows.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        # start button
        self.start_button = QPushButton("Run App",self.lib_widget3_mini2)
        self.start_button.setStyleSheet(GREEN_STYLE)
        self.start_button.setGeometry(QRect(340-50,408,100,60))
        self.start_button.clicked.connect(self.run)




        




    def updateLight(self):
        if self.combo_box1.currentText() == "-":
            self.light_state1 = GREY_LIGHT_STYLE
            self.lib_widget2.hide()
        else:
            self.light_state1 = YELLOW_LIGHT_STYLE
            self.lib_widget2.show()
        if self.combo_box2.currentText() == "Genomic DNA":
            self.light_state2 = BLUE_LIGHT_STYLE
            self.plate_label.setText("Load 10uL Genomic DNA (A1, C1, E1, G1, I1, K1, M1, O1).")
        else:
            self.light_state2 = RED_LIGHT_STYLE
            self.plate_label.setText("Load 10uL Blood (A1, C1, E1, G1, I1, K1, M1, O1).")
        self.lib_light1.setStyleSheet(self.light_state1)
        self.lib_light2.setStyleSheet(self.light_state2)
        self.resetWidget2()


    
    def librarySelect(self, current_library):
        if current_library == DNA_SEQ:
            self.lib_button1.setStyleSheet(self.check_button_style)
            self.lib_button2.setStyleSheet(self.check_button_grey_style)
            self.lib_button2.setDisabled(True)
            self.lib_button3.setStyleSheet(self.check_button_grey_style)
            self.lib_button3.setDisabled(True)

        elif current_library == RNA_SEQ:
            self.lib_button1.setStyleSheet(self.check_button_grey_style)
            self.lib_button1.setDisabled(True)
            self.lib_button2.setStyleSheet(self.check_button_style)
            self.lib_button3.setStyleSheet(self.check_button_grey_style)
            self.lib_button3.setDisabled(True)

        elif current_library == PG_SEQ:
            self.lib_button1.setStyleSheet(self.check_button_grey_style)
            self.lib_button1.setDisabled(True)
            self.lib_button2.setStyleSheet(self.check_button_grey_style)
            self.lib_button2.setDisabled(True)
            self.lib_button3.setStyleSheet(self.check_button_style)
        
        elif current_library == LIBRARY:
            print("library is where you make it")
            #self.sampleType()


    def loadingStep(self, current_step):
        if current_step == BARCODE:
            self.barcode_button.setDisabled(True)
            self.barcode_button.setText(u'\u2713')
            
            self.cartridge_button_style = [BLUE_STYLE, BLUE_LABELS]
            self.cartridge_button.setStyleSheet(self.cartridge_button_style[0])
            self.cartridge_button_label.setStyleSheet(self.cartridge_button_style[1])
            self.cartridge_button.setDisabled(False)

            self.combo_box1.setStyleSheet(DROPDOWN_GREYED)
            self.combo_box2.setStyleSheet(DROPDOWN_GREYED)
            self.combo_box1.setEnabled(False)
            self.combo_box2.setEnabled(False)
            
        elif current_step == CARTRIDGE:
            self.cartridge_button.setDisabled(True)
            self.cartridge_button.setText(u'\u2713')
            
            self.reagent_button_style = [YELLOW_STYLE, YELLOW_LABELS]
            self.reagent_button.setStyleSheet(self.reagent_button_style[0])
            self.reagent_button_label.setStyleSheet(self.reagent_button_style[1])
            #self.reagent_button.setDisabled(False)

            self.timer_button.setStyleSheet(self.reagent_button_style[0])
            self.timer_button.setDisabled(False)
           

        elif current_step == REAGENT:
            print("Reagents are ready")

            self.reagent_button.setDisabled(True)
            self.reagent_button.setText(u'\u2713')
            self.timer_button.setDisabled(True)
            self.ticker()

    def clickPlateButton(self, button):
        button_list = [self.a1_button,
                       self.c1_button,
                       self.e1_button,
                       self.g1_button,
                       self.i1_button,
                       self.k1_button,
                       self.m1_button,
                       self.o1_button]
        if button_list[button].text() == "":
            button_list[button].setText(u'\u2713')
        else:
            button_list[button].setText("")

        is_all_checked = True
        i = 0
        while is_all_checked and i < 8:
            if button_list[i].text() == "":
                is_all_checked = False
            i += 1

        if is_all_checked:
            self.lib_widget3_mini1.hide()
            self.lib_widget3_mini2.show()


    def ticker(self):
        self.timer_box = QMessageBox()
        self.timer_box.setIcon(QMessageBox.Question)
        self.timer_box.setText("Are you sure you want to start timer?")
        self.timer_box.setWindowTitle("Start timer")
        self.timer_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        #self.reset_box.buttonClicked.connect(msgButtonClick)
        ret_val = self.timer_box.exec()
        if ret_val == QMessageBox.Yes:
            self.my_qtimer.start(1000)


    def timerTimeout(self):
        if self.time == 0:
            self.my_qtimer.stop()
            self.lib_widget2.hide()
            self.lib_widget3.show()
            #self.forward_backward_widget.show()
        else:
            self.time -= 1
        self.timer_button.setText(f'{self.time//60:02}'+":"+f'{self.time-((self.time//60)*60):02}')


    def back(self):
        print("we back here")

    def run(self):
        self.run_box = QMessageBox()
        self.run_box.setIcon(QMessageBox.Question)
        self.run_box.setText("Are you sure you want to run application?")
        self.run_box.setWindowTitle("Run application")
        self.run_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        #self.reset_box.buttonClicked.connect(msgButtonClick)
        ret_val = self.run_box.exec()
        if ret_val == QMessageBox.Yes:
            print("run app!!")
            self.reset_button.setText("Stop")


    def viewResults(self):
        print("viewResults")
        self.lib_elements_off()

    def tools(self):
        print("tools")
        self.lib_elements_off()

    def reset(self):
        if self.reset_button.text() == "Reset":
            self.reset_box = QMessageBox()
            self.reset_box.setIcon(QMessageBox.Warning)
            self.reset_box.setText("Are you sure you would like to reset \nthe Make Libraries function?")
            self.reset_box.setWindowTitle("Reset button clicked")
            self.reset_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            #self.reset_box.buttonClicked.connect(msgButtonClick)
            ret_val = self.reset_box.exec()
            if ret_val == QMessageBox.Yes:
                print('Yes clicked')
                self.resetWidget1()
        else:
            self.reset_box = QMessageBox()
            self.reset_box.setIcon(QMessageBox.Warning)
            self.reset_box.setText("Are you sure you would like to stop \nthe Theseus run?")
            self.reset_box.setWindowTitle("Stop button clicked")
            self.reset_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            #self.reset_box.buttonClicked.connect(msgButtonClick)
            ret_val = self.reset_box.exec()
            if ret_val == QMessageBox.Yes:
                print('Yes clicked')
                self.resetWidget1()


    def question(self):
        print("question")

    def resetWidget1(self):
        print("resetting 1")
        self.combo_box1.setCurrentIndex(0)
        self.combo_box2.setCurrentIndex(0)
        self.combo_box1.setEnabled(True)
        self.combo_box2.setEnabled(True)
        self.combo_box1.setStyleSheet(DROPDOWN)
        self.combo_box2.setStyleSheet(DROPDOWN)
        self.lib_widget2.hide()
        #self.forward_backward_widget.hide()
        self.reset_button.setText("Reset")
        self.resetWidget2()
        self.resetWidget3()


    def resetWidget2(self):
        print("resetting 2")
        
        self.barcode_button_style = [GREEN_STYLE, GREEN_LABELS]
        self.cartridge_button_style = [GREYED_STYLE, GREY_LABELS]
        self.reagent_button_style = [GREYED_STYLE_UNCLICK, GREY_LABELS]
        
        self.barcode_button.setText("")
        self.barcode_button.setDisabled(False)

        self.cartridge_button.setText("")
        self.cartridge_button.setDisabled(True)
        self.cartridge_button.setStyleSheet(self.cartridge_button_style[0])
        self.cartridge_button_label.setStyleSheet(self.cartridge_button_style[1])

        self.reagent_button.setText("")
        self.reagent_button.setDisabled(True)
        self.reagent_button.setStyleSheet(self.reagent_button_style[0])
        self.reagent_button_label.setStyleSheet(self.reagent_button_style[1])

        self.my_qtimer.stop()
        self.time = WAIT
        self.timer_button.setText(f'{self.time//60:02}'+":"+f'{self.time-((self.time//60)*60):02}')
        self.timer_button.setStyleSheet(self.reagent_button_style[0])
        self.timer_button.setDisabled(True)

        self.lib_widget3.hide()   
        self.resetWidget3()


    def resetWidget3(self):
        print("resetting 3")
        self.plate_label.setText("Load 10uL DNA (A1, C1, E1, G1, I1, K1, M1, O1).")
        button_list = [self.a1_button,
                       self.c1_button,
                       self.e1_button,
                       self.g1_button,
                       self.i1_button,
                       self.k1_button,
                       self.m1_button,
                       self.o1_button]
        for b in button_list:
            b.setText("")
        for i in range(8):
            self.sample_table.setItem(i,1,QTableWidgetItem(""))
            self.sample_table.setItem(i,4,QTableWidgetItem(""))
        self.lib_widget3_mini1.show()
        self.lib_widget3_mini2.hide()



    
    def resetWidget4(self):
        print("resetting 3")
     
    
    def getTime(self):
        minutes = self.time // 60
        seconds = self.time - (60 * minutes)
        str_mins = str(minutes)
        if minutes < 10:
            str_mins = "0" + str(minutes)
        str_secs = str(seconds)
        if seconds < 10:
            str_secs = "0" + str(seconds)
        return str(str_mins) + ":" + str(str_secs)
        

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())

