# -*- coding:utf-8 -*_
# Importing all the necessary modules for testing
import string
from unittest import TestCase
from collections import Counter
from datetime import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from Studybuddy import *
from StudyBuddyGUI import StudyBuddyGUI

# The program starts
app = QApplication(sys.argv)


class TestStudyBuddy(TestCase):

    # --------------------------- METHOD TESTING --------------------------- #
    
    # Initialize StudyBuddyGUI, which contains the program and basic methods to test the GUI.
    def setUp(self):
        self.form = StudyBuddyGUI()
        self.ui_window = Ui_MainWindow()

    #  Testing if the given files exist.
    def test_file_exist(self):
        self.assertTrue(os.path.isfile("C:/Users/Duc/Desktop/notifications.txt"), True)
        self.assertTrue(os.path.isfile("C:/Users/Duc/Desktop/log.txt"), True)
        self.assertTrue(os.path.isfile("C:/Users/Duc/Desktop/settings.txt"), True)

    #  Test if the function get_all_notifications returns all the elements in the file.
    def test_correct_num_lines(self):
        noti_length = len(self.ui_window.get_all_notifications())
        with open("C:/Users/Duc/Desktop/notifications.txt") as f:
            num_lines = sum(1 for _ in f)
        self.assertEqual(noti_length, num_lines)

    #  Test if the function check_if_notification_data_exist works by giving a false key to check if the key exists.
    def test_noti_not_exist(self):
        noti_lst = self.ui_window.get_all_notifications()
        target_key = 'Name'
        target_value = 'Test1'
        check = None
        for i in range(0, len(noti_lst)):
            check = self.ui_window.check_if_notification_data_exist(target_key, target_value, noti_lst[i])
            if check:
                break
        self.assertFalse(check, True)

    # Basically the same as the one above, but here we check for a key that does exist.
    def test_check_if_data_exist(self):
        noti_lst = self.ui_window.get_all_notifications()
        target_key = 'Name'
        target_value = 'test22'
        check = None
        for i in range(0, len(noti_lst)):
            check = self.ui_window.check_if_notification_data_exist(target_key, target_value, noti_lst[i])
            if check:
                break
        self.assertTrue(check, True)

    #  Test if we have the show_now-key.
    def test_key_exist_now(self):
        find_key = 'show_now'
        noti_lst = self.ui_window.get_all_notifications()
        options = self.ui_window.get_time_of_notification(noti_lst)
        check = find_key in options.keys()
        self.assertTrue(check, True)

    #  Test if we have the show_later-key.
    def test_key_exist_later(self):
        find_key = 'show_later'
        noti_lst = self.ui_window.get_all_notifications()
        options = self.ui_window.get_time_of_notification(noti_lst)
        check = find_key in options.keys()
        self.assertTrue(check, True)

    #  If test_key_exist_now was successful, we will now test if show_now has the correct values, which should be positive values.
    def test_correct_key_value_now(self):
        noti_lst = self.ui_window.get_all_notifications()
        options = self.ui_window.get_time_of_notification(noti_lst)
        check = None
        for key, value in options.items():
            for key2 in value.keys():
                check = key2 > 0
                if check is False:
                    break
        self.assertTrue(check, True)
        
    # Check if show_later has the correct values, which should be negative values, because the time and date has not yet reached the given notification time.
    # The function returns a list of results.
    def test_correct_key_value_later(self):
        result_lst = []
        noti_lst = self.ui_window.get_all_notifications()
        check = None
        for notification in noti_lst:
            if ((notification['LastNotificationSeen'] == 'True' or notification['LastNotificationSeen'] == 'False') and notification['LastNotification'] != ""):
                target_key = 'LastNotification'
                frequency = notification['Frequency']
                now = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
                last_notification = notification[target_key]
                datetime_young = datetime.strptime(last_notification, "%y-%m-%d-%H-%M-%S")  # Formatvalg
                datetime_now = datetime.strptime(now, "%y-%m-%d-%H-%M-%S")  # Formatvalg
                time_delta = datetime_now - datetime_young
                frequency_millisecond = (timedelta(milliseconds=int(frequency)).total_seconds())*1000
                to_milli = time_delta.total_seconds()*1000
                result = to_milli - frequency_millisecond
                result_lst.append(result)
            elif notification['LastNotification'] == "":
                target_key = 'Registered'
                frequency = notification['Frequency']
                now = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
                last_notification = notification[target_key]
                datetime_young = datetime.strptime(last_notification, "%y-%m-%d-%H-%M-%S")  # Formatvalg
                datetime_now = datetime.strptime(now, "%y-%m-%d-%H-%M-%S")  # Formatvalg
                time_delta = datetime_now - datetime_young
                frequency_millisecond = (timedelta(milliseconds=int(frequency)).total_seconds())*1000
                to_milli = time_delta.total_seconds()*1000
                result = to_milli - frequency_millisecond
                result_lst.append(result)
        for res in result_lst:
            check = res < 0
            if check is True:
                break
        self.assertTrue(check, True)
        return result_lst

    # Getting keys from the notification-file and check if the function test_correct_key_value returns the same list of values.
    def test_correct_keys(self):
        result_lst = self.test_correct_key_value_later()
        noti_lst = self.ui_window.get_all_notifications()
        options = self.ui_window.get_time_of_notification(noti_lst)
        value_lst = [key2 for key, value in options.items() for key2, value2 in value.items()]
        minimum = float((-1) * (min(value_lst)))
        value_lst.remove(min(value_lst))
        value_lst.append(minimum)
        self.assertEqual(result_lst, value_lst)

    # Test that they key 'Name' has the right format.
    def test_check_name_format(self):
        struggle_lst = []
        noti_lst = self.ui_window.get_all_notifications()
        noti_dict = self.ui_window.get_time_of_notification(noti_lst)
        count = 0
        for keys, value in noti_dict.items():
            for keys2, value2 in value.items():
                struggle_lst.append(value[keys2]['Name'])
        for struggle in struggle_lst:
            if struggle.find("'") > 0 or struggle.find('"') > 0:
                count += 1
        self.assertEqual(count, 0)

    # The fucntion checks if the frequencies in the file are correct when they get added.
    def test_valid_frequency(self):
        frequency = [86400000, 604800000, 60000, 6000000]
        ui_window = Ui_MainWindow()
        noti_lst = self.ui_window.get_all_notifications()
        temp = []
        noti_dict = self.ui_window.get_time_of_notification(noti_lst)
        check = None
        for keys, value in noti_dict.items():
            for keys2, value2 in value.items():
                temp.append(value[keys2]['Frequency'])
        frequency_lst = list(dict.fromkeys(freq for freq in temp))
        for freq in frequency_lst:
            check = freq in frequency
            if check is False:
                break
        self.assertTrue(check, True)

    # This function checks for duplicate names. Uses the counter - module to put the names in a dictionary with a value.
    # Value == 1 = No duplicates
    # Value == 2 = Duplicates
    def test_check_duplicate(self):
        noti_lst = self.ui_window.get_all_notifications()
        struggle_lst = []
        noti_dict = self.ui_window.get_time_of_notification(noti_lst)
        count = 0
        for keys, value in noti_dict.items():
            for keys2, value2 in value.items():
                struggle_lst.append(value[keys2]['Name'])
        check_dup = Counter(struggle_lst).values()
        for value in check_dup:
            if value > 1:
                count += 1
        self.assertEqual(count, 0)
        
    # The function checks if the add_notification_function works. Deletes the notification afterwards, because it is for testing only. 
    def test_check_add_function(self):
        noti_length = len(self.ui_window.get_all_notifications())
        random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
        test_dict = {"Frequency": 60000, "FrequencyLength": "2", "LastNotification": "",
                        "LastNotificationSeen": "False","Name": random_string, "Registered": "17-04-15-13-56-04", "SubjectCode": "TDT4100"}
        self.ui_window.add_notification_to_file(test_dict)
        new_length = len(self.ui_window.get_all_notifications())
        self.assertNotEqual(noti_length, new_length)
        read_file = open("C:/Users/Duc/Desktop/notifications.txt")
        lines = read_file.readlines()
        read_file.close()
        w = open("C:/Users/Duc/Desktop/notifications.txt",'w')
        w.writelines([item for item in lines[:-1]])
        w.close()

    # Test if we can get a notification, and if there is a notification with that given key and value.
    def test_get_notification_by_key_value(self):
        noti_lst = self.ui_window.get_all_notifications()
        target_key = 'Name'
        target_value = 'test22'
        check = self.ui_window.get_notification_by_key_value(target_key, target_value, noti_lst)
        self.assertTrue(check is not None, True)

    # Test if the set_notification_by_key_value works by changing a value inside the notification-file.
    # After the change, we go through the file and check if the function actually changed the value
    def test_set_notification_by_key_value(self):
        noti_lst = self.ui_window.get_all_notifications()
        options = self.ui_window.get_time_of_notification(noti_lst)
        check = None
        target_value = 'Name'
        identifying_name = 'test22'
        target_notification = self.ui_window.get_notification_by_key_value(target_value,identifying_name, noti_lst)
        notifications = noti_lst
        for notification in noti_lst:
            if notification[target_value] == identifying_name:
                noti_lst.remove(notification)
                break
            else:
                pass
        target_notification['LastNotificationSeen'] = 'True'
        notifications.append(target_notification)
        temp = open('C:/Users/Duc/Desktop/notifications.txt', 'w').close()
        with open('C:/Users/Duc/Desktop/notifications.txt',"a") as f:
            for popup in notifications:
                f.write(json.dumps(popup, sort_keys=True))
                f.write("\n")
        f.close()
        for key, value in options.items():
            for key2, value2 in value.items():
                if value2['Name'] == 'test22':
                    if value2['LastNotificationSeen'] == 'True':
                        check = True
        self.assertTrue(check, True)

    # --------------------------- GUI TESTING --------------------------- #
    
    # Test the defaults, like if a radiobutton has the correct name, if a line edit has something written in it, if the window pop up when it should,
    # and check if a given tab is visible or not.
    def test_defaults(self):
        self.assertEqual(self.form.ui.frequency_radiobutton_1.text(), "Once a week")
        self.assertEqual(self.form.ui.frequency_radiobutton_2.text(), "Every other week")
        self.assertEqual(self.form.ui.frequency_radiobutton_3.text(), "Once a month")
        self.assertEqual(self.form.check_equal_text_save_button(), "Save")
        self.assertEqual(self.form.check_equal_text_cancel_button(), "Cancel")
        self.assertEqual(self.form.check_equal_text_clear_button(), "Clear")
        self.assertEqual(self.form.ui.struggle_lineedit.text(), "")
        self.assertEqual(self.form.ui.subject_code_linedit.text(), "")
        self.form.show()
        self.assertTrue(QTest.qWaitForWindowExposed(self.form), True)
        self.assertTrue(self.form.ui.Add_notification_tab.isVisible(), True)
        self.assertFalse(self.form.ui.Saved_subjects_tab.isVisible(), False)        
        self.assertFalse(self.form.ui.Settings_tab.isVisible(), False)  

    # Test mouseclicks by setting a text for a line edit and press the cancel/clear buttons to check if the buttons works.
    def test_clear_button(self):
        self.form.check_cancel_button()
        self.form.check_clear_button_subject()
        cancel_button = self.form.ui.Notification_clear_button
        clear_button = self.form.ui.Clear_button
        QTest.mouseClick(cancel_button, Qt.LeftButton)
        QTest.mouseClick(clear_button, Qt.LeftButton)
        check_cancel = self.form.ui.struggle_lineedit.text()
        check_clear = self.form.ui.subject_code_linedit.text()
        self.assertEqual(check_cancel, "")
        self.assertEqual(check_clear, "")

    # Test if the function of the error label works and if the save button clears out the struggle line.
    def test_error_label(self):
        save_button = self.form.ui.Notification_save_button
        QTest.mouseClick(save_button, Qt.LeftButton)
        check_struggle = self.form.ui.struggle_lineedit.text()
        check_subject = self.form.ui.subject_code_linedit.text()
        error_label = self.form.ui.add_notification_error_label.text()
        self.assertEqual(check_struggle, "")
        self.assertEqual(check_subject, "")
        self.assertEqual(error_label, "You need to enter something as subject code and give a name to what you're struggling with")

    # Test if the save button also clear out the struggle line.
    def test_save_button(self):
        self.form.ui.struggle_lineedit.setText("Kapittel 7: Epler og bananer")
        save_button = self.form.ui.Notification_save_button
        check_save = self.form.ui.struggle_lineedit.text()
        self.assertTrue(check_save, "Kapittel 7: Epler og bananer")
        QTest.mouseClick(save_button, Qt.LeftButton)
        self.assertTrue(check_save, "")

    # Test if the option to exit the program works. 
    def test_exit_option(self):
        self.form.show()
        if self.form.get_action_quit().isEnabled():
            self.form.close()
        self.assertFalse(QTest.qWaitForWindowExposed(self.form), False)

    # Test if a check box is checked when the program starts
    def test_check_box(self):
        mute_box = self.form.get_mute_box().isChecked()
        self.assertFalse(mute_box, False)
