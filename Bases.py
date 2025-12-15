import json
import os
import random
import Bonus

# --- Configuration ---
JSON_FILE_PATH = "Bases.json"

class BaseTypeLoader():
    
    def __init__(self):
        
        self.baseTypeList = self.load_data(JSON_FILE_PATH)
    
    def load_data(self, file_path=JSON_FILE_PATH):
        """
        Loads affix data from a JSON file and returns it as a Python dictionary.
        """
        
        if not os.path.exists(file_path):
            print(f"Warning: File '{file_path}' not found. Returning empty data.")
            return {}
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            #print(f"Affix data was loaded from {file_path}")
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}. File might be corrupted.")
            return {}
        except IOError as e:
            print(f"Error loading data from {file_path}: {e}")
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


if __name__ == "__main__":
    # Exploration utility: summarize base data to inform JSON updates
    baseTypeLoader = BaseTypeLoader()
    data = baseTypeLoader.baseTypeList  # raw JSON dict

    total = len(data)
    print("Base data analysis:")
    print(f"Total bases: {total}")

    # Counts and weight stats per slot
    from collections import defaultdict
    slot_counts = defaultdict(int)
    slot_drop_stats = defaultdict(lambda: {"count":0, "sum":0, "min":None, "max":None})

    overall_sum = 0
    overall_min = None
    overall_max = None

    lvl_reqs = []

    for bt in data.values():
        slot = bt.get("slot", "Unknown")
        dc = bt.get("weight", 0)
        ilvl_req = bt.get("lvl_req", 0)

        slot_counts[slot] += 1

        s = slot_drop_stats[slot]
        s["count"] += 1
        s["sum"] += dc
        s["min"] = dc if s["min"] is None else min(s["min"], dc)
        s["max"] = dc if s["max"] is None else max(s["max"], dc)

        overall_sum += dc
        overall_min = dc if overall_min is None else min(overall_min, dc)
        overall_max = dc if overall_max is None else max(overall_max, dc)

        lvl_reqs.append(ilvl_req)

    overall_avg = (overall_sum / total) if total else 0

    print(f"Overall weight → avg: {overall_avg:.2f}, min: {overall_min}, max: {overall_max}")
    if lvl_reqs:
        print(f"Level req range → min: {min(lvl_reqs)}, max: {max(lvl_reqs)}")

    # Consolidated slot summary: count, avg weight, and overall chance
    print("\nSlots (count | avg weight | overall chance):")
    total_weight_overall = sum(bt.get("weight", 0) for bt in data.values())
    for slot in sorted(slot_counts.keys()):
        stats = slot_drop_stats[slot]
        avg = (stats["sum"] / stats["count"]) if stats["count"] else 0
        slot_weight = sum(bt.get("weight", 0) for bt in data.values() if bt.get("slot") == slot)
        overall_p = (slot_weight / total_weight_overall * 100) if total_weight_overall else 0
        print(f"- {slot}: {slot_counts[slot]} | {avg:.2f} | {overall_p:.2f}%")

    # Actual probabilities based on weights (overall)
    print("\nOverall drop probabilities (normalized by total weight):")
    total_weight = sum(bt.get("weight", 0) for bt in data.values())
    if total_weight > 0:
        # Show top N by probability
        probs = []
        for bt in data.values():
            w = bt.get("weight", 0)
            p = w / total_weight
            probs.append((bt.get("name"), bt.get("slot"), w, p))
        # Sort by probability desc
        probs.sort(key=lambda x: x[3], reverse=True)
        for name, slot, w, p in probs[:10]:
            print(f"- {name} ({slot}) | weight = {w}, chance = {(p*100):.2f}%")
    else:
        print("- No weight found to compute probabilities.")

    # Example: show allowed bases near a given ilvl and probabilities within that pool
    ilvl = 15
    allowed = baseTypeLoader.get_allowed_baseTypes(ilvl=ilvl)
    print(f"\nAllowed bases at ilvl {ilvl}: {len(allowed)}")
    allowed_total_weight = sum(bt.get("weight", 0) for bt in allowed)
    if allowed_total_weight > 0:
        # Show probabilities within allowed pool
        allowed_probs = []
        for bt in allowed:
            w = bt.get("weight", 0)
            p = w / allowed_total_weight
            allowed_probs.append((bt.get("name"), bt.get("slot"), w, p, bt.get("lvl_req")))
        # Sort by probability desc
        allowed_probs.sort(key=lambda x: x[3], reverse=True)
        for name, slot, w, p, req in allowed_probs[:10]:
            print(f"- {name} ({slot}) req={req} | weight = {w}, chance = {(p*100):.2f}%")
    else:
        print("- No allowed weights to compute probabilities.")

    # Consolidated allowed slot summary: count, avg weight (global avg), and allowed chance
    print(f"\nSlots within allowed (ilvl {ilvl}) (count | avg weight | allowed chance):")
    if allowed_total_weight > 0:
        for slot in sorted(slot_counts.keys()):
            stats = slot_drop_stats[slot]
            avg = (stats["sum"] / stats["count"]) if stats["count"] else 0
            allowed_slot_weight = sum(bt.get("weight", 0) for bt in allowed if bt.get("slot") == slot)
            allowed_p = (allowed_slot_weight / allowed_total_weight * 100)
            print(f"- {slot}: {slot_counts[slot]} | {avg:.2f} | {allowed_p:.2f}%")
    else:
        print("- No allowed weights found for slot probabilities.")



