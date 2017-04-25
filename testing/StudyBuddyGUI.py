# -*- coding:utf-8 -*_
# Importing all the necessary modules
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from Studybuddy import Ui_MainWindow


class StudyBuddyGUI(QtWidgets.QMainWindow):

    # Initialize the program.
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    # A method that returns the name of the save-button
    def check_equal_text_save_button(self):
        save_button = self.ui.Notification_save_button.text()
        return save_button

    # A method that returns the name of the clear-button
    def check_equal_text_clear_button(self):
        clear_button = self.ui.Clear_button.text()
        return clear_button

    # A method that returns the name of the cancel-button
    def check_equal_text_cancel_button(self):
        cancel_button = self.ui.Notification_clear_button.text()
        return cancel_button

    # A method that sets the text for the given line edit
    def check_cancel_button(self):
        struggle_text = self.ui.struggle_lineedit.setText("Hei på deg")

    # A method that sets the text for the given line edit
    def check_clear_button_subject(self):
        return self.ui.subject_code_linedit.setText("TDT4100")

    # Getter method for fetching actionQuit
    def get_action_quit(self):
        return self.ui.actionQuit

    # Getter method for fetching a check box
    def get_mute_box(self):
        return self.ui.settings_checkbox_mute_sound
