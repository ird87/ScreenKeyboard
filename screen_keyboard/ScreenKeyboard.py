#!/usr/bin/python
# coding=utf-8
import argparse
import re
import os
import sys

try:
    from .keyboard import KeyboardGui as k
except: 
    from keyboard import KeyboardGui as k

app=None


def run(settings={
            # "text" : "Hello world"
            # "w" : 1600, 
            # "h1" : -1, 
            # "h2" : -1, 
            # "h3" : -1, 
            "lx" : 300, 
            "ly" : 300, 
            # "password" : False,
            # "b_customize":False, 
            # "multiline" : False, 
            # "font" : 'Helvetica', 
            # "font_size" : {'small': 10, 'normal': 12, 'large': 14}, 
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
    app = k.KeyboardGui(None, settings)    
    app.mainloop() #this will run until it closes
    os.environ["screen_keyboard_value"] = app.value
    os.environ["screen_keyboard_result"] = str(app.result)
    return {
    "value": app.value,
    "result": app.result
    }

def end():
    global app
    app.exit()
    exit()

def hex_type(arg_value, pat=re.compile(r'^#(?:[0-9a-fA-F]{1,2}){3}$')):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value

def fsize_type(arg_value):
    try:
        fsplit = arg_value.split(',')
        fsmall = int(fsplit[0])
        fnormal = int(fsplit[1])
        flarge = int(fsplit[2])
        return arg_value
    except:
        raise argparse.ArgumentTypeError

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    my_parser = argparse.ArgumentParser(prog='screen_keyboard',
                                    usage='%(prog)s [options] path')
    my_parser.add_argument("-t", action='store', type=str, required=False, help='current text, str')
    my_parser.add_argument("-p", action='store_true', required=False, help='password mode (not worked in multiline mode)')
    my_parser.add_argument("-w", action='store', type=int, required=False, help='width, int')
    my_parser.add_argument("-h1", action='store', type=int, required=False, help='EntryField height, str')
    my_parser.add_argument("-h2", action='store', type=int, required=False, help='InputBlock height, str')
    my_parser.add_argument("-h3", action='store', type=int, required=False, help='GeneralButtons height, str')
    my_parser.add_argument("-x", action='store', type=int, required=False, help='location x, int')
    my_parser.add_argument("-y", action='store', type=int, required=False, help='location y, int')
    my_parser.add_argument("-c", action='store_true', required=False, help='no customization mode')
    my_parser.add_argument("-m", action='store_true', required=False, help='multiline mode')
    my_parser.add_argument("-fname", action='store', type=str, required=False, help='font family name, str')
    my_parser.add_argument("-fsize", action='store', type=fsize_type, required=False, help='font size, str: "int, int, int" (small, normal, large)')
    my_parser.add_argument("-i", action='store', type=str, required=False, help='icon path, str')
    my_parser.add_argument("-l", action='store', type=str, required=False, help='language path, str')
    my_parser.add_argument("-bfu", action='store', type=hex_type, required=False, help='button foreground unactive color, str: "#xxxxxx"')
    my_parser.add_argument("-bfp", action='store', type=hex_type, required=False, help='button foreground pressed color, str: "#xxxxxx"')
    my_parser.add_argument("-bfa", action='store', type=hex_type, required=False, help='button foreground active color, str: "#xxxxxx"')
    my_parser.add_argument("-bbu", action='store', type=hex_type, required=False, help='button background unactive color, str: "#xxxxxx"')
    my_parser.add_argument("-bbp", action='store', type=hex_type, required=False, help='button background pressed color, str: "#xxxxxx"')
    my_parser.add_argument("-bba", action='store', type=hex_type, required=False, help='button background active color, str: "#xxxxxx"')

    args = my_parser.parse_args()

    settings={}

    if not args.t is None: settings["text"] = args.t
    if args.p: settings["password"] = True
    if not args.w is None: settings["w"] = args.w
    if not args.h1 is None: settings["h1"] = args.h1
    if not args.h2 is None: settings["h2"] = args.h2
    if not args.h3 is None: settings["h3"] = args.h3
    if not args.x is None: settings["lx"] = args.x
    if not args.y is None: settings["ly"] = args.y
    if args.c: settings["b_customize"] = True
    if args.m: settings["multiline"] = True
    if not args.fname is None: settings["font"] = args.fname
    if not args.fsize is None:
        fsplit = args.fsize.split(',') 
        settings["font_size"]= {"small" : int(fsplit[0]),"normal" : int(fsplit[1]),"large" : int(fsplit[2])}
    if not args.i is None: settings["icon_path"] = args.i
    if not args.l is None: settings["languages_path"] = args.l
    if not args.bfu is None: settings["b_foreground_!active"] = args.bfu
    if not args.bfp is None: settings["b_foreground_pressed"] = args.bfp
    if not args.bfa is None: settings["b_foreground_active"] = args.bfa
    if not args.bbu is None: settings["b_background_!active"] = args.bbu
    if not args.bbp is None: settings["b_background_pressed"] = args.bbp
    if not args.bba is None: settings["b_background_active"] = args.bba

    run(settings)  # то запускаем функцию main()
