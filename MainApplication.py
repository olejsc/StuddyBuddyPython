import tkinter as tk
from tkinter import *
from threading import Thread
import pyglet
import datetime
import time
import json

# ----------------------------------------------------
# GLOBALE VARIABLER
# ----------------------------------------------------


LARGE_FONT= ("Verdana", 12)
name_dict = {"SubjectCode": "", "Freqency": "", "Name" : "", "FrequencyLength" : "", 'LastNotification': "", "LastNotificationSeen": "False"}
notifications = get_all_notifications()
options = {1: 5, 2: 2, 3: 3}


# ----------------------------------------------------
# Fungerende, men ikke nødvendigvis i bruk av programmet-kode:
# ----------------------------------------------------

def callback(e):
    input_string = str(e.get())
    now = datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')
    name_dict["Name"] = input_string
    name_dict["Registered"]= now
    if get_notification_by_key_value('Name',input_string,notifications) == False:
        add_notification_to_file(name_dict)
    e.delete(0, END) #Denne linjen sletter skriven etter ADD-knappen trykkes
    
def quit_application (self):
    now = datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')
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
    print(str(target_value) + " " + str(key_value))
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

# ----------------------------------------------------
# ----------------------------------------------------



'''
def get_time_of_notification(notifications):
    opts = { Opt1: {'Time':{notification1},'Time2':{notification2}},Opt2:{'Time1':{Not1},'Time2':{not2}},Opt3:{'Time1':{Not1},'Time2':{not2}}}
    for notification in notifications:
        
        registered = notification['Registered']
        if notification['LastNotificationSeen'] == 'True' and notification['LastNotification'] != "":
            # Calculates next popup, Nåtid minus LastNotification
            # return a dict with { time_to_popup : {notification}
             popup_return_time_dict = calculate_when_next_popup_will_be(notification,options,1)
             insert_popup_into_correct_dict_position_in_opts

             
        elif notification['LastNotificationSeen'] == 'False' and notification['LastNotification'] != "":
            # Calculates next popup, Now minus LastNotification
            # If the time is there to show popup, return true or something :p If not, return a dict with { time_to_popup : {notification}} 
            if calculate_when_next_popup will be(notification,options,2) == True:
                 show_popup(notification)
                 
            # If not, return a dict with { time_to_popup : {notification}} 
            else:
                dict_with_calculated_time = calculate_when_next_popup will be(notification,options,2)

                
        elif notification['LastNotification'] == "":
            # Calculates next popup, Now minus Registered
            # return a dict with { time_to_popup : {notification}} 
            calculate_when_next_popup will be(notification,options,)
            insert_popup_into_correct_dict_position_in_opts
'''
            
def popupmsg(notification, ):
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text=msg, font=LARGE_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
        



'''def __init__(self, master, subject,):
    self.master = master
    master.title("Notification")

    self.subject = subject # hvilket fag/tema som skal leses på, må hentes fra det som er lagret i fil
    self.font=tkinter.font.Font(family='Helvetica', size=26, weight='bold')
    self.label = Label(master, text="Time to read!" + "\n" + "The subject is: " + subject, font=self.font)
    self.label.pack()

    #self.subjectLabel = Label(master, text="" + subject, font=self.font, color=)
    self.close_button = Button(master, text="Got it!", command=master.destroy)
    self.close_button.pack()
'''

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


def time_when_notified(notification,options,requested_logic):
    for key, value in notification.items():  # Går gjennom elementene i dictionary
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Finner ut tiden nå.
            solve = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")  # Finner ut og legger til når personen vil bli varslet
            solve += timedelta(seconds=value)  # -''-
            notification_time = solve.strftime("%Y-%m-%d %H:%M:%S")  # Variabel for senere bruk
            return notification_time


#  Sender varsel når nåtid er lik varseltid.


def check_vol2(self):
    last_notification = time_when_notified(variable.get())  # Lager variabel med angitt varseltid. Tid i framtiden.
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datetime_young = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")  # Formatvalg
    datetime_older = datetime.strptime(last_notification, "%Y-%m-%d %H:%M:%S")  # Formatvalg
    time_since_last = datetime_older - datetime_young
    difference = (time_since_last.total_seconds() / 3600)
    while True:
        if difference == 0:
            break
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datetime_young = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")  # Formatvalg
        time_since_last = datetime_older - datetime_young
        difference = (time_since_last.total_seconds()/3600)
    print("Du skal få varsel nå")  # Kjør notifikasjonskode


# ----------------------------------------------------
# ----------------------------------------------------
# FUNGERENDE PROGRAM UNDER:
# ----------------------------------------------------
# ----------------------------------------------------

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=lambda: quit_application(self))
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        frame = Add_notification(container, self)

        self.frames[Add_notification] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        self.root = tk.Tk()
        self.label = tk.Label(text="")
        self.label.pack()

        self.show_frame(Add_notification)
        self.update_clock()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.root.after(1000, self.update_clock)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()



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
        label = tk.Label(self, text=("""Add Serious hard subjects to learn here"""), font=LARGE_FONT, bg = "WHITE")
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



def main(): 
    app = MainApplication()
    app.mainloop()

if __name__ == '__main__':
    main()
