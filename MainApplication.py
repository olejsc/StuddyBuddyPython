import tkinter
from tkinter import *
from threading import Thread
import pyglet
import datetime
import json

class FileHandler(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)
        menubar = Menu(root)
        Popup = popup()
        Clock = clock()
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

class popup():
    def __init__(self, master, subject,):
        self.master = master
        master.title("Notification")

        self.subject = subject # hvilket fag/tema som skal leses på, må hentes fra det som er lagret i fil
        self.font=tkinter.font.Font(family='Helvetica', size=26, weight='bold')
        self.label = Label(master, text="Time to read!" + "\n" + "The subject is: " + subject, font=self.font)
        self.label.pack()

        #self.subjectLabel = Label(master, text="" + subject, font=self.font, color=)
        self.close_button = Button(master, text="Got it!", command=master.destroy)
        self.close_button.pack()

    def real_playsound(self):
        sound = pyglet.media.load('alarm2wav.wav')
        sound.play()
        pyglet.app.run()

    def playsound(self):
        global player_thread
        player_thread = Thread(target=self.real_playsound)
        player_thread.start()

class clock():
    def __init__(self, variable,options):
        self.variable = IntVar(root)
        self.variable.set("Frequency")
        options = {1: 5, 2: 2, 3: 3}
        OptionMenu(root, variable, *options.keys()).pack()


    def shut_down():
        root.quit()

    button = Button( text="OK", command=shut_down)
    button.pack()


    def time_when_notified(choice):
        for key, value in options.items():  # Går gjennom elementene i dictionary
            if key == choice:  # Hvis key er lik valget brukeren velger
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Finner ut tiden nå.
                solve = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")  # Finner ut og legger til når personen vil bli varslet
                solve += timedelta(seconds=value)  # -''-
                notification_time = solve.strftime("%Y-%m-%d %H:%M:%S")  # Variabel for senere bruk
                return notification_time


    #  Sender varsel når nåtid er lik varseltid.


    def check_vol2():
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


def main(): 
    root = tkinter.Tk()
    menubar = Menu(root)
    FileHandler(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == '__main__':
    main()
