#!/usr/bin/python
# coding=utf-8
from KeyboardGui import KeyboardGui as keybord

def main():
    app = keybord(None)
    app.title("Добро пожаловать в приложение PythonRu")
    app.mainloop() #this will run until it closes
    print(app.value)


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
