from threading import Thread
import pyglet
def real_playsound():
    sound = pyglet.media.load('alarm2wav.wav')
    sound.play()
    pyglet.app.run()

def playsound():
    global player_thread
    player_thread = Thread(target=real_playsound)
    player_thread.start()

playsound()