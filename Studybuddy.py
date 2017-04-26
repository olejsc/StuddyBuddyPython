import sys
import time
import threading
import datetime
import json
import pyglet
import PyQt5
import os
import random
import string
import winreg
from time import sleep
from threading import Thread
from datetime import *
from selenium import webdriver
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QSystemTrayIcon, QMessageBox
from PyQt5.QtGui import QIcon

# Mapping of objects and relations between them is commented below, to make it
# more intuitive. The further to the left, the more reliable the objects on
# the right are to it.Note that actions which relate to more objects are not
# included.
# ---------------START OF OBJECT MAPPING  -------------------------
# Mainwindow
#   menubar
#       menuHelp
#           ActionQuit
#           ActionMinimize_to_tray
#   statusbar
#   top_widget
#       tab_widget
#           Add_notification_tab
#               Notification_clear_button
#               Notification_save_button
#               add_notificaition_error_label
#               groupBox_3
#                   label_2
#               groupBox_4
#                   frequency_radiobutton_1
#                   frequency_radiobutton_2
#                   frequency_radiobutton_3
#               groupBox_5
#                   HorizontalLayout
#                       Clear_button
#                   subject_code_linedit
#               groupBox_6
#                   struggle_linedit
#               line_2
#           Saved_subjects_tab
#               groupBox
#                   list_of_notifications
#                   saved_subjects_delete_button
#               groupBox_2
#           Settings_tab
#               line_3
#               settings_error_label
#               settings_outer_box
#                   settings_checkbox_mute_mode
#                   settings_checkbox_startup
#                   settings_inner_box
#               settings_save_button
# -----------------END OF OBJECT MAPPING---------------------------


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        def setupVariables(self, MainWindow):
            self.notifications = self.get_all_notifications()
            self.opts = self.get_time_of_notification(self.notifications)
            self.name_dict = name_dict = {"SubjectCode": "", "Frequency": "",
                                          "Name": "", "FrequencyLength": "",
                                          "LastNotification": "",
                                          "LastNotificationSeen": "False"}
            self.__threads = []
            self.__scrapethreads = []
            self.notification_file = "notifications.txt"
            self.log_file = "log.txt"
            self.setting_file = "settings.txt"
            self.time_format = "%y-%m-%d-%H-%M-%S"
            self.key_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
            self.working_directory = os.getcwd()

        def setupFiles(self, MainWindow):
            self.notifications_exist = os.path.isfile("notifications.txt")
            self.log_exist = os.path.isfile("log.txt")
            self.settings_exist = os.path.isfile("settings.txt")
            if self.notifications_exist is False:
                file = open(self.notification_file, 'w').close()
            if self.log_exist is False:
                file = open(self.log_file, 'w').close()
            if self.settings_exist is False:
                file = open(self.setting_file, 'w').close()

        def setupMenubar(self, MainWindow):
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 597, 21))
            self.menubar.setStyleSheet("color: black;\n"
                                       "background-color: rgb(186,186, 186);\n"
                                       "")
            self.menubar.setObjectName("menubar")
            self.menuHelp = QtWidgets.QMenu(self.menubar)
            self.menuHelp.setStyleSheet("selection-color: rgb(255, 255, 255);")
            self.menuHelp.setObjectName("menuHelp")
            MainWindow.setMenuBar(self.menubar)

        def setupCentralWidget(self, MainWindow):
            self.top_widget = QtWidgets.QWidget(MainWindow)
            self.top_widget.setObjectName("top_widget")
            MainWindow.setCentralWidget(self.top_widget)

        def setupGridlayout(self, MainWindow):
            self.gridLayout = QtWidgets.QGridLayout(self.top_widget)
            self.gridLayout.setObjectName("gridLayout")

        def setupTabWidget(self, MainWindow):
            self.tabWidget = QtWidgets.QTabWidget(self.top_widget)
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(9)
            self.tabWidget.setFont(font)
            self.tabWidget.setTabBarAutoHide(False)
            self.tabWidget.setObjectName("tabWidget")
            self.Add_notification_tab = QtWidgets.QWidget()
            self.Add_notification_tab.setObjectName("Add_notification_tab")
            self.tabWidget.addTab(self.Add_notification_tab, "")
            self.Saved_subjects_tab = QtWidgets.QWidget()
            self.Saved_subjects_tab.setObjectName("Saved_subjects_tab")
            self.tabWidget.addTab(self.Saved_subjects_tab, "")
            self.Settings_tab = QtWidgets.QWidget()
            self.Settings_tab.setObjectName("Settings_tab")
            self.tabWidget.addTab(self.Settings_tab, "")
            self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
            self.tabWidget.setCurrentIndex(0)

        def setupContentNotificationTab(self, MainWindow):
            self.groupBox_4 = QtWidgets.QGroupBox(self.Add_notification_tab)
            self.groupBox_4.setGeometry(QtCore.QRect(20, 180, 271, 101))
            font = QtGui.QFont()
            font.setPointSize(9)
            self.groupBox_4.setFont(font)
            self.groupBox_4.setObjectName("groupBox_4")
            self.frequency_radiobutton_1 = QtWidgets.QRadioButton(self.groupBox_4)
            self.frequency_radiobutton_1.setGeometry(QtCore.QRect(10, 30, 200,
                                                                  17))
            self.frequency_radiobutton_1.setMinimumSize(QtCore.QSize(200, 17))
            font = QtGui.QFont()
            font.setPointSize(-1)
            self.frequency_radiobutton_1.setFont(font)
            self.frequency_radiobutton_1.setStyleSheet("min-height: 17px;\n"
                                                       "max-height: 17px;\n"
                                                       "min-width: 200px;\n"
                                                       "max-width: 200px;\n"
                                                       "font-size: 15px;\n"
                                                       "")
            self.frequency_radiobutton_1.setObjectName("""frequency_
                                                       radiobutton_1""")
            self.frequency_radiobutton_1.setChecked(True)
            self.frequency_radiobutton_2 = QtWidgets.QRadioButton(self.groupBox_4)
            self.frequency_radiobutton_2.setGeometry(QtCore.QRect(10, 50, 200, 17))
            self.frequency_radiobutton_2.setMinimumSize(QtCore.QSize(200, 17))
            self.frequency_radiobutton_2.setFont(font)
            self.frequency_radiobutton_2.setStyleSheet("min-height: 17px;\n"
                                                       "max-height: 17px;\n"
                                                       "min-width: 200px;\n"
                                                       "max-width: 200px;\n"
                                                       "font-size: 15px;")
            self.frequency_radiobutton_2.setObjectName("frequency_radiobutton_2")
            self.frequency_radiobutton_3 = QtWidgets.QRadioButton(self.groupBox_4)
            self.frequency_radiobutton_3.setGeometry(QtCore.QRect(10, 70, 200, 17))
            self.frequency_radiobutton_3.setMinimumSize(QtCore.QSize(200, 17))
            self.frequency_radiobutton_3.setFont(font)
            self.frequency_radiobutton_3.setStyleSheet("min-height: 17px;\n"
                                                       "max-height: 17px;\n"
                                                       "min-width: 200px;\n"
                                                       "max-width: 200px;\n"
                                                       "font-size: 15px;")
            self.frequency_radiobutton_3.setObjectName("frequency_radiobutton_3")
            self.Notification_save_button = QtWidgets.QPushButton(self.Add_notification_tab)
            self.Notification_save_button.setGeometry(QtCore.QRect(390, 380, 82, 32))
            self.Notification_save_button.setStyleSheet("min-height: 30px;\n"
                                                        "max-height: 30px;\n"
                                                        "min-width: 80px;\n"
                                                        "max-width: 80px;\n"
                                                        "font-size: 15px;\n"
                                                        "")
            self.Notification_save_button.setObjectName("Notification_save_button")
            self.groupBox_5 = QtWidgets.QGroupBox(self.Add_notification_tab)
            self.groupBox_5.setGeometry(QtCore.QRect(20, 10, 271, 81))
            font = QtGui.QFont()
            font.setPointSize(9)
            self.groupBox_5.setFont(font)
            self.groupBox_5.setObjectName("groupBox_5")
            self.subject_code_linedit = QtWidgets.QLineEdit(self.groupBox_5)
            self.subject_code_linedit.setGeometry(QtCore.QRect(10, 20, 251, 21))
            self.subject_code_linedit.setObjectName("subject_code_linedit")
            self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox_5)
            self.horizontalLayoutWidget.setGeometry(QtCore.QRect(100, 50, 160, 25))
            self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.Clear_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
            self.Clear_button.setObjectName("Clear_button")
            self.Clear_button.setGeometry(QtCore.QRect(100, 360, 551, 20))
            self.horizontalLayout.addWidget(self.Clear_button)
            self.line_2 = QtWidgets.QFrame(self.Add_notification_tab)
            self.line_2.setGeometry(QtCore.QRect(10, 360, 551, 20))
            self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
            self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_2.setObjectName("line_2")
            self.groupBox_6 = QtWidgets.QGroupBox(self.Add_notification_tab)
            self.groupBox_6.setGeometry(QtCore.QRect(20, 100, 271, 71))
            font = QtGui.QFont()
            font.setPointSize(9)
            self.groupBox_6.setFont(font)
            self.groupBox_6.setObjectName("groupBox_6")
            self.struggle_lineedit = QtWidgets.QLineEdit(self.groupBox_6)
            self.struggle_lineedit.setGeometry(QtCore.QRect(10, 30, 254, 27))
            self.struggle_lineedit.setStyleSheet("padding: 1px;\n"
                                                 "border-style: solid;\n"
                                                 "border: 1px solid gray;\n"
                                                 "border-radius: 3px;\n"
                                                 "min-height: 23px;\n"
                                                 "max-height: 23px;\n"
                                                 "min-width: 250px;\n"
                                                 "max-width: 250px;\n"
                                                 "\n""")
            self.struggle_lineedit.setMaxLength(250)
            self.struggle_lineedit.setAlignment(QtCore.Qt.AlignLeading |
                                                QtCore.Qt.AlignLeft |
                                                QtCore.Qt.AlignTop)
            self.struggle_lineedit.setObjectName("struggle_lineedit")
            self.Notification_clear_button = QtWidgets.QPushButton(self.Add_notification_tab)
            self.Notification_clear_button.setGeometry(QtCore.QRect(480, 380, 82, 32))
            self.Notification_clear_button.setStyleSheet("min-height: 30px;\n"
                                                         "max-height: 30px;\n"
                                                         "min-width: 80px;\n"
                                                         "max-width: 80px;\n"
                                                         "font-size: 15px;")
            self.Notification_clear_button.setObjectName("Notification_clear_button")
            self.add_notificaiton_error_label = QtWidgets.QLabel(self.Add_notification_tab)
            self.add_notificaiton_error_label.setGeometry(QtCore.QRect(10, 385, 371, 21))
            self.add_notificaiton_error_label.setObjectName("add_notificaiton_error_label")
            self.groupBox_3 = QtWidgets.QGroupBox(self.Add_notification_tab)
            self.groupBox_3.setGeometry(QtCore.QRect(309, 10, 251, 351))
            self.groupBox_3.setTitle("")
            self.groupBox_3.setObjectName("groupBox_3")
            self.label_2 = QtWidgets.QLabel(self.groupBox_3)
            self.label_2.setGeometry(QtCore.QRect(10, 0, 241, 341))
            self.label_2.setText("")
            self.label_2.setPixmap(QtGui.QPixmap("study.png"))
            self.label_2.setObjectName("label_2")
            self.groupBox_4.raise_()
            self.Notification_save_button.raise_()
            self.groupBox_5.raise_()
            self.line_2.raise_()
            self.groupBox_6.raise_()
            self.Notification_clear_button.raise_()
            self.add_notificaiton_error_label.raise_()
            self.groupBox_3.raise_()

        def setupContentSavedSubjectsTab(self, MainWindow):
            self.groupBox = QtWidgets.QGroupBox(self.Saved_subjects_tab)
            self.groupBox.setGeometry(QtCore.QRect(80, 10, 401, 291))
            self.groupBox.setObjectName("groupBox")
            self.list_of_notifications = QtWidgets.QComboBox(self.groupBox)
            self.list_of_notifications.setGeometry(QtCore.QRect(10, 30, 382, 27))
            self.list_of_notifications.setObjectName("list_of_notifications")
            self.list_of_notifications.setMaxVisibleItems(10)
            self.saved_subjects_delete_button = QtWidgets.QPushButton(self.groupBox)
            self.saved_subjects_delete_button.setGeometry(QtCore.QRect(10, 250, 82, 32))
            self.saved_subjects_delete_button.setStyleSheet("min-height: 30px;\n"
                                                            "max-height: 30px;\n"
                                                            "min-width: 80px;\n"
                                                            "max-width: 80px;\n"
                                                            "font-size: 15px;\n"
                                                            "\n""")
            self.saved_subjects_delete_button.setObjectName("saved_subjects_delete_button")
            if self.notifications:
                for notification in self.notifications:
                    self.list_of_notifications.addItem("Fag : " + notification['SubjectCode'] + " - " + notification['Name'], notification)
            else:
                self.saved_subjects_delete_button.setEnabled(False)

            self.groupBox_2 = QtWidgets.QGroupBox(self.Saved_subjects_tab)
            self.groupBox_2.setGeometry(QtCore.QRect(70, 10, 421, 301))
            self.groupBox_2.setTitle("")
            self.groupBox_2.setObjectName("groupBox_2")
            self.groupBox_2.raise_()
            self.groupBox.raise_()

        def setupContentSettingsTab(self, MainWindow):
            self.settings_save_button = QtWidgets.QPushButton(self.Settings_tab)
            self.settings_save_button.setGeometry(QtCore.QRect(480, 380, 82, 32))
            self.settings_save_button.setStyleSheet("min-height: 30px;\n"
                                                    "max-height: 30px;\n"
                                                    "min-width: 80px;\n"
                                                    "max-width: 80px;\n"
                                                    "font-size: 15px;")
            self.settings_save_button.setObjectName("settings_save_button")
            self.line_3 = QtWidgets.QFrame(self.Settings_tab)
            self.line_3.setGeometry(QtCore.QRect(10, 360, 551, 20))
            self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
            self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_3.setObjectName("line_3")
            self.settings_outer_box = QtWidgets.QGroupBox(self.Settings_tab)
            self.settings_outer_box.setGeometry(QtCore.QRect(80, 10, 411, 301))
            self.settings_outer_box.setTitle("")
            self.settings_outer_box.setObjectName("settings_outer_box")
            self.settings_checkbox_lecture_mode = QtWidgets.QCheckBox(self.settings_outer_box)
            self.settings_checkbox_lecture_mode.setGeometry(QtCore.QRect(20, 30, 240, 40))
            self.settings_checkbox_lecture_mode.setObjectName("settings_checkbox_lecture_mode")
            self.settings_checkbox_mute_sound = QtWidgets.QCheckBox(self.settings_outer_box)
            self.settings_checkbox_mute_sound.setGeometry(QtCore.QRect(20, 60, 240, 40))
            self.settings_checkbox_mute_sound.setObjectName("settings_checkbox_mute_sound")
            self.settings_checkbox_startup = QtWidgets.QCheckBox(self.settings_outer_box)
            self.settings_checkbox_startup.setGeometry(QtCore.QRect(20, 90, 240, 40))
            self.settings_checkbox_startup.setObjectName("settings_checkbox_startup")
            self.settings_checkbox_startup.setEnabled(False)
            self.settings_inner_box = QtWidgets.QGroupBox(self.settings_outer_box)
            self.settings_inner_box.setGeometry(QtCore.QRect(10, 0, 391, 291))
            self.settings_inner_box.setObjectName("settings_inner_box")
            self.settings_inner_box.raise_()
            self.settings_checkbox_lecture_mode.raise_()
            self.settings_checkbox_mute_sound.raise_()
            self.settings_checkbox_startup.raise_()
            self.settings_error_label = QtWidgets.QLabel(self.Settings_tab)
            self.settings_error_label.setGeometry(QtCore.QRect(10, 380, 401, 31))
            self.settings_error_label.setObjectName("settings_error_label")

        def setupStatusbar(self, MainWindow):
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)

        def setupTrayIcon(self, MainWindow):
            self.tray_icon = QSystemTrayIcon()
            self.tray_icon.setIcon(QIcon("logo.png"))
            self.tray_icon.setToolTip("Studybuddy System Tray Management")
            self.tray_icon.show()
            self.tray_icon.tray_menu = QtWidgets.QMenu()

        def setupActionsObjects(self, MainWindow):
            self.actionQuit = QtWidgets.QAction(MainWindow)
            self.actionQuit.setObjectName("actionQuit")
            self.actionMinimize_to_tray = QtWidgets.QAction(MainWindow)
            self.actionMinimize_to_tray.setObjectName("actionMinimize_to_tray")
            self.tray_icon.show_action = QtWidgets.QAction("Show", MainWindow)
            self.tray_icon.quit_action = QtWidgets.QAction("Exit", MainWindow)
            self.tray_icon.hide_action = QtWidgets.QAction("Hide", MainWindow)
            self.tray_icon.lecture_action = QtWidgets.QAction("Disable popups", MainWindow)
            self.tray_icon.lecture_action.setCheckable(True)
            self.tray_icon.mute_action = QtWidgets.QAction("Mute", MainWindow)
            self.tray_icon.mute_action.setCheckable(True)
            self.tray_icon.tray_menu.addAction(self.tray_icon.show_action)
            self.tray_icon.tray_menu.addAction(self.tray_icon.hide_action)
            self.tray_icon.tray_menu.addSeparator()
            self.tray_icon.tray_menu.addAction(self.tray_icon.lecture_action)
            self.tray_icon.tray_menu.addAction(self.tray_icon.mute_action)
            self.tray_icon.tray_menu.addSeparator()
            self.tray_icon.tray_menu.addAction(self.tray_icon.quit_action)
            self.tray_icon.show_action.setEnabled(False)
            chbox_mute = self.settings_checkbox_mute_sound.isChecked()
            self.tray_icon.mute_action.setChecked(chbox_mute)
            chbox_lecture = self.settings_checkbox_lecture_mode.isChecked()
            self.tray_icon.lecture_action.setChecked(chbox_lecture)
            self.tray_icon.setContextMenu(self.tray_icon.tray_menu)

        def setupMenuActions(self, MainWindow):
            self.menuHelp.addAction(self.actionQuit)
            self.menuHelp.addAction(self.actionMinimize_to_tray)
            self.menubar.addAction(self.menuHelp.menuAction())

        def setupSettings(self, MainWindow):
            if os.stat(self.setting_file).st_size == 0:
                return
            else:
                with open(self.setting_file, 'r') as f:
                    content = f.read()
                    y = content.split(",")
                    if y[0] == "True":
                        self.settings_checkbox_mute_sound.setChecked(True)
                    if y[1] == "True":
                        self.settings_checkbox_mute_sound.setChecked(True)
                    if self.check_registry_status() is True:
                        self.settings_checkbox_startup.setChecked(True)
                    else:
                        pass

        def setupActionConnections(self, MainWindow):
            self.tray_icon.show_action.triggered.connect(self.handleShowAction)
            self.tray_icon.hide_action.triggered.connect(self.handleTrayIconButton)
            self.tray_icon.quit_action.triggered.connect(self.close_application)
            self.tray_icon.mute_action.triggered.connect(self.toogle_mute_mode_sys_tray)
            self.tray_icon.lecture_action.triggered.connect(self.toogle_lecture_mode_sys_tray)
            self.tray_icon.activated.connect(self.handleTrayIconClicked)
            self.actionQuit.triggered.connect(self.close_application)
            self.actionMinimize_to_tray.triggered.connect(self.handleTrayIconButton)
            self.Notification_save_button.clicked.connect(self.callback_input)
            self.Notification_clear_button.clicked.connect(self.struggle_lineedit.clear)
            self.Notification_clear_button.clicked.connect(self.add_notificaiton_error_label.clear)
            self.saved_subjects_delete_button.clicked.connect(self.delete_notification)
            self.settings_save_button.clicked.connect(self.write_settings)
            self.Clear_button.clicked.connect(self.subject_code_linedit.clear)

        def setupPopuplogic(self, MainWindow):
            for key, value in self.opts.items():
                if key == 'show_now':
                    for key2, value2 in value.items():
                        self.trigger_popup(value2)
                if key == 'show_later':
                    for key3, value3 in value.items():
                        worker = Worker(key3, value3)
                        random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
                        T = QtCore.QThread()
                        T.setObjectName('thread_' + random_string)
                        self.__threads.append((T, worker))
                        worker.moveToThread(T)
                        # Connect worker signal to function to show popup,
                        # such that when the timer is done in worker, it exexutes targeted function:
                        worker.sig_done.connect(self.trigger_popup)
                        worker.sig_finished.connect(self.abort_worker_thread)
                        # Make sure the worker start workingf
                        T.started.connect(worker.work)
                        T.start()

        # Initializes the Mainwindow
        MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        MainWindow.show()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 530)
        MainWindow.setMaximumSize(600, 530)
        MainWindow.setMinimumSize(600, 530)

        # Calls methods to setup various GUI elements
        setupVariables(self, MainWindow)
        setupFiles(self, MainWindow)       # Initializes and creates files.
        setupMenubar(self, MainWindow)     # Initializes and create the menubar.
        setupCentralWidget(self, MainWindow)       # Creates the centralwidget.
        setupGridlayout(self, MainWindow)      # Setup the gridlayout.
        setupTabWidget(self, MainWindow)       # Setup the tabwidget,which hold all tabs.
        setupContentNotificationTab(self, MainWindow)      # Setup content in Studdybuddy tab.
        setupContentSavedSubjectsTab(self, MainWindow)     # Setup content in Saved subjects tab.
        setupContentSettingsTab(self, MainWindow)      # Setup content in settings tab.
        setupSettings(self, MainWindow)      # Setup default settings.
        setupStatusbar(self, MainWindow)       # Setup the statusbar.
        setupTrayIcon(self, MainWindow)      # Initializes and setup the system tray icon.
        setupActionsObjects(self, MainWindow)       # Setup action objects for events.
        setupMenuActions(self, MainWindow)       # Setup actions which are in the menubar.
        self.retranslateUi(MainWindow)       # Set text to objects, make them distinctive in the gui.
        setupActionConnections(self, MainWindow)        # Setup connections and triggers between actions and methods.
        QtCore.QMetaObject.connectSlotsByName(MainWindow)      # Connect slots to signals by names.
        setupPopuplogic(self, MainWindow)       # Check if popups exists, creates threads for them if nescesarry.

# Methods outside of setupUI are placed outside:
# These methods are used by the program more often than
# just the setup, but also during event handling and actions.

    def toogle_mute_mode_sys_tray(self):
        if self.settings_checkbox_mute_sound.isChecked() is True:
            self.settings_checkbox_mute_sound.setChecked(False)
            self.tray_icon.mute_action.setChecked(False)
        else:
            self.settings_checkbox_mute_sound.setChecked(True)
            self.tray_icon.mute_action.setChecked(True)

    def toogle_lecture_mode_sys_tray(self):
        if self.settings_checkbox_lecture_mode.isChecked() is True:
            self.settings_checkbox_lecture_mode.setChecked(False)
            self.tray_icon.lecture_action.setChecked(False)
        else:
            self.settings_checkbox_lecture_mode.setChecked(True)
            self.tray_icon.lecture_action.setChecked(True)
        
                                                            
    def handleTrayIconClicked(self, reason):
        if int(reason) == 2:
            self.handleShowAction()
        else:
            pass

    def handleTrayIconButton(self):
        MainWindow.hide()
        self.tray_icon.show_action.setEnabled(True)
        self.tray_icon.hide_action.setEnabled(False)
        self.tray_icon.showMessage(
            "StudyBuddy",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )
        
# Shows the mainwindow, and enables the system tray hide action
# (making it possible to click on the hide-action).

    def handleShowAction(self):
        self.tray_icon.hide_action.setEnabled(True)
        MainWindow.activateWindow()
        MainWindow.raise_()
        MainWindow.show()
        self.tray_icon.show_action.setEnabled(False)

# Closes the appliation. Called by the exit button in top left corner,
# or by the exit action in the system tray menu.

    def close_application(self):
        choice = QMessageBox.question(QtWidgets.QWidget(MainWindow), 'Warning',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.abort_workers()
            now = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
            with open('log.txt', 'r+') as f:
                data = f.read()
                f.seek(0)
                f.write(now)
                f.truncate()
            self.tray_icon.hide()
            sys.exit()
        else:
            pass

# This mthod is called by Notification_save_button when it is clicked,
# when the user wants to save a new subject. The method does a couple of
# things: 1. It validates the input in the two line-edit fields, respectively
# the subject code, and whatever name is entered in the struggle-lineedit.
# 2. If validation is passed, it creates a new thread in the scrapeworker class
# ,and store a reference of the thread in the list self.__scrapethreads, and
# starts the thread, and disables any buttons and lineedits in the tab.
# 3. It connects the signals in the scrapeworker object to methods in
# MainWindow.
    def callback_input(self):
        (struggle_bool, subject_code_bool) = (self.struggle_lineedit.isModified(),
                                              self.subject_code_linedit.isModified())
        if struggle_bool or subject_code_bool:
            self.name = self.struggle_lineedit.text()
            self.sub_code = self.subject_code_linedit.text()
            if struggle_bool is False:
                self.add_notificaiton_error_label.setText("""You need to give y
                                                          our struggle a name,
                                                          for example a chapter
                                                          or topic which you fi
                                                          nd hard.""")
                return
            elif subject_code_bool is False:
                self.add_notificaiton_error_label.setText("""You need to type i
                                                          n which subject-code
                                                          you are struggling wi
                                                          th""")
                return
            else:
                if ("'" in self.name) or ('"' in self.name) or("'" in self.sub_code) or ('"' in self.sub_code):
                    self.add_notificaiton_error_label.setText("""Single and dou
                                                              ble quotes are no
                                                              t allowed in the
                                                              name and in the s
                                                              ubject-code""")
                    self.subject_code_linedit.clear()
                    self.subject_code_linedit.setModified(False)
                    self.struggle_lineedit.clear()
                    self.struggle_lineedit.setModified(False)
                    return
                self.notifications = self.get_all_notifications()
                if self.get_notification_by_key_value('Name',
                                                      self.name,
                                                      self.notifications)is False:  # Check that the name of the struggle is not taken
                    self.frequency = self.retrieve_checkbox_values()
                    self.now = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
                    self.name_dict["Name"] = self.name
                    self.name_dict["SubjectCode"] = self.sub_code
                    self.name_dict["Registered"] = self.now
                    self.name_dict["FrequencyLength"] = "2"
                    self.name_dict["Frequency"] = self.frequency
                    self.add_notificaiton_error_label.setText("Cheking if subject code exist.. this can take a while..")
                    self.Notification_save_button.setEnabled(False)
                    self.Notification_clear_button.setEnabled(False)
                    self.Clear_button.setEnabled(False)
                    self.subject_code_linedit.setEnabled(False)
                    self.struggle_lineedit.setEnabled(False)
                    self.create_scrapethread(self.sub_code,self.name_dict) # Creates thread and worker
                    return
                else:
                    self.add_notificaiton_error_label.setText("That name for a topic is already taken")
                    self.struggle_lineedit.clear()
                    self.struggle_lineedit.setModified(False)
        else:
            self.add_notificaiton_error_label.setText("You need to enter something as subject code and give a name to what you're struggling with")

    def trigger_popup(self, value):
# The trigger_popup method is one of the most important ones in the application.
# setupPopuplogic calls this method if any popups should show when the program
# starts. The method is later called from threads in worker objects when their
# timer is reached. The method check if the sound is muted, and fills in
# information in the popupbox relevant to the user. If the user click on the
# postpone-button, a new thread with the same notification is created,
# effectively postponing the notification.
        if value['Frequency']:
            if int(value['Frequency']) == 604800000:
                postpone = "One week"
            elif int(value['Frequency']) == 1209600000:
                postpone = "Two weeks"
            else:
                postpone = "One month"
        if self.settings_checkbox_lecture_mode.isChecked() is False:
            if self.settings_checkbox_mute_sound.isChecked() is False:
                self.playsound()
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowModality(0)
            msg_box.setWindowIcon(QtGui.QIcon("logo.png"))
            msg_box.setText(str(value["Name"] + "\nAre you going to read this?"))
            msg_box.setWindowTitle(str(value["SubjectCode"]))
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            postpone_button = msg_box.button(QtWidgets.QMessageBox.No)
            postpone_button.setText('Postpone ' + "(" + postpone + ")")
            yes_button = msg_box.button(QtWidgets.QMessageBox.Yes)
            msg_box.setDefaultButton(postpone_button)
            msg_box.exec_()
            key = 'LastNotification'
            now = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
            if msg_box.clickedButton() == yes_button:
                self.set_notification_key_value(key, value['Name'], now)
            elif msg_box.clickedButton() == postpone_button:
                self.set_notification_key_value(key, value['Name'], now)
                self.create_postponed_workerthread(value)
        else:
            self.create_postponed_workerthread(value)

    def create_scrapethread(self,sub_code,name_dict):
        # Creates scrapeworker object.
        scrapeworker = ScraperWorker(sub_code, name_dict)
        # Creates Qthread.
        T = QtCore.QThread()
        T.setObjectName('thread_' + sub_code)
        # Creates reference in list to manage thread, by appending to list.
        self.__scrapethreads.append((T, scrapeworker))
        # Changes the thread affinity for this object (Qthread T).
        scrapeworker.moveToThread(T)
        # Connect scrapeworker signal to validate method
        scrapeworker.sig_scrape_done.connect(self.validate)
        scrapeworker.sig_scrape_starting.connect(self.push_mainwindow_to_front)
        # Connect scrapeworker signal to abort_worker_thread method.
        scrapeworker.sig_finished.connect(self.abort_worker_thread)
        # Connects the thread T to scrapeworkers scrapework-method,
        # telling it to execute method once thread have started.
        T.started.connect(scrapeworker.scrapework)
        # Start the thread.
        T.start()
        

    def create_postponed_workerthread(self,value):
        random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
        worker = Worker(value['Frequency'],value)
        T = QtCore.QThread()
        T.setObjectName('thread_' + random_string)
        self.__threads.append((T, worker))
        worker.moveToThread(T)
        worker.sig_done.connect(self.trigger_popup)
        worker.sig_finished.connect(self.abort_worker_thread)
        T.started.connect(worker.work)
        T.start()
    

    def write_settings(self):
# This method is called by the save button in the settings tab.
# What it does, is simply check the checkboxes there, and write them to a file
# called settings.txt in working directory.
        lecture_mode = self.settings_checkbox_lecture_mode.isChecked()
        if lecture_mode is True:
            self.tray_icon.lecture_action.setChecked(True)
        mute_mode = self.settings_checkbox_mute_sound.isChecked()
        if mute_mode is True:
            self.tray_icon.mute_action.setChecked(True)
        startup_mode = self.settings_checkbox_startup.isChecked()
        with open("settings.txt",'w') as setting:
            setting.write("" + str(mute_mode) + "," + str(startup_mode))
        setting.close()
        if startup_mode is True:
            if self.check_registry_status() is True:
                pass
            else:
                self.create_registry_startup()
        if startup_mode is False:
            if self.check_registry_status() is False:
                pass
            else:
                self.delete_registry_startup()
        self.settings_error_label.setText("Success, settings saved")

    def quit_and_store(self, identifying_name, value):
# This method is called everytime you click OK on a notification.
# What it does is simply write to file the notification you just clicked OK
# to read.
        key = 'LastNotificationSeen'
        self.set_notification_key_value(key, identifying_name, value)

    def push_mainwindow_to_front(self):
        MainWindow.activateWindow()
        MainWindow.raise_()
        MainWindow.show()
    def delete_notification(self):
# This method is called everytime you delete a subject from the saved subjects
# tab. It simply removes the nofication from the combobox in the GUI, and delete
# the given notification from the notifications.txt file.
        notification = self.list_of_notifications.currentData()
        index_position = self.list_of_notifications.currentIndex()
        self.list_of_notifications.removeItem(index_position)
        self.notifications = self.get_all_notifications()
        if notification in self.notifications :
            self.notifications.remove(notification)
        temp = open('notifications.txt', 'w').close()
        with open('notifications.txt', "a") as f:
            for notification in self.notifications:
                f.write(json.dumps(notification, sort_keys = True))
                f.write("\n")
        f.close()

    def get_all_notifications(self):
# Retrieves all notifications from the notifications.txt file, and return them as
# a list.Each notification is writtenon one line, and is a dictionary. The returned
# list have multiple dictionaires (unless there is only one notification)
        notifications = []
        with open('notifications.txt',"r") as f:
            for line in f:
                notifications.append(json.loads(line))
        f.close()
        return notifications

    def get_notification_by_key_value(self,target_value,key_value,notifications):
# Find and identifies a given notification by its given key:value pair in a big
# list where each notification is a dictionairy.For example: ('hard topic','Name'
# ,list_of_notifications) will search all dictionaries inside the list for with a
# key that have that name.
        for notification in notifications:
            for key, value in notification.items():
                if ((str(key) == str(target_value))and ( str(value) == str(key_value))):
                    return notification
                else:
                    pass
        return False

    def create_registry_startup(self):

# This method uses winreg to create a registry key in the windows registry with
# values that point to running directory, and naming the value "Studybuddy".
# What it effectively does,is registering the application to launch at startup
# when windows start.

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path,
                                 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'Studybuddy', 0,winreg.REG_SZ,self.working_directory+ "\\Studybuddy.py")
            winreg.CloseKey(key)
        except OSError as error:
            return False

    def check_registry_status(self):
# This method check if the application is registered to run at startup,
# returning true if it is, and false if not
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                      self.key_path, 0, access=winreg.KEY_READ)
        try:
            key_value = winreg.QueryValueEx(key,"Studybuddy")
            if key_value:
                winreg.CloseKey(key)
                return True
            else:
                winreg.CloseKey(key)
                return False
        except OSError as error:
            return False

    def delete_registry_startup(self):
# This method deletes the key which allows the program to run at startup on
# windows. If there is no such key to delete, False is returned. 
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(key, 'Studybuddy')
            winreg.CloseKey(key)
            return True
        except OSError as error:
            return False

    def add_notification_to_file(self,dictionary_notification):
# Writes the notification to file, appending it to other, existing notifications (if any).
        with open('notifications.txt',"a") as f:
            f.write(json.dumps(dictionary_notification, sort_keys = True))
            f.write("\n")
        f.close()

    # Check if given key:value pair exist in a given dictionary, and return true if it does.
    def check_if_notification_data_exist(self,target_key,target_value,notification):
        if notification[target_key] == target_value:
            return True
        else:
            return False

    # TODO: INSERT COMMENT
    def set_notification_key_value(self,key, identifying_name, value):
        target_value = 'Name'
        target_notification = self.get_notification_by_key_value(target_value,identifying_name,self.notifications)
        notifications = self.notifications
        for notification in notifications:
            if notification[target_value]== identifying_name:
                notifications.remove(notification)
                break
            else:
                pass
        target_notification[key] = value
        notifications.append(target_notification)
        temp = open('notifications.txt', 'w').close()
        with open('notifications.txt',"a") as f:
            for popup in notifications:
                f.write(json.dumps(popup, sort_keys = True))
                f.write("\n")
        f.close()

    def next_popup_time(self,notification,opts, target_key):
        not_dict = {}
        frequency = notification['Frequency']
        now = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
        last_notification = notification[target_key]
        datetime_young = datetime.strptime(last_notification, "%y-%m-%d-%H-%M-%S")  # Formatvalg
        datetime_now = datetime.strptime(now, "%y-%m-%d-%H-%M-%S")  # Formatvalg
        time_delta = datetime_now - datetime_young
        frequency_millisecond = (timedelta(milliseconds=int(frequency)).total_seconds())*1000
        to_milli = time_delta.total_seconds()*1000
        result = to_milli - frequency_millisecond
        if result > 0:
            not_dict[result] = notification
            if 'show_now' in opts.keys():
                opts['show_now'][result] = notification
                return opts
            else:
                opts['show_now']= {result:notification}
            return opts
        elif result <= 0:
            result = int(result *(-1))
            not_dict[result] = notification
            if 'show_later' in opts.keys():
                opts['show_later'][result] = notification
            else:
                opts['show_later'] = {result: notification}
            return opts

    
    def get_time_of_notification(self,notifications):
        opts = {}
        for notification in notifications:
            if ((notification['LastNotificationSeen'] == 'True' or notification['LastNotificationSeen'] == 'False')
                and notification['LastNotification'] != ""):
                target_key = 'LastNotification'
                opts = self.next_popup_time(notification,opts, target_key)
            elif notification['LastNotification'] == "":
                target_key = 'Registered'
                opts = self.next_popup_time(notification,opts, target_key)
            else:
                pass
        return opts

    def real_playsound(self):
        sound = pyglet.media.load('alarm2wav.wav')
        sound.play()
        pyglet.app.run()

    def playsound(self):
        global player_thread
        player_thread = Thread(target=self.real_playsound,daemon =True)
        player_thread.start()



    def retrieve_checkbox_values(self):
        if self.frequency_radiobutton_1.isChecked():
            frequency = 604800000
            return frequency
        elif self.frequency_radiobutton_2.isChecked():
            frequency = 1209600000
            return frequency
        else:
            frequency = 2419200000
            return frequency

    def validate(self, notification):
        self.Notification_save_button.setEnabled(True)
        self.Notification_clear_button.setEnabled(True)
        self.Clear_button.setEnabled(True)
        self.subject_code_linedit.setEnabled(True)
        self.struggle_lineedit.setEnabled(True)
        if notification['Scraperesult'] is True:
            if notification.pop('Scraperesult', None) != None:
                self.add_notification_to_file(notification)
            self.list_of_notifications.clear()
            self.notifications = self.get_all_notifications()
            self.saved_subjects_delete_button.setEnabled(True)
            for noti in self.notifications:
                self.list_of_notifications.addItem(noti['Name']+ "- Fag:"+noti['SubjectCode'],noti)
            self.add_notificaiton_error_label.setText("Success! Subject code was found, and notification have been created!")
            self.subject_code_linedit.clear()
            self.subject_code_linedit.setModified(False)
            self.struggle_lineedit.clear()
            self.struggle_lineedit.setModified(False)
        else:
            self.add_notificaiton_error_label.setText("The subjectcode you entered is not found.. please try again with a new one")
            self.subject_code_linedit.clear()
            self.subject_code_linedit.setModified(False)
            self.struggle_lineedit.clear()
            self.struggle_lineedit.setModified(False)


    def abort_worker_thread(self,thread_name):
        quitted = False
        if self.__threads:
            index = 0
            for thread, worker in self.__threads:
                temp_thread = thread.objectName()
                temp_thread_name = str(temp_thread)
                if temp_thread == thread_name:
                    thread.requestInterruption()
                    thread.quit()
                    thread.wait()
                    self.__threads.pop(index)
                    quitted = True
                    break
                else:
                    index += 1
        if self.__scrapethreads and quitted == False:
            index = 0
            for thread, worker in self.__scrapethreads:
                temp_thread = thread.objectName()
                temp_thread_name = str(temp_thread)
                if temp_thread == thread_name:
                    thread.quit()
                    thread.wait()
                    self.__scrapethreads.pop(index)
                    quitted = True
                    break
                else:
                    index += 1
        else:
            pass

    def abort_workers(self):
        if self.__threads:
            for thread, worker in self.__threads:# note nice unpacking by Python, avoids indexing
                thread.requestInterruption()
                thread.quit() # this will quit **as soon as thread event loop unblocks**
                thread.wait()  # <- so you need to wait for it to *actually* quit
        if self.__scrapethreads:
            for thread, worker in self.__scrapethreads:
                # thread.requestInterruption()
                thread.quit()  # this will quit **as soon as thread event loop unblocks**
                thread.wait()
        else:
            pass
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Studybuddy"))
        MainWindow.setWindowIcon(QIcon("logo.png"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Frequency"))
        self.frequency_radiobutton_1.setText(_translate("MainWindow", "Once a week"))
        self.frequency_radiobutton_2.setText(_translate("MainWindow", "Every other week"))
        self.frequency_radiobutton_3.setText(_translate("MainWindow", "Once a month"))
        self.Notification_save_button.setText(_translate("MainWindow", "Save"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Enter subject"))
        self.subject_code_linedit.setPlaceholderText(_translate("MainWindow", "Type in subject code... example: TDT4100"))
        self.Clear_button.setText(_translate("MainWindow", "Clear"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Description"))
        self.struggle_lineedit.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Whatsthis</p></body></html>"))
        self.struggle_lineedit.setPlaceholderText(_translate("MainWindow", "What is your struggle?"))
        self.Notification_clear_button.setText(_translate("MainWindow", "Cancel"))
        self.add_notificaiton_error_label.setText(_translate("MainWindow", ""))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Add_notification_tab), _translate("MainWindow", "StudyBuddy"))
        self.groupBox.setTitle(_translate("MainWindow", "Notification list"))
        self.saved_subjects_delete_button.setText(_translate("MainWindow", "Delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Saved_subjects_tab), _translate("MainWindow", "Manage notifications"))
        self.settings_save_button.setText(_translate("MainWindow", "Save"))
        self.settings_checkbox_lecture_mode.setText(_translate("MainWindow", "Disable popups and mute at the same time"))
        self.settings_checkbox_mute_sound.setText(_translate("MainWindow", "Mute sound from popups"))
        self.settings_checkbox_startup.setText(_translate("MainWindow", "Start program at windows startup"))
        self.settings_inner_box.setTitle(_translate("MainWindow", "Settings"))
        self.settings_error_label.setText(_translate("MainWindow", ""))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Settings_tab), _translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionMinimize_to_tray.setText(_translate("MainWindow", "Minimize to tray"))
        self.actionMinimize_to_tray.setShortcut(_translate("MainWindow", "Ctrl+M"))
        
class ScraperWorker(QObject):
    """
    Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
    """
    sig_scrape_done = pyqtSignal([dict])
    sig_scrape_starting = pyqtSignal()
    sig_finished = pyqtSignal(str)

    def __init__(self, subjectcode, notification):
        super().__init__()
        self.subjectcode = subjectcode
        self.notification = notification
        self.error_message = ""
    def scrapeCoursePage(self):
        browser = webdriver.Chrome()
        browser.set_window_position(0, 0)
        browser.set_window_size(0, 0)
        #sjekker om det er skrivd noe i tekstfeltet, og søker deretter opp dette i NTNU sin nettside med emneoversikt
        course = self.subjectcode
        self.sig_scrape_starting.emit()
        url = "http://www.ntnu.no/web/studier/emnesok#semester=2016&gjovik=true&trondheim=true&alesund=true&faculty=-1&institute=-1&multimedia=false&english=false&phd=false&courseAutumn=true&courseSpring=true&courseSummer=true&pageNo=5&season=spring&sortOrder=ascTitle&searchQueryString=" + self.subjectcode +""
        browser.get(url)
        self.sig_scrape_starting.emit()
        browser.implicitly_wait(3)
        #Legger til alle emnekodene som finnes under søkeordet som brukeren har skriv inn i en liste:
        course_element = browser.find_elements_by_xpath("//td[@class='coursecode']")
        courses = [x.text for x in course_element]
        browser.quit()
        if ((not courses) or (course not in courses)):
            return False
            #Sjekker at faget finnes:
        if course.upper() in courses:
            return True
        else:
            return False
        
    def scrapework(self):
        thread_name = QThread.currentThread().objectName()
        scraperesult = self.scrapeCoursePage()
        self.notification['Scraperesult']= scraperesult
        self.sig_scrape_done.emit(self.notification)
        self.sig_finished.emit(thread_name)


    # Retrives the input entered in the lineEdit object, validates it, and if valid, write the new notification to file.

class Worker(QObject):
    """
    Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
    """
    sig_done = pyqtSignal([dict])  # worker id: emitted at end of work()
    sig_finished = pyqtSignal(str)

    def __init__(self, timer, noti):
        super().__init__()
        self.timer = timer
        self.noti = noti
        self.isRunning = True



    @pyqtSlot()
    def work(self):
        """
        Pretend this worker method does work that takes a long time. During this time, the thread's
        event loop is blocked, except if the application's processEvents() is called: this gives every
        thread (incl. main) a chance to process events, which in this sample means processing signals
        received from GUI (such as abort).
        """
        thread_name = QThread.currentThread().objectName()
        self.noti['Threadname']= str(thread_name)
        y = random.randint(30000,300000)
        while self.isRunning == True:
            for x in range (0,y + 300,300):
                b = QThread.currentThread().isInterruptionRequested()
                if b == True:
                    self.isRunning == False
                    break
                sleep(0.3)
                if x >= y:
                    self.isRunning == False
                    self.sig_done.emit(self.noti)
                    break
                else:
                    pass
            break
        app.processEvents()
        self.sig_finished.emit(thread_name)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
