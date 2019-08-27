import sys
import os
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QLabel, QButtonGroup, QHBoxLayout, QLabel, QMessageBox
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import QRect, QSize, Qt, QThread, QProcess
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFileDialog
from functools import partial
import datetime
import csv
import pickle
import serial
import serial.tools.list_ports
import glob
import parse
import argparse
#from subprocess import Popen

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
    

LIBRARY_BUTTON = "QPushButton { background-image: url(img/buttons/LIBRARIES1.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/LIBRARIES2.png); border: none; }"
LIBRARY2_BUTTON = "QPushButton { background-image: url(img/buttons/LIBRARIES3.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/LIBRARIES2.png); border: none; }"
RESULTS_BUTTON = "QPushButton { background-image: url(img/buttons/RESULTS1.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/RESULTS2.png); border: none; }"
RESULTS2_BUTTON = "QPushButton { background-image: url(img/buttons/RESULTS3.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/RESULTS2.png); border: none; }"
TOOLS_BUTTON = "QPushButton { background-image: url(img/buttons/TOOLS1.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/TOOLS2.png); border: none; }"
TOOLS2_BUTTON = "QPushButton { background-image: url(img/buttons/TOOLS3.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/TOOLS2.png); border: none; }"
RESET_BUTTON = "QPushButton { background-image: url(img/buttons/RESET1.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/RESET2.png); border: none; }"
STOP_BUTTON = "QPushButton { background-image: url(img/buttons/STOP1.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/STOP2.png); border: none; }"
NEXT_BUTTON = "QPushButton { background-image: url(img/buttons/NEXT1.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/NEXT2.png); border: none; }"
BACK_BUTTON = "QPushButton { background-image: url(img/buttons/BACK1.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/BACK2.png); border: none; }"
RUN_BUTTON = "QPushButton { background-image: url(img/buttons/RUNAPP1.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/RUNAPP2.png); border: none; }"
TIMER_BUTTON = "background-image: url(img/buttons/TIMER.png); border: none; color: black; font-size: 20px;"
LOAD_BUTTON = "QPushButton { background-image: url(img/buttons/LOAD1.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/LOAD2.png); border: none; }"
SAVE_BUTTON = "QPushButton { background-image: url(img/buttons/SAVE1.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/SAVE2.png); border: none; }"
EXPORT_BUTTON = "QPushButton { background-image: url(img/buttons/EXPORT1.png); border: none; }\
                QPushButton:pressed { background-image: url(img/buttons/EXPORT2.png); border: none; }"

GREY_LIGHT = "background-image: url(img/buttons/DOT1.png); border: none;"
WHITE_LIGHT = "background-image: url(img/buttons/DOT2.png); border: none;"
BLUE_LIGHT = "background-image: url(img/buttons/DOT3.png); border: none;"
PURPLE_LIGHT = "background-image: url(img/buttons/DOT4.png); border: none;"
TEAL_LIGHT = "background-image: url(img/buttons/DOT5.png); border: none;"
GREEN_LIGHT = "background-image: url(img/buttons/DOT6.png); border: none;"
WINE_LIGHT = "background-image: url(img/buttons/DOT7.png); border: none;"
RED_LIGHT = "background-image: url(img/buttons/DOT8.png); border: none;"
ORANGE_LIGHT = "background-image: url(img/buttons/DOT9.png); border: none;"
YELLOW_LIGHT = "background-image: url(img/buttons/DOT10.png); border: none;"

GREEN_BOX_STYLE = "background-image: url(img/buttons/BOX03.png); border: none; font-size: 20px;"
LIME_BOX_STYLE = "background-image: url(img/buttons/BOX02.png); border: none; font-size: 20px;"
YELLOW_BOX_STYLE = "background-image: url(img/buttons/BOX01.png); border: none; font-size: 20px;"
GREY_BOX_STYLE = "background-image: url(img/buttons/WHITEBOX.png); border: none; font-size: 20px;"

LABELS = "QLabel {font: bold 18px;\
                border: 0px solid gray;}"
GREY_LABELS = "QLabel {font: bold 18px;\
                border: 0px solid gray;\
                color: #E6E6E6}"
BIG_GREY_LABELS = "QLabel {font: bold 32px;\
                border: 0px solid gray;\
                color: #E6E6E6}"
THIN_LABELS = "QLabel {font: 16px;\
                border: 0px solid gray;}"
THIN_DARK_LABELS = "QLabel {font: 10px;\
                border: 0px solid gray;\
                color: #3a3a3a}"
GREEN_LABELS = "QLabel {font: bold 18px;\
                border: 0px solid #9AFF9A;\
                color: #9cbd97}"
LIME_LABELS = "QLabel {font: bold 18px;\
                border: 0px solid #3399FF;\
                color: #c8d097}"
YELLOW_LABELS = "QLabel {font: bold 18px;\
                border: 0px solid #F8C957;\
                color: #fbe4ab}"

class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.library = -1

        self.title = "Theseus UI"
        self.top = 100
        self.left = 100
        self.width = 1000
        self.height = 750 
        self.icon_name = "img/icon.png"
        self.logo_name = "img/logo2.png"
        self.plate_name = "img/plate.png"

        self.style = "background-color: #1F1F1F"
        self.widget_style = "background-color: #1F1F1F; border: 1px solid gray; border-radius: 3px; color: white; font: 12px"
        self.widget_style2 = "background-color: #1F1F1F; border: 0px solid gray; border-radius: 3px; color: white; font: 12px"
        self.widget_style3 = "background-color: #ffffff; border: 0px solid gray; border-radius: 3px; color: black; font: 12px"

        self.button_width_1 = 180
        self.button_height_1 = 40 
        self.button_width_2 = 120
        self.button_height_2 = 120 

        self.check_button_w = 30
        self.check_button_h = 30 
        self.check_button_margins = 10
        
        self.home_margins_0 = 20
        self.home_margins_1 = 35
        self.home_margins = 50
        #self.home_styles = [LIBRARY_BUTTON, YELLOW_STYLE, RED_CIRCLE_STYLE]

        self.make_button_style = LIBRARY_BUTTON
        self.results_button_style = RESULTS_BUTTON
        self.tools_button_style = TOOLS_BUTTON
        #self.check_button_style = CHECK_BUTTON_STYLE
        #self.check_button_grey_style = CHECK_BUTTON_GREY_STYLE

        self.light_state1 = GREY_LIGHT
        self.light_state2 = BLUE_LIGHT

        self.barcode_button_style = [YELLOW_BOX_STYLE, YELLOW_LABELS]
        self.cartridge_button_style = [GREY_BOX_STYLE, GREY_LABELS]
        self.reagent_button_style = [GREY_BOX_STYLE, GREY_LABELS]

        self.library_apps = [["-",[],"grey",""]]
        self.input_types = ["Genomic DNA", "10 uL Blood"]
        
        self.time = WAIT
        self.timer = self.getTime()

        self.input_sizes = [10,10,10,10,10,10,10,10] # this should get updated by reader
        self.next = True
        self.reset_state = "reset"

        self.input_values = []
        self.current_job = "N/A"
        self.loaded_job = "N/A"
        self.loaded_job_data = [["","","","","","",""],
                                ["","","","","","",""],
                                ["","","","","","",""],
                                ["","","","","","",""],
                                ["","","","","","",""],
                                ["","","","","","",""],
                                ["","","","","","",""],
                                ["","","","","","",""]]
        self.loaded_job_library = "N/A"
        self.loaded_job_input = "N/A"
        self.loaded_job_color = "white"

        self.loaded_light_state1 = GREY_LIGHT
        self.loaded_light_state2 = BLUE_LIGHT


        self.initWindow()


    def initWindow(self):
        
        self.loadScripts()
        self.loadMostRecentJob()
        self.setWindowIcon(QtGui.QIcon(self.icon_name))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        self.setStyleSheet(self.style)
        self.loadWelcomeWidgets()
        self.loadLibraryWidgets()
        self.loadResultsWidgets()
        self.loadHomePanel()
        self.show()


    def loadScripts(self):
        app_path = "apps"
        for (dirpath, dirnames, filenames) in os.walk(app_path):
            filenames.sort()
            for file in filenames:
                name = ""
                inputs = []
                color = "yellow"
                input_pass = True
                if file != "theseus_utils.py" and file[-3:] == ".py":
                    with open("apps/" + str(file), 'r') as f:
                        lines = f.readlines()
                        for l in lines:
                            k = l.split(":")
                            if k[0] == '#NAME':
                                name = k[1].split("\n")[0]
                            elif k[0] == '#INPUTS':
                                inputs = k[1].split("\n")[0].split(",")
                                for i in inputs:
                                    if i not in self.input_types:
                                        input_pass = False
                            elif k[0] == '#COLOR':
                                color = k[1].split("\n")[0]
                if name != "" and input_pass:
                    print(str([name,inputs,color,str("apps/"+str(file))]))
                    self.library_apps.append([name,inputs,color,str("apps/"+str(file))])


    def loadMostRecentJob(self):
        app_path = "runs_info"
        for (dirpath, dirnames, filenames) in os.walk(app_path):
            filenames.sort(reverse=True)
            if len(filenames) != 0:
                self.loaded_job = str(filenames[0])
                file = open(os.path.join("runs_info", self.loaded_job),"rb")
                p_data = pickle.load(file)
                self.loaded_job_data = p_data["data"]
                self.loaded_job_library = p_data["library"]
                self.loaded_job_color = p_data["color"]
                print(self.loaded_job_color)
                self.loaded_job_input = p_data["input"]
                self.loaded_job = self.loaded_job + " (most recent)"
                file.close()


    def loadHomePanel(self):
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(self.logo_name))
        self.label.setGeometry(QRect(self.home_margins,
                                 self.home_margins_0*1.5,
                                 self.button_width_2,
                                 self.button_height_2))
        self.label.setToolTip("For the Better")


        self.parent_hbox = QHBoxLayout()
        
        self.make_button = QPushButton(self)
        self.make_button.setStyleSheet(self.make_button_style)
        self.make_button.setGeometry(QRect(self.home_margins_0,
                                 (self.height/1.55)-self.home_margins_1-(3*self.button_height_1+2*self.home_margins_1)-100,
                                 self.button_width_1,
                                 self.button_height_1))
        self.make_button.setFlat(True)
        self.make_button.setAutoFillBackground(True)
        self.make_button.setToolTip("Begin Theseus initializing process.")
        self.parent_hbox.addWidget(self.make_button)
        self.make_button.clicked.connect(partial(self.display,MAKE_LIBRARIES))

        self.view_results_button = QPushButton(self)
        self.view_results_button.setStyleSheet(self.results_button_style)
        self.view_results_button.setGeometry(QRect(self.home_margins_0,
                                 (self.height/1.55)-self.home_margins_1-(2*self.button_height_1+self.home_margins_1)-100,
                                 self.button_width_1,
                                 self.button_height_1))
        self.view_results_button.setToolTip("View results of previous Theseus runs.")
        self.parent_hbox.addWidget(self.view_results_button)
        self.view_results_button.clicked.connect(partial(self.display,RESULTS))

        self.tools_button = QPushButton(self)
        self.tools_button.setStyleSheet(self.tools_button_style)
        self.tools_button.setGeometry(QRect(self.home_margins_0,
                                 (self.height/1.55)-self.home_margins_1-self.button_height_1-100,
                                 self.button_width_1,
                                 self.button_height_1))
        self.tools_button.setToolTip("Configure Theseus")
        self.parent_hbox.addWidget(self.tools_button)
        self.tools_button.clicked.connect(partial(self.display,TOOLS))

        self.launchWelcome()


    
    def display(self, current_pane):
        if current_pane == MAKE_LIBRARIES:
            if self.make_button_style == LIBRARY_BUTTON:
                self.make_button_style = LIBRARY2_BUTTON
                self.make_button.setStyleSheet(self.make_button_style)
                self.results_button_style = RESULTS_BUTTON
                self.view_results_button.setStyleSheet(self.results_button_style)
                self.tools_button_style = TOOLS_BUTTON
                self.tools_button.setStyleSheet(self.tools_button_style)
                #self.view_results_button.setStyleSheet(self.greyed_style)
                #self.tools_button.setStyleSheet(self.greyed_circle_style)
                #self.view_results_button.setDisabled(True)
                #self.tools_button.setDisabled(True)
                self.launchLibrary()
                self.hideWelcome()
                self.hideResults()
            else:
                self.make_button_style = LIBRARY_BUTTON
                self.make_button.setStyleSheet(self.make_button_style)
                #self.view_results_button.setStyleSheet(self.home_styles[RESULTS-1])
                #self.tools_button.setStyleSheet(self.home_styles[TOOLS-1])
                #self.view_results_button.setDisabled(False)
                #self.tools_button.setDisabled(False)
                self.hideLibrary()
                self.launchWelcome()
            #self.Library()
        elif current_pane == RESULTS:
            if self.results_button_style == RESULTS_BUTTON:
                #self.make_button.setStyleSheet(self.greyed_style)
                self.make_button_style = LIBRARY_BUTTON
                self.make_button.setStyleSheet(self.make_button_style)
                self.results_button_style = RESULTS2_BUTTON
                self.view_results_button.setStyleSheet(self.results_button_style)
                self.tools_button_style = TOOLS_BUTTON
                self.tools_button.setStyleSheet(self.tools_button_style)
                #self.tools_button.setStyleSheet(self.greyed_circle_style)
                #self.make_button.setDisabled(True)
                #self.tools_button.setDisabled(True)
                self.hideLibrary()
                self.hideWelcome()
                self.launchResults()
            else:
                #self.make_button.setStyleSheet(self.home_styles[MAKE_LIBRARIES-1])
                self.results_button_style = RESULTS_BUTTON
                self.view_results_button.setStyleSheet(self.results_button_style)
                #self.tools_button.setStyleSheet(self.home_styles[TOOLS-1])
                #self.make_button.setDisabled(False)
                #self.tools_button.setDisabled(False)
                self.launchWelcome()
                self.hideResults()

            print("results")
        elif current_pane == TOOLS:
            if self.tools_button_style == TOOLS_BUTTON:
                #self.make_button.setStyleSheet(self.greyed_style)
                #self.view_results_button.setStyleSheet(self.greyed_style)
                self.make_button_style = LIBRARY_BUTTON
                self.make_button.setStyleSheet(self.make_button_style)
                self.results_button_style = RESULTS_BUTTON
                self.view_results_button.setStyleSheet(self.results_button_style)
                self.tools_button_style = TOOLS2_BUTTON
                self.tools_button.setStyleSheet(self.tools_button_style)
                #self.make_button.setDisabled(True)
                #self.view_results_button.setDisabled(True)
                self.hideLibrary()
                self.hideWelcome()
                self.hideResults()
            else:
                #self.make_button.setStyleSheet(self.home_styles[MAKE_LIBRARIES-1])
                #self.view_results_button.setStyleSheet(self.home_styles[RESULTS-1])
                self.tools_button_style = TOOLS_BUTTON
                self.tools_button.setStyleSheet(self.tools_button_style)
                #self.make_button.setDisabled(False)
                #self.view_results_button.setDisabled(False)
                self.launchWelcome()
            print("tools")
        elif current_pane == HOME:
            print("home is where you make it")

    def loadWelcomeWidgets(self):
        self.wel_widget1 = QWidget(self)
        self.wel_widget1.hide()
        self.wel_widget1.setGeometry(self.left+120, 10, self.width, self.height)
        self.wel_widget1.setStyleSheet(self.widget_style2)

        self.wel_label1 = QLabel(self.wel_widget1)
        self.wel_label1.setText("Welcome to Theseus")
        self.wel_label1.setGeometry(QRect(80, 60, self.width-(80*2)-(self.left+120), 25))
        self.wel_label1.setStyleSheet(BIG_GREY_LABELS)

        self.wel_label2 = QLabel(self.wel_widget1)
        self.wel_label2.setText("This is where a Theseus description can go. blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah Thank you for using Theseus.")
        self.wel_label2.setGeometry(QRect(80, 125, self.width-(80*2)-(self.left+120), self.height-125-60-60-60))
        self.wel_label2.setStyleSheet(THIN_LABELS)
        self.wel_label2.setWordWrap(True)
        self.wel_label2.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.wel_label2 = QLabel(self.wel_widget1)
        self.wel_label2.setText("version: pre-alpha")
        self.wel_label2.setGeometry(QRect(80, self.height-95, self.width-(80*2)-(self.left+120), 60))
        self.wel_label2.setStyleSheet(THIN_DARK_LABELS)
        self.wel_label2.setWordWrap(True)

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
        for l in self.library_apps[1:]:
            self.combo_box1.addItem(l[0])
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
        self.reset_button = QPushButton(self.lib_widget1)
        self.reset_button.setStyleSheet(RESET_BUTTON)
        self.reset_button.setGeometry(QRect(37,700,96,30))
        self.reset_button.clicked.connect(self.reset)
        # next back button

        self.lib_widget1_mini1 = QWidget(self.lib_widget1)
        self.lib_widget1_mini1.hide()
        self.lib_widget1_mini1.setGeometry(QRect((self.width - (self.left+120) - 37)/2 -30 ,700,61,30))
        self.lib_widget1_mini1.setStyleSheet(self.widget_style2)
        self.next_back_button = QPushButton(self.lib_widget1_mini1)
        self.next_back_button.setStyleSheet(NEXT_BUTTON)
        self.next_back_button.setGeometry(QRect(0,0,61,30))
        self.next_back_button.clicked.connect(self.nextBack)
        # question button
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
        self.timer_button.setStyleSheet(TIMER_BUTTON)
        self.timer_button.setGeometry(QRect(self.home_margins + 50 + 25,self.home_margins*7,125,44))
        self.timer_button.setDisabled(True)
        self.timer_button.hide()
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
        self.barcode_button_shell.setStyleSheet(YELLOW_BOX_STYLE)
        self.barcode_button_shell.setGeometry(QRect(37,20,40,40))
        self.barcode_button_shell.setDisabled(True)

        self.cartridge_button_shell = QPushButton(u'\u2713',self.lib_widget3)
        self.cartridge_button_shell.setStyleSheet(LIME_BOX_STYLE)
        self.cartridge_button_shell.setGeometry(QRect(37+self.home_margins,20,40,40))
        self.cartridge_button_shell.setDisabled(True)

        self.reagent_button_shell = QPushButton(u'\u2713',self.lib_widget3)
        self.reagent_button_shell.setStyleSheet(GREEN_BOX_STYLE)
        self.reagent_button_shell.setGeometry(QRect(37+self.home_margins*2,20,40,40))
        self.reagent_button_shell.setDisabled(True)

        self.lib_widget3_mini1 = QWidget(self.lib_widget3)
        self.lib_widget3_mini1.setGeometry(37,80,680,488)
        self.lib_widget3_mini1.setStyleSheet(self.widget_style2)

        self.plate_label = QLabel(self.lib_widget3_mini1)
        self.plate_label.setText("Load 10uL Genomic DNA (A1, C1, E1, G1, I1, K1, M1, O1).")
        self.plate_label.setGeometry(QRect(0,0,680,20))
        self.plate_label.setStyleSheet(LABELS)

        self.plate = QLabel(self.lib_widget3_mini1)
        self.plate.setPixmap(QPixmap(self.plate_name))
        self.plate.setGeometry(QRect(0,20,680,468))
        self.plate.setToolTip("Reagent plate map")


        
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

        self.sample_table = QTableWidget(8,6,self.lib_widget3_mini2_1)
        self.sample_table.setStyleSheet(TABLE_STYLE)
        self.sample_table.setGeometry(QRect(0,0,680,325))
        self.sample_table.setHorizontalHeaderItem(0,QTableWidgetItem("Well"))
        self.sample_table.setHorizontalHeaderItem(1,QTableWidgetItem("Size (ng)"))
        self.sample_table.setHorizontalHeaderItem(2,QTableWidgetItem("Sample"))
        self.sample_table.setHorizontalHeaderItem(3,QTableWidgetItem("Database"))
        self.sample_table.setHorizontalHeaderItem(4,QTableWidgetItem("Date"))
        self.sample_table.setHorizontalHeaderItem(5,QTableWidgetItem("Notes"))
        self.sample_table_header = self.sample_table.horizontalHeader()       
        self.sample_table_header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.sample_table_header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.sample_table_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.sample_table_header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.sample_table_header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.sample_table_header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        self.sample_table_rows = self.sample_table.verticalHeader()   
        for i in range(8):
            item = QTableWidgetItem(WELLS[i])
            item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            self.sample_table.setItem(i,0,item)
            self.sample_table.item(i,0).setBackground(LIGHTEST_GREY)
            self.sample_table.item(i,0).setForeground(RED)
            item = QTableWidgetItem("Database update")
            item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            self.sample_table.setItem(i,3,item)
            self.sample_table.item(i,3).setBackground(LIGHTEST_GREY)
            self.sample_table.item(i,3).setForeground(BLUE)
            item = QTableWidgetItem(str(datetime.date.today()))
            item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            self.sample_table.setItem(i,4,item)
            self.sample_table.item(i,4).setBackground(LIGHTEST_GREY)
            self.sample_table_rows.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        # start button
        self.start_button = QPushButton(self.lib_widget3_mini2)
        self.start_button.setStyleSheet(RUN_BUTTON)
        self.start_button.setGeometry(QRect(340-96,408,192,60))
        self.start_button.clicked.connect(self.run)


    def loadResultsWidgets(self):
        self.res_widget1 = QWidget(self)
        self.res_widget1.hide()
        self.res_widget1.setGeometry(self.left+120, 10, self.width, self.height)
        self.res_widget1.setStyleSheet(self.widget_style)

        self.res_widget1_mini1 = QWidget(self.res_widget1)
        self.res_widget1_mini1.show()
        self.res_widget1_mini1.setGeometry(37,60,707,325)
        self.res_widget1_mini1.setStyleSheet(self.widget_style3)

        self.res_label1 = QLabel(self.res_widget1)
        self.res_label1.setText("Displaying: " + str(self.loaded_job))
        self.res_label1.setGeometry(QRect(37, 20, 707, 25))
        self.res_label1.setStyleSheet(LABELS)

        self.results_table = QTableWidget(8,7,self.res_widget1_mini1)
        self.results_table.setStyleSheet(TABLE_STYLE)
        self.results_table.setGeometry(QRect(0,0,707,325))
        self.results_table.setHorizontalHeaderItem(0,QTableWidgetItem("Well"))
        self.results_table.setHorizontalHeaderItem(1,QTableWidgetItem("In ng"))
        self.results_table.setHorizontalHeaderItem(2,QTableWidgetItem("Sample"))
        self.results_table.setHorizontalHeaderItem(3,QTableWidgetItem("Database"))
        self.results_table.setHorizontalHeaderItem(4,QTableWidgetItem("Date"))
        self.results_table.setHorizontalHeaderItem(5,QTableWidgetItem("Notes"))
        self.results_table.setHorizontalHeaderItem(6,QTableWidgetItem("Out ng"))
        self.results_table_header = self.results_table.horizontalHeader()       
        self.results_table_header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.results_table_header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.results_table_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.results_table_header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.results_table_header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.results_table_header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        self.results_table_header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        self.results_table_rows = self.results_table.verticalHeader()   
        for i in range(8):
            for j in range(7):
                print(self.loaded_job_data[i][j])
                item = QTableWidgetItem(self.loaded_job_data[i][j])
                if j != 2:
                    item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                    self.results_table.setItem(i,j,item)
                    self.results_table.item(i,j).setBackground(LIGHTEST_GREY)
                else:
                    self.results_table.setItem(i,j,item)
            self.results_table_rows.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)



        self.res_light1 = QWidget(self.res_widget1)
        self.res_light1.setStyleSheet(self.loaded_light_state1)
        self.res_light1.setGeometry(QRect(37, 400, self.check_button_w, self.check_button_h))

        self.res_combo_box1 = QtWidgets.QComboBox(self.res_widget1)
        self.res_combo_box1.setGeometry(QRect(80, 400, 200, 30))
        self.res_combo_box1.setObjectName("combo_box1")
        self.res_combo_box1.addItem(str(self.loaded_job_library))
        self.res_combo_box1.setStyleSheet(DROPDOWN_GREYED)
        self.res_combo_box1.setEnabled(False)

        self.res_light2 = QWidget(self.res_widget1)
        self.res_light2.setStyleSheet(self.loaded_light_state2)
        self.res_light2.setGeometry(QRect(37, 440, self.check_button_w, self.check_button_h))

        self.res_combo_box2 = QtWidgets.QComboBox(self.res_widget1)
        self.res_combo_box2.setGeometry(QRect(80, 440, 200, 30))
        self.res_combo_box2.setObjectName("combo_box2")
        self.res_combo_box2.addItem(str(self.loaded_job_input))
        self.res_combo_box2.setStyleSheet(DROPDOWN_GREYED)
        self.res_combo_box2.setEnabled(False)



        self.res_widget1_mini2 = QWidget(self.res_widget1)
        self.res_widget1_mini2.show()
        self.res_widget1_mini2.setGeometry(37,520,707,30)
        self.res_widget1_mini2.setStyleSheet(self.widget_style2)

        # load button
        self.load_button = QPushButton(self.res_widget1_mini2)
        self.load_button.setStyleSheet(LOAD_BUTTON)
        self.load_button.setGeometry(QRect(0,0,61,30))
        self.load_button.clicked.connect(self.loadRunData)
        # save button
        self.save_button = QPushButton(self.res_widget1_mini2)
        self.save_button.setStyleSheet(SAVE_BUTTON)
        self.save_button.setGeometry(QRect(81,0,61,30))
        self.save_button.clicked.connect(self.saveRunData)
        # export button
        self.export_button = QPushButton(self.res_widget1_mini2)
        self.export_button.setStyleSheet(EXPORT_BUTTON)
        self.export_button.setGeometry(QRect(707-84,0,84,30))
        self.export_button.clicked.connect(self.exportRunData)

        




    def updateLight(self):
        lights = {
            "grey": GREY_LIGHT,
            "white": WHITE_LIGHT,
            "blue": BLUE_LIGHT,
            "purple": PURPLE_LIGHT,
            "teal": TEAL_LIGHT,
            "green": GREEN_LIGHT,
            "wine": WINE_LIGHT,
            "red": RED_LIGHT,
            "orange": ORANGE_LIGHT,
            "yellow": YELLOW_LIGHT,
        }
        if self.combo_box1.currentText() == "-":
            self.light_state1 = GREY_LIGHT
            self.lib_widget2.hide()
        else: 
            self.light_state1 = lights[self.library_apps[self.combo_box1.currentIndex()][2]]
            self.lib_widget2.show()
        if self.combo_box2.currentText() == "Genomic DNA":
            self.light_state2 = BLUE_LIGHT
            self.plate_label.setText("Load 10uL Genomic DNA (A1, C1, E1, G1, I1, K1, M1, O1).")
            self.plate_name = "img/g_plate.png"
            self.plate.setPixmap(QPixmap(self.plate_name))
        else:
            self.light_state2 = WINE_LIGHT
            self.plate_label.setText("Load 10uL Blood (A1, C1, E1, G1, I1, K1, M1, O1).")
            self.plate_name = "img/plate.png"
            self.plate.setPixmap(QPixmap(self.plate_name))
        self.lib_light1.setStyleSheet(self.light_state1)
        self.lib_light2.setStyleSheet(self.light_state2)
        self.resetWidget2()

    def updateLoadedLight(self):
        lights = {
            "grey": GREY_LIGHT,
            "white": WHITE_LIGHT,
            "blue": BLUE_LIGHT,
            "purple": PURPLE_LIGHT,
            "teal": TEAL_LIGHT,
            "green": GREEN_LIGHT,
            "wine": WINE_LIGHT,
            "red": RED_LIGHT,
            "orange": ORANGE_LIGHT,
            "yellow": YELLOW_LIGHT,
        }
        self.loaded_light_state1 = lights[self.loaded_job_color]
        self.res_combo_box1.setItemText(0, str(self.loaded_job_library))
        if self.loaded_job_input == "Genomic DNA":
            self.loaded_light_state2 = BLUE_LIGHT
            self.res_combo_box2.setItemText(0, str(self.loaded_job_input))
        else:
            self.loaded_light_state2 = WINE_LIGHT
            self.res_combo_box2.setItemText(0, str(self.loaded_job_input))
        self.res_light1.setStyleSheet(self.loaded_light_state1)
        self.res_light2.setStyleSheet(self.loaded_light_state2)


    
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
            
            self.cartridge_button_style = [LIME_BOX_STYLE, LIME_LABELS]
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
            
            self.reagent_button_style = [GREEN_BOX_STYLE, GREEN_LABELS]
            self.reagent_button.setStyleSheet(self.reagent_button_style[0])
            self.reagent_button_label.setStyleSheet(self.reagent_button_style[1])
            #self.reagent_button.setDisabled(False)

            self.timer_button.setStyleSheet(TIMER_BUTTON)
            self.timer_button.setDisabled(False)
            self.timer_button.show()
           

        elif current_step == REAGENT:
            print("Reagents are ready")
            self.ticker()



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
            self.reagent_button.setDisabled(True)
            self.reagent_button.setText(u'\u2713')
            self.timer_button.setDisabled(True)


    def timerTimeout(self):
        if self.time == 0:
            self.my_qtimer.stop()
            self.lib_widget2.hide()
            self.lib_widget3.show()
            self.lib_widget1_mini1.show()
            #self.forward_backward_widget.show()
        else:
            self.time -= 1
        self.timer_button.setText(f'{self.time//60:02}'+":"+f'{self.time-((self.time//60)*60):02}')



    def run(self):
        self.run_box = QMessageBox()
        self.run_box.setIcon(QMessageBox.Question)
        self.run_box.setText("Are you sure you want to run application?")
        self.run_box.setWindowTitle("Run application")
        self.run_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        #self.reset_box.buttonClicked.connect(msgButtonClick)
        ret_val = self.run_box.exec()
        if ret_val == QMessageBox.Yes:
            input_pass = self.pushInputs()
            if input_pass:
                print("run app!!")
                self.launchScript()
                self.reset_button.setStyleSheet(STOP_BUTTON)
                self.reset_state = "stop"


    def pushInputs(self):
        pickle_dict = {"library":"", "input":"", "color":"", "data":[]}
        pickle_list = []
        temp_inputs = []
        input_pass = True
        bad_values = []
        for p in range(8):
            pickle_list.append([])
            for i in range(6):
                if i == 1 and self.sample_table.item(p,i).text() != "":
                    try:
                        input_val = float(self.sample_table.item(p,i).text())
                        temp_inputs.append(input_val)
                    except ValueError:
                        input_pass = False
                        bad_values.append(self.sample_table.item(p,i).text())

                pickle_list[-1].append(self.sample_table.item(p,i).text())
            pickle_list[-1].append("")
        if input_pass:
            pickle_dict["data"] = pickle_list
            pickle_dict["color"] = self.library_apps[self.combo_box1.currentIndex()][2]
            pickle_dict["input"] = self.combo_box2.currentText()
            pickle_dict["library"] = self.combo_box1.currentText()
            self.input_values = temp_inputs
            self.current_job = os.path.join("runs_info", str(datetime.datetime.now()).replace(" ","_").replace(":","-").replace(".","-") + ".p")
            file = open(self.current_job,"wb")
            pickle.dump(pickle_dict, file)
            file.close()
        else:
            self.error_msg = QMessageBox()
            self.error_msg.setIcon(QMessageBox.Warning)
            self.error_msg.setWindowTitle("Input Error")
            self.error_msg.setText("Please only use numerical values in the size column.")
            self.error_msg.setDetailedText("Triggered by values \"" + str("\", \"".join(bad_values)) + ".\"")
            self.error_msg.exec()
        return input_pass

    def openFileNameDialog(self):
        self.loaded_job = QFileDialog.getOpenFileName(self, 'Open runs info file', 'runs_info', "*.p")[0].split("/")[-1]
        print(self.loaded_job)
        self.updateLoadedJob()
        self.updateResultsInfo()

    def updateLoadedJob(self):
        app_path = "runs_info"
        file = open(os.path.join("runs_info", self.loaded_job),"rb")
        p_data = pickle.load(file)
        self.loaded_job_data = p_data["data"]
        self.loaded_job_library = p_data["library"]
        self.loaded_job_color = p_data["color"]
        print(self.loaded_job_color)
        self.loaded_job_input = p_data["input"]
        self.loaded_job = self.loaded_job
        file.close()

    def updateResultsInfo(self):
        for i in range(8):
            for j in range(7):
                print(self.loaded_job_data[i][j])
                item = QTableWidgetItem(self.loaded_job_data[i][j])
                if j != 2:
                    item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                    self.results_table.setItem(i,j,item)
                    self.results_table.item(i,j).setBackground(LIGHTEST_GREY)
                else:
                    self.results_table.setItem(i,j,item)
            self.results_table_rows.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        self.res_label1.setText("Displaying: " + str(self.loaded_job))
        self.updateLoadedLight()

    def openExportNameDialog(self):
        self.export_file = QFileDialog.getSaveFileName(self, 'Select or name .csv report file', os.path.join('report_export',str(self.loaded_job.split(".p")[0]) + ".csv"), "*.csv")[0].split("/")[-1]
        print(self.export_file)
        print(self.export_file[-4:])
        if self.export_file[-4:] == ".csv":
            self.saveRunData()
            self.exportReport()

    def exportReport(self):
        print("we did it!")
        temp = [[self.loaded_job, self.loaded_job_library, self.loaded_job_input]] + self.loaded_job_data
        print(temp)
        with open(os.path.join('report_export', self.export_file), "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(temp)

    def launchScript(self):
        self.process1 = QtCore.QProcess()
        self.process1.finished.connect(self.launchCmdToHost)
        self.cmd1 = "python " + str(self.library_apps[self.combo_box1.currentIndex()][3]) + " -i \"" + str(self.input_types[self.combo_box2.currentIndex()]) + "\" -i2 " + " ".join([ str(i) for i in self.input_sizes ])
        print(self.cmd1)
        self.process1.start(self.cmd1)

    def launchCmdToHost(self):
        self.process2 = QtCore.QProcess()
        self.process2.finished.connect(self.finishedCmd)
        self.cmd2 = "python thes_host/thes_host.py -i cmd/cmd.txt"
        print(self.cmd2)
        self.process2.start(self.cmd2)

    def finishedCmd(self):
        print("cmd finished!")


    def viewResults(self):
        print("viewResults")
        self.lib_elements_off()

    def tools(self):
        print("tools")
        self.lib_elements_off()

    def reset(self):
        if self.reset_state == "Reset":
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

    def nextBack(self):
        if self.next:
            self.lib_widget3_mini1.hide()
            self.lib_widget3_mini2.show()
            self.next_back_button.setStyleSheet(BACK_BUTTON)
            self.next = False
        else:
            self.lib_widget3_mini1.show()
            self.lib_widget3_mini2.hide()
            self.next_back_button.setStyleSheet(NEXT_BUTTON)
            self.next = True

    def question(self):
        print("question")

    def loadRunData(self):
        print("load run data")
        self.openFileNameDialog()

    def saveRunData(self):
        print("save run data")
        pickle_dict = {"library":"", "input":"", "color":"", "data":[]}
        pickle_list2 = []
        temp_inputs = []
        for p in range(8):
            pickle_list2.append([])
            for i in range(7): 
                pickle_list2[-1].append(self.results_table.item(p,i).text())
                print(self.results_table.item(p,i).text())
        pickle_dict["data"] = pickle_list2
        self.loaded_job_data = pickle_list2
        pickle_dict["color"] = self.loaded_job_color
        pickle_dict["input"] = self.loaded_job_input
        pickle_dict["library"] = self.loaded_job_library
        self.loaded_job = self.loaded_job.split(" (most recent)")[0]
        #print(self.loaded_job_data)
        file = open(os.path.join("runs_info", self.loaded_job),"wb")
        pickle.dump(pickle_dict, file)
        file.close()
        

    def exportRunData(self):
        self.openExportNameDialog()

    def launchLibrary(self):
        self.lib_widget1.show()
        if self.time == 0:
            self.lib_widget3.show()
        else:
            if self.combo_box1.currentText() != "-":
                self.lib_widget2.show()

    def launchResults(self):
        self.updateLoadedLight()
        self.res_widget1.show()

    def launchWelcome(self):
        self.wel_widget1.show()

    def hideLibrary(self):
        self.lib_widget1.hide()
        self.lib_widget2.hide()
        self.lib_widget3.hide()

    def hideResults(self):
        self.res_widget1.hide()

    def hideWelcome(self):
        self.wel_widget1.hide()

    def resetWidget1(self):
        print("resetting 1")
        self.combo_box1.setCurrentIndex(0)
        self.combo_box2.setCurrentIndex(0)
        self.combo_box1.setEnabled(True)
        self.combo_box2.setEnabled(True)
        self.combo_box1.setStyleSheet(DROPDOWN)
        self.combo_box2.setStyleSheet(DROPDOWN)
        self.lib_widget1_mini1.hide()
        self.lib_widget2.hide()
        #self.forward_backward_widget.hide()
        self.reset_button.setStyleSheet(RESET_BUTTON)
        self.reset_state = "reset"
        self.resetWidget2()
        self.resetWidget3()


    def resetWidget2(self):
        print("resetting 2")
        
        self.barcode_button_style = [YELLOW_BOX_STYLE, YELLOW_LABELS]
        self.cartridge_button_style = [GREY_BOX_STYLE, GREY_LABELS]
        self.reagent_button_style = [GREY_BOX_STYLE, GREY_LABELS]
        
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
        self.timer_button.setStyleSheet(TIMER_BUTTON)
        self.timer_button.setDisabled(True)
        self.timer_button.hide()
        self.lib_widget1_mini1.hide()

        self.lib_widget3.hide()   
        self.resetWidget3()


    def resetWidget3(self):
        print("resetting 3")
        '''
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
        '''
        for i in range(8):
            self.sample_table.setItem(i,1,QTableWidgetItem(""))
            self.sample_table.setItem(i,2,QTableWidgetItem(""))
            self.sample_table.setItem(i,5,QTableWidgetItem(""))
        self.lib_widget3_mini1.show()
        self.lib_widget3_mini2.hide()
        self.next_back_button.setStyleSheet(NEXT_BUTTON)
        self.next = True



    
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
        
class RunApp(QtCore.QObject):
    signal = QtCore.pyqtSignal(object)

    def __init__(self, script, input_type, concentrations):
        QtCore.QThread.__init__(self)
        self.script = script
        self.input_type = input_type
        self.concentrations = concentrations

    def run(self):
        print("running")
        


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())

