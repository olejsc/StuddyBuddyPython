'''from tkinter import *

class NotificationWindow(Button):
    def __init__(self, parent):
        root.geometry("200x200")
        Button.__init__(self, parent)
        self.config()
        self['text'] = 'Ok!'
        # Command to close the window (the destory method)
        self['command'] = parent.destroy
        self.pack(side=BOTTOM) #self.pack(side=BOTTOM)
        self.place(relx=0.5, rely=0.5, anchor=CENTER)


root = Tk()
NotificationWindow(root)
mainloop()
-----------------------------------------------------------------------
from tkinter import Tk, Label, Button

class popup:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="Nå er det tid for å lese!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

root = Tk()
my_gui = popup(root)
root.mainloop()'''


