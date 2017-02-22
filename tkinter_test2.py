from tkinter import Tk, Label, Button
from threading import Thread
import pyglet

class popup():
    def __init__(self, master):
        self.master = master
        master.title("Notification")

        self.label = Label(master, text="Time to read!")
        self.label.pack()

        self.close_button = Button(master, text="Close", command=master.destroy)
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
notification_window = popup(root)
notification_window.playsound()
root.mainloop()
