import pyglet

window = pyglet.window.Window

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=200, y=200,
                          anchor_x='center', anchor_y='center')

def on_draw():
    window.clear()
    label.draw()

pyglet.app.run()