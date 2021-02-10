from tkinter import *
from Keyboard import Keyboard
k = Keyboard()
k.load_language('ru.xml')

window = Tk()
window.title("Добро пожаловать в приложение PythonRu")
window.geometry('{0}x{1}+{2}+{3}'.format(k.width, k.height, k.location_x, k.location_y))
myEntry = Entry(window)
myEntry.place(x=0,y=0, width=440, height=30) # here
window.mainloop()