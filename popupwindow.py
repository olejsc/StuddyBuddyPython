import ctypes  # An included library with Python install.

def PopUpBox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)
PopUpBox('Your title', 'Your text', 1)
