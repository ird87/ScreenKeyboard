#!/usr/bin/python
# coding=utf-8
from KeyboardGui import KeyboardGui as keybord
app=None

def run(setting={
            # "w" : 1600, 
            # "h1" : -1, 
            # "h2" : -1, 
            # "h3" : -1, 
            "lx" : 1000, 
            "ly" : 400, 
            # "multiline" : False, 
            # "font" : 'Helvetica', 
            # "font_size" : 12, 
            # "icon_path" : os.path.join(os.path.dirname(os.path.realpath(__file__)), "attachments"),  
            # "languages_path" : os.path.join(os.path.dirname(os.path.realpath(__file__)), "languages"),
            # "b_foreground_!active":"#ffffff",
            # "b_foreground_pressed":"#ffffff",
            # "b_foreground_active":"#ffffff",
            # "b_background_!active":"#232526",
            # "b_background_pressed":"#484a4b",
            # "b_background_active":"#484a4b",
            }
        ):
    global app
    app = keybord(None, setting)    
    app.mainloop() #this will run until it closes
    print(app.value)    

def end():
    global app
    app.exit()
    exit()

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    run()  # то запускаем функцию main()
