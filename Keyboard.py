import os
from lxml import etree as ET

class Keyboard(object):
    """docstring for ClassName"""
    def __init__(self):
        super(Keyboard, self).__init__()
        self.languages_path = os.path.join(os.getcwd(), "languages")  
        self.width=0
        self.height=0
        self.location_x =0
        self.location_y=0
        self.language=""
        self.shift = False
        self.numbers_keyboard = False
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
                result["icon"] = el.get("icon")
                result["size"] = el.get("size")
            elif el.get("type") == "input":
                result["type"] = "input"
                result["value1"] = el.get("value1")
                result["value2"] = el.get("value2")
                result["size"] = el.get("size")
            elif el.get("type") == "turn":
                result["type"] = "turn"
                result["name"] = el.get("name")
                iconTurnOn = el.get("iconTurnOn")
                iconTurnOff = el.get("iconTurnOff")
                if iconTurnOn and iconTurnOff:
                    result["textTurnOn"] = iconTurnOn
                    result["textTurnOff"] = iconTurnOff
                else:
                    result["iconTurnOn"] = el.get("iconTurnOn")
                    result["iconTurnOff"] = el.get("iconTurnOff")
                result["turnTarget"] = el.get("turnTarget")                
                result["size"] = el.get("size")
            elif el.get("type") == "languare":
                result["type"] = "languare"
                result["name"] = el.get("name")                
                result["size"] = el.get("size")
            elif el.get("type") == "action":
                result["type"] = "action"
                result["name"] = el.get("name")                
                result["action"] = el.get("action")   
                result["size"] = el.get("size")
        elif el.tag == "field":
            result["control"] = "field"
            if el.get("type") == "line":
                result["type"] = "line"
                result["size"] = el.get("size")
            elif el.get("type") == "multiline":                
                result["type"] = "multiline"
                result["size"] = el.get("size")
        return result

    def set_shift(self, value):
        self.shift = value

    def set_numbers_keyboard(self, value):
        self.numbers_keyboard = value

    def set_languare(self, value):
        self.languare = value