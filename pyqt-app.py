# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basic.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!
import sys
import time
from time import sleep
from threading import Thread
import threading
import pyglet
import datetime
from datetime import *
import json
import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator


#---------------------------------------------------
    # INSERT COMMENT
#---------------------------------------------------

notification_window = False
name_dict = {"SubjectCode": "", "Frequency": "", "Name" : "", "FrequencyLength" : "", 'LastNotification': "", "LastNotificationSeen": "False"}
                
'''
if notification_window == True:
    playsound(self)'''

def real_playsound(self):
    sound = pyglet.media.load('alarm2wav.wav')
    sound.play()
    pyglet.app.run()

def playsound(self):
    global player_thread
    player_thread = Thread(target=self.real_playsound)
    player_thread.start()



# Class achitechture:
# Mainwindow
#   CentralWidget
#       verticalLayoutWidget & VerticalLayout
#           groupBox
#               radioButton
#               radioButton_2
#               radioButton_ 3
#           label (text)
#           lineedit (input text)
#           label_2(text, empty at the moment (you cant see it if you run file))
#           horizontallayout (QtWidgets.QHBoxLayout())
#               push_btn
#               push_btn2
#   Menubar
#       MenuRexx
#           ActionAvslutt



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        self.notifications = self.get_all_notifications()
        opts = self.get_time_of_notification(self.notifications)
        # MainWindow style and initialization
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
        
        # CentralWidge initialization
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Initial layouts. VerticalLayoutWidget is inside centralvidget, and
        # VerticalLaout is inside verticalLayoutsWidget
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 10, 371, 371))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0,0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Creates a groupbox with 3 radio buttons and assign
        # it to the Vertical Layout and VerticalLayoutWidget
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 40, 289, 17))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(True)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(10,60, 289,17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_3.setGeometry(QtCore.QRect(10, 80, 289, 17))
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout.addWidget(self.groupBox)

        # Creates a label, and a line edit in Vertical Layout
        # and VerticalLayoutWidget
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.label.setText("Skriv inn navn på temaet")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)

        # Validation of lineEdit:
        # self.lineEdit.setInputMask("ABCDEFGH")
        # self.lineEdit.setMaxLength (140)
        # reg_exp_input  = QRegExp()
        # reg_exp_input.setPattern("[^'"]")
        # input_validator = QRegExpValidator(reg_exp_input, self.lineEdit)
        # self.lineEdit.setValidator(input_validator)


        
        
        # Empty label, meant to be "invisble", but if invalid input
        # is entered, it shows up with the error msg
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        # Creates a horizontalBox Layout with 2 buttons in the
        # Vertical Layout and VerticalLayoutWidget
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.callback_input)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        # No idea what this is :) Autogenereated stuff.
        self.groupBox.raise_()
        self.label.raise_()
        self.lineEdit.raise_()
        self.label_2.raise_()

        # Sets centralwidget as centralwidget of the window... 
        MainWindow.setCentralWidget(self.centralwidget)

        # Creates menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 499, 21))
        self.menubar.setObjectName("menubar")
        
        # create menu Rexx 
        self.menuRexx = QtWidgets.QMenu(self.menubar)
        self.menuRexx.setObjectName("menuRexx")
        
        # create menubar in in mainwindow
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAvslutt = QtWidgets.QAction(MainWindow)
        self.actionAvslutt.setObjectName("actionAvslutt")
        self.menubar.addAction(self.menuRexx.menuAction())
        self.actionAvslutt.triggered.connect(self.close_application)
        self.menuRexx.addAction(self.actionAvslutt)
        self.actionTest = QtWidgets.QAction(MainWindow)
        self.actionTest.setObjectName("actionTest")
        self.menuRexx.addAction(self.actionTest)
        MainWindow.show()
        

        # Popup-logic
        self.mylist = []
        for key, value in opts.items():
            if key == 'show_now':
                for key2, value2 in value.items():
                    now2 = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
                    notification_window = True
                    key_now = 'LastNotification'
                    self.trigger_popup(value2)
                    #self.set_notification_key_value(key_now, value2['Name'], now2,self.notifications)
                    print('Showing normal popup now...')
            elif key == 'show_later':
                print("Done with normal popups now")
                for key3, value3 in value.items():
                    if value3['LastNotificationSeen'] == 'True':
                        key_later = 'LastNotification'
                        now3 = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
                        key4 = 1000
                        thread = threading.Thread(target=Ui_MainWindow.popupTimer, args = (self,key3,value3))
                        thread.start()
                        # self.set_notification_key_value(key_later, value3['Name'], now3,self.notifications)
                    else:
                        pass
        


        # Dont ask. 
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # No idea, but sets names (NOT VALUES) on stuff in the GUI. 
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Frekvens"))
        self.radioButton.setText(_translate("MainWindow", "En gang i uken"))
        self.radioButton_2.setText(_translate("MainWindow", "Annehver uke"))
        self.radioButton_3.setText(_translate("MainWindow", "En gang i måneden"))
        self.label.setText(_translate("MainWindow", "Legg til navn på temaet"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Kul text"))
        self.pushButton_2.setText(_translate("MainWindow", "Lagre"))
        self.pushButton.setText(_translate("MainWindow", "Avbryt"))
        self.menuRexx.setTitle(_translate("MainWindow", "Rexx"))
        self.actionAvslutt.setText(_translate("MainWindow", "Avslutt"))
        self.actionAvslutt.setShortcut(_translate("MainWindow", "Ctrl+Q"))


    # Closes the appliation. Called by the exit button in top left corner. 
    def close_application(self):
        choice = QMessageBox.question(QtWidgets.QWidget(MainWindow), 'Warning',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if choice == QMessageBox.Yes:
            now = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
            with open('log.txt', 'r+') as f:
                data = f.read()
                f.seek(0)
                f.write(now)
                f.truncate()
            sys.exit()
        else:
            pass

    # Retrives the input entered in the lineEdit object, validates it, and if valid, write the new notification to file.
    def callback_input(self):
        if self.lineEdit.isModified():
            frequency = 0
            name = str(self.lineEdit.text())
            if ("'"  or '"' in name) :
                self.label_2.setText("Single and double quotes are not allowed in the name")
                self.lineEdit.clear()
                self.lineEdit.setModified(False)
                return
            self.notifications = self.get_all_notifications()
            if self.get_notification_by_key_value('Name',name,self.notifications) == False:
                if self.radioButton.isChecked():
                    frequency = 604800000
                elif self.radioButton_2.isChecked():
                    frequency = 1209600000
                else:
                    frequency = 2419200000
                now = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
                name_dict["Name"] = name
                name_dict["SubjectCode"] = "TDT4160"
                name_dict["Registered"]= now
                name_dict["FrequencyLength"]= "2"
                name_dict["Frequency"] = frequency
                self.add_notification_to_file(name_dict)
                print("Adding notification to notifications.txt...")
                print("Added the notification : " + str(name_dict) + "... to the file")
                self.label_2.setText("Success! Notification added.")
                self.lineEdit.clear()
                self.lineEdit.setModified(False)
            else:
                if "'" in name or '"' in name :
                    self.label_2.setText("Single and double quotes are not allowed in the name")
                    self.lineEdit.clear()
                    self.lineEdit.setModified(False)
                else:
                    self.label_2.setText("That name for a topic is allready taken")
                    self.lineEdit.clear()
                    self.lineEdit.setModified(False)
            
        else:
            self.label_2.setText("You need to enter something in the name field!")
            pass



    def popupTimer(self,key,value):
        print("Popup will be deployed in: " + str(int(key/1000))+"...seconds"+"\n")
        for x in range(key,-1,-1000):
            sleep(1)
            print("Deploying popup in" +str(x/1000)+" seconds ." +"\n")
            print("This applies to: "+ str(value["Name"]))
            if x <= 0:
                print("Showing delayed popup now!")
                Ui_MainWindow.trigger_popup(self,value)
        
                

    def trigger_popup(self,value):
        print("triggering popup...")
        choice = QMessageBox.question(QtWidgets.QWidget(MainWindow), 'Reading reminder!',
                                      "You need to read now. Are you gonna read this topic?", QMessageBox.Yes |
                                      QMessageBox.No, QMessageBox.No)
        if (choice == QMessageBox.Yes ):
            now = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
            self.quit_and_store(value['Name'], "True")
            pass
        else:
            pass
        
    def quit_and_store(self, identifying_name, value):
        key = 'LastNotificationSeen'
        self.set_notification_key_value(key, identifying_name, value)

    # Retrieves all notifications from the notifications.txt file, and return them as a list.Each notification is written
    # on one line, and is a dictionary. The returned list have multiple dictionaires (unless there is only one notification)
    def get_all_notifications(self):
        notifications = []
        with open('notifications.txt',"r") as f:
            for line in f:
                notifications.append(json.loads(line))
        f.close()
        return notifications

    # Find and identifies a given notification by its given key:value pair in a big list where each notification is a dictionairy.
    # For example: ('hard topic','Name',list_of_notifications) will search all dictionaries
    # inside the list for with a key that have that name.
    def get_notification_by_key_value(self,target_value,key_value,notifications):
        for notification in notifications:
            for key, value in notification.items():
                if ((str(key) == str(target_value))and ( str(value) == str(key_value))):
                    return notification
                else:
                    pass
        return False

    # Writes the notification to file, appending it to other, existing notifications (if any).
    def add_notification_to_file(self,dictionary_notification):
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
        if result > 0 :
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
                print("Existing keys in show_later, adding:")
                print(result)
                opts['show_later'][result] = notification
            else:
                print("No existing keys in show_later, adding:")
                print(result)
                opts['show_later']= {result:notification}
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
        print("Ferdig med tidsberegninger for hver notifikasjon...")
        return opts

    def real_playsound(self):
        sound = pyglet.media.load('alarm2wav.wav')
        sound.play()
        pyglet.app.run()

    def playsound(self):
        global player_thread
        player_thread = Thread(target=self.real_playsound)
        player_thread.start()
                 

'''class popupobject(Ui_MainWindow):
    def __init__(self,Ui_MainWindow):
        self.value = value
        self.trigger_popup(self,value)
        self.show()
    def trigger_popup(self,value):
        print("triggering popup...")
        self.msg = QtWidgets.QMessageBox()
        self.msg.setText("This is a message box")
        self.msg.setInformativeText("This is additional information")
        self.msg.setWindowTitle("MessageBox demo")
        self.msg.setDetailedText(str(value['Name']))
        self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # self.choice = QMessageBox.question(QtWidgets.QWidget(MainWindow), 'Reading reminder!',
                                      # "You need to read now. Are you gonna read this topic?", QMessageBox.Yes |
                                      # QMessageBox.No, QMessageBox.No)
        # self.choice.text(str(value['Name']))
        if self.msg == QMessageBox.Yes:
            now = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
            quit_and_store(self, value['Name'], "True")
            print('quit application')
        else:
            pass
            '''

class Popupthread(QtCore.QThread):

    def __init__(self,):
        QThread.__init__(self)
        

    def __del__(self):
        self.wait()

    def run(self):
        pass
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

