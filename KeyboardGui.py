from tkinter import *
from PIL import Image, ImageTk
from Keyboard import Keyboard, icon_path

class KeyboardGui(Tk):

    def __init__(self, parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.value = ""
        self.k = Keyboard()
        self.initialize()

    def initialize(self):        
        self.k.load_language('ru')        
        
        self.top = Toplevel(self)
        self.top.geometry('0x0+10000+10000') # make it not visible
        self.top.protocol('WM_DELETE_WINDOW', self.destroy) # close root window if toplevel is closed
        
        self.top.bind("<FocusOut>", self.on_focus_out)
        self.top.bind("<Visibility>", self.visibility)
        self.top.bind('<Motion>', func=self.motion)

        self.geometry('{0}x{1}+{2}+{3}'.format(self.k.width, self.k.height, self.k.location_x, self.k.location_y))
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.frame = None
        self.reload_keyboard()

    def reload_keyboard(self):
        if not self.frame is None:
            self.frame.destroy()        
        self.frame=Frame(self,bg = "white",width=self.k.width, height=self.k.height)
        self.frame.grid(padx = 0, pady = 0)
        x=0
        y=0
        w=0
        h=self.k.entry_field['height']
        for row in self.k.entry_field['rows']:
            count = 0
            for el in row:
                if count == len(row)-1:
                    w=self.width(el["size"], x, True)
                else:
                    w=self.width(el["size"])                
                self.create_el(el,x, y, w, h)
                x+=w
                count+=1
            y+=h
            x=0        
        rows=None
        if not self.k.numbers:
            rows=self.k.input_block['LanguareBlock']["rows"]
            h=self.k.input_block['height']/len(rows)
        else:
            rows=self.k.input_block['NumbersKeyboard']["rows"]
            h=self.k.input_block['height']/len(rows)
        for row in rows:
            count = 0
            for el in row:
                if count == len(row)-1:
                    w=self.width(el["size"], x, True)
                else:
                    w=self.width(el["size"])                
                self.create_el(el,x, y, w, h)
                x+=w
                count+=1
            y+=h
            x=0
        h=self.k.general_buttons['height']
        for row in self.k.general_buttons['rows']:
            count = 0
            for el in row:
                if count == len(row)-1:
                    w=self.width(el["size"], x, True)
                else:
                    w=self.width(el["size"])                
                self.create_el(el,x, y, w, h)
                x+=w
                count+=1
            y+=h
            x=0

    def icon_btn(self, icon, x, y, w, h, command):
        image = Image.open(icon_path(icon))
        maxsize = (w-5, h-5)
        image.thumbnail(maxsize, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        button = Button(self.frame, image=photo, command=command)
        button.photo = photo
        button.place(x=x,y=y, width=w, height=h)

    def text_btn(self, text, x, y, w, h, command):
        button = Button(self.frame, text=text, command=command)
        button.place(x=x,y=y, width=w, height=h)

    def entry_field(self, x, y, w, h):
        entry = Entry(self.frame)
        entry.place(x=x,y=y, width=w, height=h)


    def create_el(self, el, x, y, w, h):        
        if el["control"]=="button":
            text=""
            icon=""
            button=None
            if el["type"] == "apply":
                if el["icon"]:
                    self.icon_btn(el["icon"], x, y, w, h, self.simplecommand)
                else:
                    self.text_btn(el["text"], x, y, w, h, self.simplecommand)
            elif el["type"] == "input":
                if not self.k.uppercase:
                    self.text_btn(el["value1"], x, y, w, h, self.simplecommand)
                else:
                    self.text_btn(el["value2"], x, y, w, h, self.simplecommand)
            elif el["type"] == "turn":
                if el["iconTurnOn"] and el["iconTurnOff"]:
                    if el["turnTarget"]=="uppercase":
                        if not self.k.uppercase:
                            self.icon_btn(el["iconTurnOff"], x, y, w, h, self.switch_case)
                        else:
                            self.icon_btn(el["iconTurnOn"], x, y, w, h, self.switch_case)
                    elif el["turnTarget"]=="numbers":
                        if not self.k.numbers:
                            self.icon_btn(el["iconTurnOff"], x, y, w, h, self.switch_input_keyboard)
                        else:
                            self.icon_btn(el["iconTurnOn"], x, y, w, h, self.switch_input_keyboard)
                else:
                    if el["turnTarget"]=="uppercase":
                        if not self.k.uppercase:
                            self.text_btn(el["textTurnOff"], x, y, w, h, self.switch_case)
                        else:
                            self.text_btn(el["textTurnOn"], x, y, w, h, self.switch_case)
                    elif el["turnTarget"]=="numbers":
                        if not self.k.numbers:
                            self.text_btn(el["textTurnOff"], x, y, w, h, self.switch_input_keyboard)
                        else:
                            self.text_btn(el["textTurnOn"], x, y, w, h, self.switch_input_keyboard)
            elif el["type"] == "languare":
                if el["icon"]:
                    self.icon_btn(el["icon"], x, y, w, h, self.simplecommand)
                else:
                    self.text_btn(el["text"], x, y, w, h, self.simplecommand)
            elif el["type"] == "action":
                if el["icon"]:
                    self.icon_btn(el["icon"], x, y, w, h, self.simplecommand)
                else:
                    self.text_btn(el["text"], x, y, w, h, self.simplecommand)         
        elif el["control"]=="field":            
            self.entry_field(x, y, w, h) 

    # def clear(self):
    #     pass

    def width(self, size, used_width=0, last=False):
        w=0
        if last:
            w=self.k.width-used_width
        else:
            w=self.k.width/12*size
        return w

    def on_focus_out(self, event):
        w = self.focus_get()
        if w == None:
            self.value = "WORK"
            self.top.destroy()  
            self.destroy()
        else:
            w.bind("<FocusOut>", self.on_focus_out)

    def motion(self, event):
        x, y = event.x, event.y
        print(x,y)

    def visibility(self, event):
        pass

    def simplecommand(self):
        print("simplecommand")

    def switch_case(self):
        self.k.switch_case()
        self.reload_keyboard()

    def switch_input_keyboard(self):
        self.k.switch_input_keyboard()
        self.reload_keyboard()



