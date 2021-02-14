#!/usr/bin/python
# coding=utf-8
from KeyboardGui import KeyboardGui as keybord
app=None

def run(w=-1, h1=120, h2=-1, h3=-1, lx=-1, ly=-1, multiline=False):
    global app
    app = keybord(None, w, h1, h2, h3, lx, ly, multiline)    
    app.mainloop() #this will run until it closes
    print(app.value)    

def end():
    global app
    app.exit()
    exit()

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    run()  # то запускаем функцию main()
