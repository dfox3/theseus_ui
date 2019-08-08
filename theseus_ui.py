import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QLabel, QButtonGroup, QHBoxLayout, QLabel
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QRect, QSize, Qt
from functools import partial
from time import sleep

from make_libraries import MakeLibraries

MAKE_LIBRARIES = 1
viewResults_RESULTS = 2
tools = 3
HOME = -1
LIBRARY = -1
BARCODE = DNA_SEQ = 1
CARTRIDGE = RNA_SEQ = 2
REAGENT = PG_SEQ = 3

WAIT = 5

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
                                             border-radius: 7px;\
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
                                             border-radius: 7px;\
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

        self.button_width_1 = 120
        self.button_height_1 = 100 
        self.button_width_2 = 120
        self.button_height_2 = 120 

        self.check_button_w = 30
        self.check_button_h = 30 
        self.check_button_margins = 10
        
        self.home_margins = 50
        self.greyed_style = GREYED_STYLE
        self.home_styles = [GREEN_STYLE, YELLOW_STYLE, RED_CIRCLE_STYLE]
        self.greyed_circle_style = GREYED_CIRCLE_STYLE
        #self.check_button_style = CHECK_BUTTON_STYLE
        #self.check_button_grey_style = CHECK_BUTTON_GREY_STYLE

        self.light_state1 = GREY_LIGHT_STYLE
        self.light_state2 = BLUE_LIGHT_STYLE

        self.barcode_button_style = [GREEN_STYLE, GREEN_LABELS]
        self.cartridge_button_style = [GREYED_STYLE, GREY_LABELS]
        self.reagent_button_style = [GREYED_STYLE, GREY_LABELS]

        
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
        self.viewResults_button.setStyleSheet(self.home_styles[viewResults_RESULTS-1])
        self.viewResults_button.setGeometry(QRect(self.home_margins,
                                 self.height-self.home_margins-(2*self.button_height_1+self.home_margins)-100,
                                 self.button_width_1,
                                 self.button_height_1))
        self.viewResults_button.setToolTip("View results of previous Theseus runs.")
        self.parent_hbox.addWidget(self.viewResults_button)
        self.viewResults_button.clicked.connect(partial(self.display,viewResults_RESULTS))

        self.tools_button = QPushButton("Tools",self)
        self.tools_button.setStyleSheet(self.home_styles[tools-1])
        self.tools_button.setGeometry(QRect(self.home_margins,
                                 self.height-self.home_margins-self.button_height_1-100,
                                 self.button_width_2,
                                 self.button_height_2))
        self.tools_button.setToolTip("Configure Theseus")
        self.parent_hbox.addWidget(self.tools_button)
        self.tools_button.clicked.connect(partial(self.display,tools))



    
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

        #reset button
        self.reset_button = QPushButton("Reset",self.lib_widget1)
        self.reset_button.setStyleSheet(RED_STYLE_SMALL_FONT)
        self.reset_button.setGeometry(QRect(37,700,60,30))
        self.reset_button.clicked.connect(self.reset)
        #question button
        self.question_button = QPushButton("?",self.lib_widget1)
        self.question_button.setStyleSheet(BG_STYLE_SMALL_FONT)
        self.question_button.setGeometry(QRect(self.width - (self.left+120) - 37,700,30,30))
        self.question_button.clicked.connect(self.question)


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
        # widget3
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

        self.label = QLabel(self.lib_widget3)
        self.label.setPixmap(QPixmap(self.plate_name))
        self.label.setGeometry(QRect(37,100,680,468))
        self.label.setToolTip("Reagent plate map")








    def updateLight(self):
        if self.combo_box1.currentText() == "-":
            self.light_state1 = GREY_LIGHT_STYLE
            self.lib_widget2.hide()
        else:
            self.light_state1 = YELLOW_LIGHT_STYLE
            self.lib_widget2.show()
        if self.combo_box2.currentText() == "Genomic DNA":
            self.light_state2 = BLUE_LIGHT_STYLE
        else:
            self.light_state2 = RED_LIGHT_STYLE
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


            #Add line for check mark
            #self.reagent_button_style = [YELLOW_STYLE, YELLOW_LABELS]
            #self.reagent_button.setStyleSheet(self.reagent_button_style[0])
            #self.reagent_button_label.setStyleSheet(self.reagent_button_style[1])
            #self.reagent_button.setDisabled(False)
        
        #elif current_step == TIMER:
            #print("Timer is set")
            #self.sampleType()

    #self.timer = QtCore.QTimer(self)
    #self.timer.timeout.connect(self.ticker)
    #self.timer.start(self.time)

    def ticker(self):
        self.my_qtimer.start(1000)


    def timerTimeout(self):
        if self.time == 0:
            self.my_qtimer.stop()
            self.lib_widget2.hide()
            self.lib_widget3.show()
        else:
            self.time -= 1
        self.timer_button.setText(f'{self.time//60:02}'+":"+f'{self.time-((self.time//60)*60):02}')


    

    def viewResults(self):
        print("viewResults")
        self.lib_elements_off()

    def tools(self):
        print("tools")
        self.lib_elements_off()


    def lib_elements_on(self):
        self.lib_button1.show()
        self.lib_button2.show()
        self.lib_button3.show()
        self.lib_label1.show()
        self.lib_label2.show()
        self.lib_label3.show()


    def lib_elements_off(self):
        self.lib_button1.hide()
        self.lib_button2.hide()
        self.lib_button3.hide()

    def reset(self):
        self.resetWidget1()
        self.resetWidget2()
        self.resetWidget3()

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
        self.lib_widget3.hide()

    def resetWidget2(self):
        print("resetting 2")
        
        self.barcode_button_style = [GREEN_STYLE, GREEN_LABELS]
        self.cartridge_button_style = [GREYED_STYLE, GREY_LABELS]
        self.reagent_button_style = [GREYED_STYLE, GREY_LABELS]
        
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


    def resetWidget3(self):
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

