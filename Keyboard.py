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
    def __init__(self):
        super(Keyboard, self).__init__()
        self.languages_path = os.path.join(os.getcwd(), "languages")  
        self.width=0
        self.height=0
        self.location_x = 0
        self.location_y = 0
        self.language=""
        self.uppercase = False
        self.numbers = False
        self.entry_field = {}
        self.input_block = {}
        self.general_buttons = {}

    def get_languages(self):
        files = []              
        for file in os.listdir(self.languages_path):
            if file.endswith(".xml"):
                files.append(file)
        return files

    def load_language(self, language):
        file="{0}.xml".format(language)
        if file in self.get_languages():
            self.language = language
            file = os.path.join(self.languages_path, file)
            doc = ET.parse(file)
            root = doc.getroot()
            self.width = int(root.get("width"))
            self.location_x = int(root.get("locationX"))
            self.location_y = int(root.get("locationY"))
            self.entry_field = self.get_block(root.find("EntryField"))
            self.input_block = self.get_block(root.find("InputBlock"))
            self.general_buttons = self.get_block(root.find("GeneralButtons"))
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
            if el.get("type") == "line":
                result["type"] = "line"
                result["size"] = float(el.get("size"))
            elif el.get("type") == "multiline":                
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

    def switch_languare(self, value):
        self.languare = value