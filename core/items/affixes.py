import json
import os
import random
import sys
from core import bonus as Bonus

# --- Configuration ---
JSON_FILE_NAME = "Affixes.json"

def _candidate_paths(filename: str):
    here = os.path.dirname(__file__)              # .../core/items
    root = os.path.dirname(os.path.dirname(here)) # project root
    return [
        os.path.join(root, "data", filename),   # preferred location
        os.path.join(root, filename),            # legacy root location
    ]

class AffixLoader():
    
    def __init__(self):
        
        self.affixList = self.load_data()
        self.used_affixes = []
    
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
            print(f"Error loading affix data: {last_err}")
        else:
            print(f"Warning: Affix data file not found in any expected location: {paths}")
        return {}
        
    def get_affix_by_name(self, affixList, name):
        """
        Retrieves an affix object from the restructured data by its vagueName.
        """
        return affixList.get(name)
    
    def get_random_affix(self, gear_slot):
        """
        Retrieves a random affix from the affix list
        """
        
        random_vague_name = random.choice(list(self.affixList.keys()))
        return self.get_affix_by_name(self.affixList, random_vague_name)
    
    def get_affixes_for_slot(self, affixType, gear_slot):
        """
        Retrieves a random prefix affix object from the restructured data.
        """
        affixes = []
        # Iterate over the values (the affix objects) in the top-level dictionary
        for affix_obj in self.affixList.values():
            # Check the 'type' attribute of each affix object
            if (affix_obj.get("type") == affixType) and (gear_slot in affix_obj.get("slots")):
                    affixes.append(affix_obj)
    
        return affixes
    
    def get_affixes(self, affixType):
        """
        Retrieves all affix objects from the restructured data.
        """
        affixes = []
        # Iterate over the values (the affix objects) in the top-level dictionary
        for affix_obj in self.affixList.values():
            # Check the 'type' attribute of each affix object
            if (affix_obj.get("type") == affixType):
                    affixes.append(affix_obj)
    
        return affixes
    

    def create_random_affix(self, affixType, ilvl, gear_slot):
        
        js_affixes = self.get_affixes_for_slot(affixType, gear_slot)

        if not js_affixes:
            print(f"Error: No available {affixType} affixes for {gear_slot} (all used or none defined).")
            return None
        
        weights = [bt['weight'] for bt in js_affixes]
        
        js_affix = random.choices(js_affixes, weights=weights)[0]
        
        # save affix to prevent double use
        self.used_affixes.append(js_affix)
        
        return Affix(js_affix, ilvl)
        
        
class Affix():
    def __init__(self, json_affix, ilvl, roll="random"):
        
        # from json
        self.typ = json_affix["type"] # string
        self.name = json_affix["name"] # string
        self.clearName = json_affix["clearName"] # string
        self.slots = json_affix["slots"] # string array
        
        self.ph_description = json_affix["description"] # string, description placeholder
        self.tags = json_affix["tags"] # string array
        
        self.xStat = json_affix["xStat"] # string array
        self.xType = json_affix["xType"] # string
        self.xRange = json_affix["xRange"] # int array
        self.xValue = 0

        # explicit scope for local/global behavior
        self.scope = json_affix.get("scope", "global")
        
        self.yStat = json_affix.get("yStat") # string array
        self.yType = json_affix.get("yType") # string
        self.yRange = json_affix.get("yRange") # int array
        self.yValue = 0
        
        
        self.zStat = json_affix.get("zStat") # string array
        self.zType = json_affix.get("zType") # string
        self.zRange = json_affix.get("zRange") # int array
        self.zValue = 0
        
        # intrinsic
        self.ilvl = ilvl
        
        # roll the value
        if roll == "random":
            roll = random.random()
        
        # calculate explicit values
        self.xValue = (self.xRange[-1] - self.xRange[0]) * ilvl/100 * roll + self.xRange[0]
        self.xValue = round(self.xValue)
        
        if self.yStat != None:
            self.yValue = (self.yRange[-1] - self.yRange[0]) * ilvl/100 * roll + self.yRange[0]
            self.yValue = round(self.yValue)
        
        if self.zStat != None:
            self.zValue = (self.zRange[-1] - self.zRange[0]) * ilvl/100 * roll + self.zRange[0]
            self.zValue = round(self.zValue)
        
        # create boni (only for global scope)
        self.boni = []
        if self.scope == "global":
            if self.xType == "additive":
                self.boni.append(Bonus.Bonus(self.xStat, self.xValue, 0)) 
            elif self.xType == "multiplicative":
                self.boni.append(Bonus.Bonus(self.xStat, 0 , self.xValue))
            
        if self.scope == "global" and self.yStat != None:
            if self.yType == "additive":
                self.boni.append(Bonus.Bonus(self.yStat, self.yValue, 0)) 
            elif self.yType == "multiplicative":
                self.boni.append(Bonus.Bonus(self.yStat, 0 , self.yValue))
                
        if self.scope == "global" and self.zStat != None:
            if self.zType == "additive":
                self.boni.append(Bonus.Bonus(self.zStat, self.zValue, 0)) 
            elif self.zType == "multiplicative":
                self.boni.append(Bonus.Bonus(self.zStat, 0 , self.zValue))
                  
        # create description
        self.description = self.ph_description.replace("xValue", str(self.xValue))
        if self.yStat is not None:
            self.description = self.description.replace("yValue", str(self.yValue))
        if self.zStat is not None:
            self.description = self.description.replace("zValue", str(self.zValue))
        
    def has_tag(self, tag):
        if tag in self.tags:
            return True
        
    def __str__(self):
        return f"{self.name} ({self.clearName}) | {self.typ} \nSlots: {self.slots}\n{self.description}\n{self.xStat} | {self.xType} | {self.xRange} | {self.xValue}\n"
