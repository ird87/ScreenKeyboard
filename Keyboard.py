import os
from lxml import etree as ET

def icon_path(name):
    file = os.path.join(os.getcwd(), "attachments", name)  
    return file

def file_or_empty(file): 
    if os.path.isfile(icon_path(file)):
        return file
    else:
        return ""

class Keyboard(object):
    """docstring for ClassName"""
    def __init__(self, w, h1, h2, h3, lx, ly, multiline):
        super(Keyboard, self).__init__()
        self.languages_path = os.path.join(os.getcwd(), "languages")  
        self.width=w
        self.height=0
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.location_x = lx
        self.location_y = ly
        self.uppercase = False
        self.numbers = False
        self.multiline = multiline
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
        if self.width ==-1:
            self.width = int(root.get("width"))
        if self.location_x ==-1: 
            self.location_x = int(root.get("locationX"))
        if self.location_y ==-1:
            self.location_y = int(root.get("locationY"))
        self.entry_field = self.get_block(root.find("EntryField"))
        self.input_block = self.get_block(root.find("InputBlock"))
        self.general_buttons = self.get_block(root.find("GeneralButtons"))
        if self.h1 != -1:
            self.entry_field["height"] = self.h1
        if self.h2 != -1:
            self.input_block["height"] = self.h2
        if self.h3 != -1:
            self.general_buttons["height"] = self.h3
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
                result["icon"] = file_or_empty(el.get("icon"))
                result["size"] = float(el.get("size"))
            elif el.get("type") == "input":
                result["type"] = "input"
                if el.get("value"):
                    result["value1"] = el.get("value")
                    result["value2"] = el.get("value")
                else:
                    result["value1"] = el.get("value1")
                    result["value2"] = el.get("value2")
                result["size"] = float(el.get("size"))
            elif el.get("type") == "turn":
                result["type"] = "turn"
                result["name"] = el.get("name")
                result["iconTurnOn"] = file_or_empty(el.get("iconTurnOn"))
                result["iconTurnOff"] = file_or_empty(el.get("iconTurnOff"))
                result["textTurnOn"] = el.get("textTurnOn")
                result["textTurnOff"] = el.get("textTurnOff")
                    
                result["turnTarget"] = el.get("turnTarget")                
                result["size"] = float(el.get("size"))
            elif el.get("type") == "languare":
                result["type"] = "languare"
                result["text"] = el.get("text")
                result["icon"] = file_or_empty(el.get("icon"))
                result["name"] = el.get("name")                
                result["size"] = float(el.get("size"))
            elif el.get("type") == "action":
                result["type"] = "action"
                result["name"] = el.get("name")  
                result["text"] = el.get("text")
                result["icon"] = file_or_empty(el.get("icon"))              
                result["action"] = el.get("action")   
                result["size"] = float(el.get("size"))
        elif el.tag == "field":
            result["control"] = "field"
            if not self.multiline:
                if el.get("type") == "line":
                    self.multiline = False
                    result["type"] = "line"
                    result["size"] = float(el.get("size"))
                elif el.get("type") == "multiline":                
                    self.multiline = True
                    result["type"] = "multiline"
                    result["size"] = float(el.get("size"))
            else:
                result["type"] = "multiline"
                result["size"] = float(el.get("size"))
        return result

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

