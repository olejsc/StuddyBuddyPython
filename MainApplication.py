import tkinter as tk
from tkinter import *
from threading import Thread
import pyglet
import datetime
from datetime import *
import json




# ----------------------------------------------------
# Fungerende, men ikke nødvendigvis i bruk av programmet-kode:
# ----------------------------------------------------

def callback(e):
    input_string = str(e.get())
    now = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
    name_dict["Name"] = input_string
    name_dict["Registered"]= now
    name_dict["Frequency"] = "300000"
    if get_notification_by_key_value('Name',input_string,notifications) == False:
        add_notification_to_file(name_dict)
    e.delete(0, END) #Denne linjen sletter skriven etter ADD-knappen trykkes
    
def quit_application (self):
    now = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
    with open('log.txt', 'r+') as f:
        data = f.read()
        f.seek(0)
        f.write(now)
        f.truncate()
    self.destroy()

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
    for notification in notifications:
        for key, value in notification.items():
            if ((str(key) == str(target_value))and ( str(value) == str(key_value))):
                return notification
            else:
                pass
    return False

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
    target_value = 'Name'
    target_notification = get_notification_by_key_value(target_value,identifying_name,notifications)
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

# ----------------------------------------------------
# ----------------------------------------------------



def next_popup_time(notification,opts, target_key):
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
        not_dict[result] = notification
        if 'show_later' in opts.keys():
            print("Existing keys in show_later, adding:")
            print(result)
            opts['show_later'][result] = notification
        else:
            print(result)
            opts['show_later']= {result:notification}
        return opts


def get_time_of_notification(notifications):
    opts = {}
    for notification in notifications:
        if ((notification['LastNotificationSeen'] == 'True' or notification['LastNotificationSeen'] == 'False')
            and notification['LastNotification'] != ""):
            target_key = 'LastNotification'
            opts = next_popup_time(notification,opts, target_key)
        elif notification['LastNotification'] == "":
            target_key = 'Registered'
            opts = next_popup_time(notification,opts, target_key)
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




def shut_down(self):
    self.quit()


# ----------------------------------------------------
# ----------------------------------------------------
# FUNGERENDE PROGRAM UNDER:
# ----------------------------------------------------
# ----------------------------------------------------

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.geometry("400x400")
        print('Initialiserer MainApplication...')
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=lambda: quit_application(self))
        menubar.add_cascade(label="File", menu=filemenu)
        tk.Tk.config(self, menu=menubar)
        self.frames = {}
        
        for F in (Add_notification,):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        print('Initialiserer Add_notification screen...')
        frame = Add_notification(container, self)
        self.frames[Add_notification] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        opts = get_time_of_notification(notifications)
        notification_window = False
        for key, value in opts.items():
            if key == 'show_now':
                for key2, value2 in value.items():
                    noti = 'now'
                    now2 = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
                    notification_window = True
                    key_now = 'LastNotification'
                    set_notification_key_value(key_now, value2['Name'], now2)
                    topLevel(key2,value2,noti)
                    print('Showing popups now...')
            elif key == 'show_later':
                for key3, value3 in value.items():
                    if value3['LastNotificationSeen'] == 'True':
                        noti = 'delayed'
                        self.after(key_ms,topLevel(key3,value3,noti))
                        notification_window = True
                        key_later = 'LastNotification'
                        now3 = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
                        set_notification_key_value(key_later, value3['Name'], now3)
                    else:
                        pass
        if notification_window == True:
            playsound(self)
    
        self.show_frame(Add_notification)
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def real_playsound(self):
        sound = pyglet.media.load('alarm2wav.wav')
        sound.play()
        pyglet.app.run()

    def playsound(self):
        global player_thread
        player_thread = Thread(target=self.real_playsound)
        player_thread.start()



# ----------------------------------------------------
# GLOBALE VARIABLER
# ----------------------------------------------------


LARGE_FONT= ("Verdana", 12)
name_dict = {"SubjectCode": "", "Freqency": "", "Name" : "", "FrequencyLength" : "", 'LastNotification': "", "LastNotificationSeen": "False"}
notifications = get_all_notifications()
options = {1: 5, 2: 2, 3: 3}


class Add_notification(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        #Dette er Meldingen som vises
        label = tk.Label(self, text=("""Add subject here"""), font=LARGE_FONT, bg = "WHITE")
        label.pack(pady=10,padx=10)
        #Dette er feltet vi skriver inn i:
        e = Entry(self)
        e.pack()
        e.focus_set()

        b = Button(self, text="ADD", width=5, pady = 10, padx = 5, command=lambda: callback(e), font="Arial", )
        b.pack()

        #Dette var bare pynt
        #separator = Frame(height=10, bd=1, relief=SUNKEN)
        #separator.pack(fill=X, padx=5, pady=5)


def topLevel(frequency,subject, type_of_not):
    top=Toplevel()
    top.attributes("-topmost", True)
    top.title("Notification!")
    label1 = Label(top, text="Time to read!" + "\n" + str(subject['Name']), font=('Times', 14))
    label1.grid(row=0,column = 1, sticky = N)
    label2 = Label(top, text="Fag:" + "\n" + str(subject['SubjectCode']), font=('Times', 10))
    label2.grid(row=1,column = 1, sticky = N)
    close_button = Button(top, text="Got it!", command=lambda: quit_and_store(top, subject['Name'], 'True'))
    close_button.grid(row = 2,column = 1, sticky = N)
    '''label1 = Label(top, text="Registered date is: " + "\n" + str(subject['Registered']), font=('Times', 12))
    label1.grid(row=0,column = 0, sticky = N)
    label2 = Label(top, text="LastNotification is:" + "\n" +str(subject['LastNotification']), font=('Times', 12))
    label2.grid(row=0,column = 1, sticky = W)
    label3 = Label(top, text="LastNotificationSeen is:" + "\n" +str(subject['LastNotificationSeen']), font=('Times', 12))
    label3.grid(row=0,column = 2, sticky = W)
    label4 = Label(top, text="Result after time calculation " + "\n" +str(int(frequency)), font=('Times', 12))
    label4.grid(row=1,column = 0, sticky = W)
    label5 = Label(top, text="Notification type: " + "\n" + type_of_not, font=('Times', 12))
    label5.grid(row=1,column = 2, sticky = W)
    label6 = Label(top, text="Frequency in ms: " + "\n" + str(int(subject['Frequency'])), font=('Times', 12))
    label6.grid(row=1,column = 1, sticky = W)
    label7 = Label(top, text="Name is: " + "\n" + str(subject['Name']), font=('Times', 12))
    label7.grid(row=2,column = 0, sticky = W)
    close_button = Button(top, text="Got it!", command=lambda: quit_and_store(top, subject['Name'], 'True'))
    close_button.grid(row = 2,column = 1, sticky = N)'''


def quit_and_store(self, identifying_name, value):
    key = 'LastNotificationSeen'
    set_notification_key_value(key, identifying_name, value)
    self.destroy()


def main(): 
    app = MainApplication()
    app.mainloop()

if __name__ == '__main__':
    main()
