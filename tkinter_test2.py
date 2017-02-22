from tkinter import Tk, Label, Button
import tkinter.font
from threading import Thread
import pyglet

class popup():
    def __init__(self, master, subject, font):
        self.master = master
        master.title("Notification")

        self.subject = subject # hvilket fag/tema som skal leses på, må hentes fra det som er lagret i fil
        self.font=font
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

root = Tk()
helv36=tkinter.font.Font(family='Helvetica', size=26, weight='bold')
notification_window = popup(root, "ITGK kapittel 1", helv36)
notification_window.playsound()
root.mainloop()
