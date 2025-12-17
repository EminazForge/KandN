import json
import os
import random
from core import bonus as Bonus

# --- Configuration ---
JSON_FILE_NAME = "Bases.json"

def _candidate_paths(filename: str):
    here = os.path.dirname(__file__)              # .../core/items
    root = os.path.dirname(os.path.dirname(here)) # project root
    return [
        os.path.join(root, "data", filename),   # preferred location
        os.path.join(root, filename),            # legacy root location
    ]

class BaseTypeLoader():
    
    def __init__(self):
        
        self.baseTypeList = self.load_data()
    
    def load_data(self, file_path: str | None = None):
        """
        Loads affix data from a JSON file and returns it as a Python dictionary.
        """
        # Determine candidate paths (data/ then root/) unless an explicit path is provided
        paths = [file_path] if file_path else _candidate_paths(JSON_FILE_NAME)
        last_err = None
        for p in paths:
            try:
                if p and os.path.exists(p):
                    with open(p, 'r') as f:
                        data = json.load(f)
                    return data
            except json.JSONDecodeError as e:
                last_err = e
                break
            except OSError as e:
                last_err = e
                continue
        if last_err:
            print(f"Error loading base data: {last_err}")
        else:
            print(f"Warning: Base data file not found in any expected location: {paths}")
        return {}
        
    def get_baseType_by_name(self, baseTypeList, name):
        """
        Retrieves an affix object from the restructured data by its vagueName.
        """
        return baseTypeList.get(name)
    
    def get_allowed_baseTypes(self, ilvl, exclude=[], gearSlot="random"):
        """
        Retrieves a list of all basetypes with the given ilvl.
        """
        baseTypes = []
        
        # prevent low level bases to drop (20 levels below ilvl)
        max_lvl = ilvl
        min_lvl = max(ilvl - 25, 0)
        
        # Apply restrictions
        for baseType in self.baseTypeList.values():
            if max_lvl >= baseType.get("lvl_req"):
                if min_lvl <= baseType.get("lvl_req"):
                    if baseType.get("name") not in exclude:
                        if gearSlot == "random":
                            baseTypes.append(baseType)
                        if baseType.get("slot") == gearSlot:
                            baseTypes.append(baseType)
    
        return baseTypes

    def create_random_baseType(self, ilvl, exclude=[], gearSlot="random"):

        js_baseTypes = self.get_allowed_baseTypes(ilvl, exclude, gearSlot)
        weights = [bt['weight'] for bt in js_baseTypes]
        
        js_baseType = random.choices(js_baseTypes, weights=weights)[0]
        
        baseType = BaseType(js_baseType, ilvl)
        return baseType
        
    
class BaseType():
    def __init__(self, json_baseType, ilvl):
        
        # from json
        self.slot = json_baseType["slot"] # string
        self.name = json_baseType["name"] 
        self.vagueName = json_baseType["vagueName"] 
        
        self.tags = json_baseType["tags"] # string array
        
        self.lvl_req = json_baseType["lvl_req"] # int
        self.str_req = json_baseType["str_req"] # int
        self.int_req = json_baseType["int_req"] # int
        self.dex_req = json_baseType["dex_req"] # int
        
        self.description0 = json_baseType.get("description") # string
        
        self.xStat = json_baseType.get("xStat") # string
        self.xType = json_baseType.get("xType") # int
        self.xValue0 = json_baseType.get("xValue") # int
        self.xValue = self.xValue0 # int

        self.yStat = json_baseType.get("yStat") # string
        self.yType = json_baseType.get("yType") # int
        self.yValue0 = json_baseType.get("yValue") # int
        self.yValue = self.yValue0 # int
       
        self.zStat = json_baseType.get("zStat") # string
        self.zType = json_baseType.get("zType") # int
        self.zValue0 = json_baseType.get("zValue") # int    
        self.zValue = self.zValue0 # int    
        
        # intrinsic
        self.ilvl = ilvl
        
        # affix modifiers
        self.total_additives = 0
        self.total_multiplier = 0
        
        self.update_boni()
        
        
    def update_boni(self):
        
        # apply modifications from affix modifiers
        self.xValue = round((self.xValue0 + self.total_additives) * (1 + self.total_multiplier/100))
        self.description = str(self.description0).replace("xValue", str(self.xValue))
        
        if self.yValue != None:
            self.yValue = round((self.yValue0 + self.total_additives) * (1 + self.total_multiplier/100))
            self.description = str(self.description).replace("yValue", str(self.yValue))
        
        if self.zValue != None:
            self.zValue = round((self.zValue0 + self.total_additives) * (1 + self.total_multiplier/100))
            self.description = str(self.description).replace("zValue", str(self.zValue)) 
        
        # create boni
        self.boni = []

        if self.xType == "additive":
            self.boni.append(Bonus.Bonus(self.xStat, self.xValue, 0)) 
        elif self.xType == "multiplicative":
            self.boni.append(Bonus.Bonus(self.xStat, 0 , self.xValue))
            
        if self.yStat != None:
            if self.yType == "additive":
                self.boni.append(Bonus.Bonus(self.yStat, self.yValue, 0)) 
            elif self.yType == "multiplicative":
                self.boni.append(Bonus.Bonus(self.yStat, 0 , self.yValue))
                
        if self.zStat != None:
            if self.zType == "additive":
                self.boni.append(Bonus.Bonus(self.zStat, self.zValue, 0)) 
            elif self.xType == "multiplicative":
                self.boni.append(Bonus.Bonus(self.zStat, 0 , self.zValue))   

        
        
    def modify_base_values(self, add_mod = 0, multi_mod = 0):
        
        self.total_additives += add_mod
        self.total_multiplier += multi_mod
        
        self.update_boni()
        
        
    def has_tag(self, tag):
        if tag in self.tags:
            return True
        
        return False
                   
    def __str__(self):
        return f"\nBaseType: {self.name} | VagueName: {self.vagueName} | Slot: {self.slot} \ntags: {self.tags} \n{self.xStat} | {self.xType} | {self.xValue} \n"
