from Tkinter import *
root = Tk()

class rootwindow():
    def __init__(self, master):
        self.master = master

        self.button1 = Button(root, text="Hello World click to close")
        self.button1.pack()


