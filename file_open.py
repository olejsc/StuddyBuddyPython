import tkinter
from tkinter import *
import datetime
import json

class FileHandler(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)
        menubar = Menu(root)
        root.config(menu=menubar)
        # define menubar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.quit_application)
        menubar.add_cascade(label="File", menu=filemenu)
    
    def quit_application (self):
        now = datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')
        with open('log.txt', 'r+') as f:
            data = f.read()
            f.seek(0)
            f.write(now)
            f.truncate()
        root.destroy()

    # Retrieves all notifications from the notifications.txt file, and return them as a list.Each notification is written
    # on one line, and is a dictionary. The returned list have multiple dictionaires (unless there is only one notification)
    def get_all_notifications():
        notifications = []
        with open('notifications.txt',"r") as f:
            for line in f:
                notifications.append(json.loads(line))
        f.close()
        return notifications

    # Find and identifies a given notification by its given key:value pair in a big list where each notification is a dictionairy.
    # For example: ('hard topic','Name',list_of_notifications) will search all dictionaries
    # inside the list for with a key that have that name.
    def get_notification_by_key_value(target_value,key_value,notifications):
        print(str(target_value) + " " + str(key_value))
        for notification in notifications:
            for key, value in notification.items():
                if ((str(key) == str(target_value))and ( str(value) == str(key_value))):
                    return notification
        
            
    # Writes the notification to file, appending it to other, existing notifications (if any).
    def add_notification_to_file(dictionary_notification):
        with open('notifications.txt',"a") as f:
            f.write(json.dumps(dictionary_notification, sort_keys = True))
            f.write("\n")
        f.close()

    # Check if given key:value pair exist in a given dictionary, and return true if it does.
    def check_if_notification_data_exist(target_key,target_value,notification):
        if notification[target_key] == target_value:
            return True
        else:
            return False

    # TODO: INSERT COMMENT
    def set_notification_key_value(key, identifying_name, value):
        notifications = get_all_notifications()
        target_value = 'Name'
        target_notification = get_notification_by_key_value(target_value,identifying_name,notifications)
        old_value = target_notification[key]
        for notification in notifications:
            if notification['Name']== identifying_name:
                notifications.remove(notification)
                break
            else:
                pass
        notifications.append(target_notification)
        temp = open('notifications.txt', 'w').close()
        with open('notifications.txt',"a") as f:
            for popup in notifications:
                f.write(json.dumps(popup, sort_keys = True))
                f.write("\n")
        f.close()


if __name__=='__main__':
    root = tkinter.Tk()
    FileHandler(root).pack(side="top", fill="both", expand=True)
    menubar = Menu(root)
    root.mainloop()
