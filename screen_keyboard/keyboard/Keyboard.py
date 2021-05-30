import os
import sys
from lxml import etree as ET

def set_or_default(d, value, default):
    if value in d:
        return d[value]
    else:
        return default

def app_path():
    return os.path.abspath(os.path.dirname(sys.argv[0]))

class Keyboard(object):
    """docstring for ClassName"""
    def __init__(self, settings):
        super(Keyboard, self).__init__()

        self.height=0
        self.settings = settings

        self.multiline = False
        
        self.attachments_path = set_or_default(self.settings, "icon_path", os.path.join(app_path(), "attachments")) 
        self.languages_path = set_or_default(self.settings, "languages_path", os.path.join(app_path(), "languages"))

        self.b_style = {
        "b_foreground_!active" : set_or_default(self.settings, "b_foreground_!active", "#ffffff"),
        "b_foreground_pressed": set_or_default(self.settings, "b_foreground_pressed", "#ffffff"),
        "b_foreground_active": set_or_default(self.settings, "b_foreground_active", "#ffffff"),
        "b_background_!active": set_or_default(self.settings, "b_background_!active", "#232526"),
        "b_background_pressed": set_or_default(self.settings, "b_background_pressed", "#484a4b"),
        "b_background_active": set_or_default(self.settings, "b_background_active", "#484a4b"),
        }

        self.b_customize = set_or_default(self.settings, "b_customize", True)

        self.uppercase = False
        self.numbers = False
        
        self.entry_field = {}
        self.input_block = {}
        self.general_buttons = {}
        self.language=""
        self.languages = self.get_languages()
        if self.languages:
           self.language = self.languages[0]
           self.load_language()

    def get_languages(self):
        files = []              
        for file in os.listdir(self.languages_path):
            if file.endswith(".xml"):
                files.append(file.replace(".xml", ""))
        return files

    def load_language(self):
        file = os.path.join(self.languages_path, "{0}.xml".format(self.language))
        doc = ET.parse(file)
        root = doc.getroot()
        self.width=set_or_default(self.settings, "w", int(root.get("width")))
        self.location_x = set_or_default(self.settings, "lx", int(root.get("locationX"))) 
        self.location_y = set_or_default(self.settings, "ly", int(root.get("locationY"))) 
        font = root.find("Font")
        self.font=set_or_default(self.settings, "font", font.get("name")) 
        font_size = set_or_default(self.settings, "font_size", [])
        self.font_size = {
           "normal" : set_or_default(font_size, "normal", int(font.get("normal"))),
           "small" : set_or_default(font_size, "small", int(font.get("small"))),
           "large" : set_or_default(font_size, "large", int(font.get("large"))),
        } 

        self.entry_field = self.get_block(root.find("EntryField"))
        self.input_block = self.get_block(root.find("InputBlock"))
        self.general_buttons = self.get_block(root.find("GeneralButtons"))
        self.entry_field["height"] = set_or_default(self.settings, "h1", self.entry_field["height"])  
        self.input_block["height"] = set_or_default(self.settings, "h2", self.input_block["height"])  
        self.general_buttons["height"] = set_or_default(self.settings, "h3", self.general_buttons["height"]) 
        self.height += self.entry_field["height"]
        self.height += self.input_block["height"]
        self.height += self.general_buttons["height"]

    def get_block(self, block):
        result = {}
        if block.tag == "InputBlock":
            result["height"] = int(block.get("height"))
            result["LanguareBlock"] = self.get_block(block.find("LanguareBlock"))
            result["NumbersKeyboard"] = self.get_block(block.find("NumbersKeyboard"))
        elif block.tag == "LanguareBlock" or block.tag == "NumbersKeyboard":
            result["rows"]=self.get_rows(block)
        else:
            result["height"] = int(block.get("height"))
            result["rows"]=self.get_rows(block)
        return result

    def get_rows(self, root):
        result = []
        for row in root.iter("row"):
            result.append(self.get_row(row))
        return result

    def get_row(self, row):
        result = []
        for el in row.iter():
            if not len(el):
                result.append(self.get_el(el))
        return result

    def get_el(self, el):
        result={}
        if el.tag == "button":
            result["control"] = "button"
            if el.get("type") == "apply":                
                result["type"] = "apply"
                result["text"] = el.get("text")
                result["icon"] = self.file_or_empty(el.get("icon"))
                result["size"] = float(el.get("size"))
                result["style"] = self.set_btn_style(el)
            elif el.get("type") == "input":
                result["type"] = "input"
                if el.get("value"):
                    result["value1"] = el.get("value")
                    result["value2"] = el.get("value")
                else:
                    result["value1"] = el.get("value1")
                    result["value2"] = el.get("value2")
                result["size"] = float(el.get("size"))
                result["style"] = self.set_btn_style(el)
            elif el.get("type") == "turn":
                result["type"] = "turn"
                result["name"] = el.get("name")
                result["iconTurnOn"] = self.file_or_empty(el.get("iconTurnOn"))
                result["iconTurnOff"] = self.file_or_empty(el.get("iconTurnOff"))
                result["textTurnOn"] = el.get("textTurnOn")
                result["textTurnOff"] = el.get("textTurnOff")
                    
                result["turnTarget"] = el.get("turnTarget")                
                result["size"] = float(el.get("size"))
                result["style"] = self.set_btn_style(el)
            elif el.get("type") == "languare":
                result["type"] = "languare"
                result["text"] = el.get("text")
                result["icon"] = self.file_or_empty(el.get("icon"))
                result["name"] = el.get("name")                
                result["size"] = float(el.get("size"))
                result["style"] = self.set_btn_style(el)
            elif el.get("type") == "action":
                result["type"] = "action"
                result["name"] = el.get("name")  
                result["text"] = el.get("text")
                result["icon"] = self.file_or_empty(el.get("icon"))              
                result["action"] = el.get("action")   
                result["size"] = float(el.get("size"))
                result["style"] = self.set_btn_style(el)
        elif el.tag == "field":
            result["control"] = "field"            
            result["type"] = self.set_multiline(el)
            result["size"] = float(el.get("size"))
            result["font"] = self.set_entry_font(el)

        return result

    def set_entry_font(self, el):
        font_size = el.get("font-size")
        if not font_size in ["Small", "Normal", "Large"]:
            font_size = "Normal"
        style = "EntryFont{0}".format(font_size)
        return style

    def set_btn_style(self, el):
        font_size = el.get("font-size")
        align = el.get("align")
        if not font_size in ["Small", "Normal", "Large"]:
            font_size = "Normal"
        if not align in ["Top", "Center", "Bottom"]:
            align = "Center"
        style = "ScreenButton{0}{1}".format(font_size, align)
        return style

    def set_multiline(self, el):
        line_type = "line"
        multiline = False
        val = el.get("type")
        if val in ["line", "multiline"]:
            if val == "multiline":
                multiline = True
        multiline =  set_or_default(self.settings, "multiline", multiline)
        if multiline:
            self.multiline = True
            line_type = "multiline"
        else:
            self.multiline = False
            line_type = "line"
        return line_type




    def switch_case(self):
        if self.uppercase:
            self.uppercase = False
        else:
            self.uppercase = True

    def switch_input_keyboard(self):
        if self.numbers:
            self.numbers = False
            self.uppercase = False
        else:
            self.numbers = True
            self.uppercase = False

    def switch_language(self):
        if len(self.languages)>1:
            i = self.languages.index(self.language)
            if i+1 == len(self.languages):
                self.language = self.languages[0]
            else:
                self.language = self.languages[i+1]
        self.uppercase = False
        self.numbers = False
        self.load_language()

    def get_entry_field_rows(self):
        return self.entry_field['rows']

    def get_input_block_rows(self):
        rows = None
        if not self.numbers:
            rows=self.input_block['LanguareBlock']["rows"]
        else:
            rows=self.input_block['NumbersKeyboard']["rows"]
        return rows

    def get_general_buttons_rows(self):
        return self.general_buttons['rows']

    def switch_languare(self, value):
        self.languare = value

    def get_entry_field_height(self):
        return self.entry_field['height']

    def get_input_block_height(self):
        h = 0
        if not self.numbers:
            h=self.input_block['height']
        else:
            h=self.input_block['height']
        return h

    def get_general_buttons_height(self):
        return self.general_buttons['height']

    def get_entry_field_y(self):
        return 0

    def get_input_block_y(self):
        return self.get_entry_field_height()

    def get_general_buttons_y(self):
        return self.get_entry_field_height()+self.get_input_block_height()

    def icon_path(self, name):
        file = os.path.join(self.attachments_path, name)  
        return file

    def file_or_empty(self, file): 
        if os.path.isfile(self.icon_path(file)):
            return file
        else:
            return ""