from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from PIL import Image, ImageTk
from .Keyboard import Keyboard, set_or_default

class KeyboardGui(Tk):

    def __init__(self, parent, settings):
        Tk.__init__(self,parent)
        self.parent = parent
        self.value = set_or_default(settings, "text", "")
        self.password = set_or_default(settings, "password", False)
        self.result = False
        self.k = Keyboard(settings)
        if not self.k.language:
            return
        self.initialize()

    def initialize(self):        
        self.top = Toplevel(self)
        self.top.geometry('0x0+10000+10000') 
        self.top.protocol('WM_DELETE_WINDOW', self.destroy) 
        
        self.top.bind("<FocusOut>", self.focus_out)

        self.geometry('{0}x{1}+{2}+{3}'.format(self.k.width, self.k.height, self.k.location_x, self.k.location_y))
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.entry_field_base_frame = None
        self.input_block_base_frame = None
        self.general_buttons_base_frame = None
        self.entry_field_base_frame = self.reload_frame(self, self.entry_field_base_frame, self.k.get_entry_field_height())
        self.input_block_base_frame = self.reload_frame(self, self.input_block_base_frame, self.k.get_input_block_height())
        self.general_buttons_base_frame = self.reload_frame(self, self.general_buttons_base_frame, self.k.get_general_buttons_height())
        self.entry_field_frame = None
        self.input_block_frame = None
        self.general_buttons_frame = None
        self.reload_keyboard()

    def reload_keyboard(self):
        self.reload_styles()
        self.reload_entry_field()
        self.reload_input_block()
        self.reload_general_buttons()

    def set_colors_for_style(self, style):
        s = ttk.Style()
        s_map =s.map 
        if self.k.b_customize:        
            s_map = s.map("{}.TButton".format(style),
               foreground=[('!active', self.k.b_style["b_foreground_!active"]),('pressed', self.k.b_style["b_foreground_pressed"]), ('active', self.k.b_style["b_foreground_active"])],
                background=[ ('!active',self.k.b_style["b_background_!active"]),('pressed', self.k.b_style["b_background_pressed"]), ('active', self.k.b_style["b_background_active"])]
                )
        return s_map

    def reload_styles(self):

        # Для кнопок с иконками

        style_standart= ttk.Style()
        style_standart.map = self.set_colors_for_style("ScreenButton")

        # Для мальнького шрифта

        style_small_top= ttk.Style()
        style_small_center = ttk.Style()
        style_small_bottom = ttk.Style()

        style_small_top.map = self.set_colors_for_style("ScreenButtonSmallTop")
        style_small_top.map = self.set_colors_for_style("ScreenButtonSmallCenter")
        style_small_top.map = self.set_colors_for_style("ScreenButtonSmallBottom")
        style_small_center.configure('ScreenButtonSmallTopTButton', font=(self.k.font, self.k.font_size["small"]), anchor=N)
        style_small_center.configure('ScreenButtonSmallCenter.TButton', font=(self.k.font, self.k.font_size["small"]), anchor=CENTER)
        style_small_center.configure('ScreenButtonSmallBottom.TButton', font=(self.k.font, self.k.font_size["small"]), anchor=S)

        # Для нормального шрифта

        style_normal_top= ttk.Style()
        style_normal_center = ttk.Style()
        style_normal_bottom = ttk.Style()

        style_normal_top.map = self.set_colors_for_style("ScreenButtonNormalTop")
        style_normal_top.map = self.set_colors_for_style("ScreenButtonNormalCenter")
        style_normal_top.map = self.set_colors_for_style("ScreenButtonNormalBottom")

        style_normal_center.configure('ScreenButtonNormalTopTButton', font=(self.k.font, self.k.font_size["normal"]), anchor=N)
        style_normal_center.configure('ScreenButtonNormalCenter.TButton', font=(self.k.font, self.k.font_size["normal"]), anchor=CENTER)
        style_normal_center.configure('ScreenButtonNormalBottom.TButton', font=(self.k.font, self.k.font_size["normal"]), anchor=S)

        # Для большого шрифта

        style_large_top= ttk.Style()
        style_large_center = ttk.Style()
        style_large_bottom = ttk.Style()

        style_large_top.map = self.set_colors_for_style("ScreenButtonLargeTop")
        style_large_top.map = self.set_colors_for_style("ScreenButtonLargeCenter")
        style_large_top.map = self.set_colors_for_style("ScreenButtonLargeBottom")

        style_large_center.configure('ScreenButtonLargeTop.TButton', font=(self.k.font, self.k.font_size["large"]), anchor=N)
        style_large_center.configure('ScreenButtonLargeCenter.TButton', font=(self.k.font, self.k.font_size["large"]), anchor=CENTER)
        style_large_center.configure('ScreenButtonLargeBottom.TButton', font=(self.k.font, self.k.font_size["large"]), anchor=S)

    def reload_entry_field(self):
        frame_h = self.k.get_entry_field_height()        
        rows = self.k.get_entry_field_rows()
        row_h = frame_h / len(rows) 
        self.entry_field_frame = self.reload_frame(self.entry_field_base_frame, self.entry_field_frame, frame_h)
        self.create_rows(self.entry_field_frame, rows, row_h)
        self.entry.focus()

    def reload_input_block(self):
        frame_h = self.k.get_input_block_height()
        rows = self.k.get_input_block_rows()
        row_h = frame_h / len(rows) 
        self.input_block_frame = self.reload_frame(self.input_block_base_frame, self.input_block_frame, frame_h)
        self.create_rows(self.input_block_frame, rows, row_h)  
        self.entry.focus()      

    def reload_general_buttons(self):
        frame_h = self.k.get_general_buttons_height()
        rows = self.k.get_general_buttons_rows()
        row_h = frame_h / len(rows) 
        self.general_buttons_frame = self.reload_frame(self.general_buttons_base_frame, self.general_buttons_frame, frame_h)
        self.create_rows(self.general_buttons_frame, rows, row_h)
        self.entry.focus()

    def reload_frame(self, base_frame, frame, h):
        if not frame is None:
            frame.destroy()
        frame=Frame(base_frame ,bg = "white",width=self.k.width, height=h)
        frame.grid(padx = 0, pady = 0)
        return frame

    def create_rows(self, frame, rows, h):
        y=0
        for row in rows:            
            self.create_row(frame, row, h, y)
            y+=h

    def create_row(self, frame, row, h, y):
        count = 0
        x=0
        for el in row:
            if count == len(row)-1:
                w=self.width(el["size"], x, True)
            else:
                w=self.width(el["size"])                
            self.create_el(frame, el, x, y, w, h)
            x+=w
            count+=1

    def create_el(self, frame, el, x, y, w, h):        
        if el["control"]=="button":
            text=""
            icon=""
            button=None
            if el["type"] == "apply":
                if el["icon"]:
                    self.create_btn_with_icon(frame, el["icon"], x, y, w, h, self.apply)
                else:
                    self.create_btn_with_text(frame, el["text"], x, y, w, h, self.apply, el["style"])
            elif el["type"] == "input":
                if not self.k.uppercase:
                    self.create_btn_with_text(frame, el["value1"], x, y, w, h, lambda k=el["value1"]: self.input(k), el["style"])
                else:
                    self.create_btn_with_text(frame, el["value2"], x, y, w, h, lambda k=el["value2"]: self.input(k), el["style"])
            elif el["type"] == "turn":
                if el["iconTurnOn"] and el["iconTurnOff"]:
                    if el["turnTarget"]=="uppercase":
                        if not self.k.uppercase:
                            self.create_btn_with_icon(frame, el["iconTurnOff"], x, y, w, h, self.switch_case)
                        else:
                            self.create_btn_with_icon(frame, el["iconTurnOn"], x, y, w, h, self.switch_case)
                    elif el["turnTarget"]=="numbers":
                        if not self.k.numbers:
                            self.create_btn_with_icon(frame, el["iconTurnOff"], x, y, w, h, self.switch_input_keyboard)
                        else:
                            self.create_btn_with_icon(frame, el["iconTurnOn"], x, y, w, h, self.switch_input_keyboard)
                else:
                    if el["turnTarget"]=="uppercase":
                        if not self.k.uppercase:
                            self.create_btn_with_text(frame, el["textTurnOff"], x, y, w, h, self.switch_case, el["style"])
                        else:
                            self.create_btn_with_text(frame, el["textTurnOn"], x, y, w, h, self.switch_case, el["style"])
                    elif el["turnTarget"]=="numbers":
                        if not self.k.numbers:
                            self.create_btn_with_text(frame, el["textTurnOff"], x, y, w, h, self.switch_input_keyboard, el["style"])
                        else:
                            self.create_btn_with_text(frame, el["textTurnOn"], x, y, w, h, self.switch_input_keyboard, el["style"])
            elif el["type"] == "languare":
                if el["icon"]:
                    self.create_btn_with_icon(frame, el["icon"], x, y, w, h, self.switch_language)
                else:
                    self.create_btn_with_text(frame, self.k.language, x, y, w, h, self.switch_language, el["style"])
            elif el["type"] == "action":
                if el["icon"]:
                    self.create_btn_with_icon(frame, el["icon"], x, y, w, h, lambda a=el["action"]: self.action(a))
                else:
                    self.create_btn_with_text(frame, el["text"], x, y, w, h, lambda a=el["action"]: self.action(a),el["style"])         
        elif el["control"]=="field":
            if el["type"]=="line":
                self.create_entry_field(frame, x, y, w, h) 
            elif el["type"]=="multiline":
                self.create_text_field(frame, x, y, w, h) 

    def create_btn_with_icon(self, frame, icon, x, y, w, h, command):
        image = Image.open(self.k.icon_path(icon))
        maxsize = (w*0.9, h*0.7)
        image.thumbnail(maxsize, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        button = ttk.Button(frame, image=photo, command=command, style="ScreenButton.TButton")
        button.photo = photo
        button.place(x=x,y=y, width=w, height=h)

    def create_btn_with_text(self, frame, text, x, y, w, h, command, style):       
        button = ttk.Button(frame, text=text, command=command, style="{0}.TButton".format(style))
        button.place(x=x,y=y, width=w, height=h)

    def create_entry_field(self, frame, x, y, w, h):
        self.entry = None
        if self.password:
            self.entry = Entry(frame, show="*")
        else:
            self.entry = Entry(frame)
        self.entry.place(x=x+1,y=y+1, width=w-2, height=h-2)
        self.entry.insert(END, self.value)
        self.entry.focus()

    def create_text_field(self, frame, x, y, w, h):
        self.entry = ScrolledText (frame)
        self.entry.place(x=x+1,y=y+1, width=w-2, height=h-2)
        self.entry.insert(END, self.value)
        self.entry.focus()

    def width(self, size, used_width=0, last=False):
        w=0
        if last:
            w=self.k.width-used_width
        else:
            w=self.k.width/12*size
        return w

    def focus_out(self, event):
        w = self.focus_get()
        if w == None:
            self.exit()
        else:
            w.bind("<FocusOut>", self.focus_out)

    def exit(self):
        self.get_text()
        self.top.destroy()  
        self.destroy()

    def action(self, a):
        if a=="backspace":
            if self.k.multiline:
                try:
                    self.entry.delete("sel.first", "sel.last")
                except:                    
                    insert = self.entry.index("insert")
                    line, char = insert.split(".")
                    delindex = "{0}.{1}".format(line, int(char)-1)
                    self.entry.delete(delindex) 
            else:
                try:
                    self.entry.delete("sel.first", "sel.last")
                except:
                    insert = self.entry.index("insert")
                    self.entry.delete(insert-1)   
        elif a=="enter":
            if self.k.multiline:
                try:
                    self.entry.delete("sel.first", "sel.last")
                except:
                    pass
                self.entry.insert(INSERT, "\n")

    def input(self, k):
        try:
            self.entry.delete("sel.first", "sel.last")
        except:
            pass
        self.entry.insert(INSERT, k)
        self.entry.focus()

    def switch_case(self):
        self.k.switch_case()
        self.reload_input_block()
        self.reload_general_buttons()

    def switch_input_keyboard(self):
        self.k.switch_input_keyboard()
        self.reload_input_block()
        self.reload_general_buttons()

    def switch_language(self):
        self.k.switch_language()
        self.reload_input_block()
        self.reload_general_buttons()

    def apply(self):
        self.get_text()
        self.result = True
        self.top.destroy()  
        self.destroy()

    def get_text(self):
        if self.k.multiline:
            self.value  = self.entry.get('1.0', 'end-1c')
        else:
            self.value = self.entry.get()
