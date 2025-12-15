import Bonus
import ItemGenerator
import Stat   
        
class Character():
    def __init__(self, name):
        self.name = name
        self.lvl = 1
        self.exp = 0
        self.total_skill_points = 0
        self.left_skill_points = 0
        self.gold = 0
        
        self.initialize_stats()
        self.initialize_gear()
        self.initialize_inventory()
        
    def initialize_stats(self):
        self.stats = []
        
        # ressources
        self.stats.append(Stat.Stat("Life", "hp", 10))
        self.stats.append(Stat.Stat("Mana", "mana", 10))
        self.stats.append(Stat.Stat("Speed", "sp", 0))
        
        # attributes
        self.stats.append(Stat.Stat("Strength", "str", 10))
        self.stats.append(Stat.Stat("Intelligence", "int", 10))
        self.stats.append(Stat.Stat("Dexterity", "dex", 10))
        
        # offenses
        self.stats.append(Stat.Stat("Minimum physical damage", "minpd", 1))
        self.stats.append(Stat.Stat("Maximum physical damage", "maxpd", 2))
        self.stats.append(Stat.Stat("Minimum spell damage", "maxsd", 2))
        self.stats.append(Stat.Stat("Maximum spell damage", "maxsd", 2))
        self.stats.append(Stat.Stat("Accuracy", "acc", 0.8))
        
        # defenses
        self.stats.append(Stat.Stat("Armor", "armor", 0))
        self.stats.append(Stat.Stat("Fire Resistance", "fires", 0))
        self.stats.append(Stat.Stat("Shock Resistance", "shres", 0))
        self.stats.append(Stat.Stat("Frost Resistance", "frres", 0))
        self.stats.append(Stat.Stat("Chaos Resistance", "chres", 0))
        self.stats.append(Stat.Stat("Evasion", "ev", 0.2))
        
        # misc
        self.stats.append(Stat.Stat("Gold Find", "gfin", 0))
        self.stats.append(Stat.Stat("Magic Find", "mfin", 0))
        self.stats.append(Stat.Stat("Flee Chance", "fch", 0))
        self.stats.append(Stat.Stat("Merchant prices", "mpr", 0))
        
        #slots
        self.stats.append(Stat.Stat("Skill Slots", "ssl", 3, decimals=0))
        self.stats.append(Stat.Stat("Habit slots", "hsl", 2, decimals=0))
        self.stats.append(Stat.Stat("Potion slots", "psl", 1, decimals=0))
        self.stats.append(Stat.Stat("Inventory slots", "isl", 10, decimals=0))
    
    def get_stat_by_name(self, name):
        for stat in self.stats:
            if stat.name == name:
                break
        return stat
    
    def get_stat_by_id(self, sid):
        for stat in self.stats:
            if stat.sid == sid:
                break
        return stat
    
    def apply_bonus_to_stat(self, bonus):
        self.get_stat_by_id(bonus.sid).add_bonus(bonus.add_bonus, bonus.multi_bonus)   
        
    def initialize_gear(self):
        self.equipment = {
            "Weapon": None,
            "Offhand": None,
            "Helmet": None,
            "BodyArmor": None,
            "Boots": None,
            "Belt": None,
            "Amulet": None,
            "Ring": None,
            }
        
    def equip(self, gear_piece):
                
        # requirement
        # level
        if gear_piece.lvl_req > self.lvl:
            print(f"Player cannot equip \"{gear_piece.name}\" due to its level restrictions")
            return
        # strength
        if gear_piece.str_req > self.get_stat_by_id("str").total:
            print(f"Player cannot equip \"{gear_piece.name}\" due to its Strength restrictions")
            return
        # intelligence
        if gear_piece.str_req > self.get_stat_by_id("int").total:
            print(f"Player cannot equip \"{gear_piece.name}\" due to its Intelligence restrictions")
            return
        # dexterity
        if gear_piece.str_req > self.get_stat_by_id("dex").total:
            print(f"Player cannot equip \"{gear_piece.name}\" due to its Dexterity restrictions")
            return

        print(f"Player equips \"{gear_piece.name}\"")
        
        if gear_piece.slot == "Weapon":
            self.equipment["Weapon"] = gear_piece
            
        if gear_piece.slot == "Wand":
            self.equipment["Weapon"] = gear_piece  
            
        if gear_piece.slot == "Offhand":
            self.equipment["Offhand"] = gear_piece
            
        if gear_piece.slot == "Shield":
            self.equipment["Offhand"] = gear_piece  
            
        if gear_piece.slot == "Helmet":
            self.equipment["Helmet"] = gear_piece
            
        if gear_piece.slot == "BodyArmor":
            self.equipment["BodyArmor"] = gear_piece
            
        if gear_piece.slot == "Boots":
            self.equipment["Boots"] = gear_piece
            
        if gear_piece.slot == "Belt":
            self.equipment["Belt"] = gear_piece
            
        if gear_piece.slot == "Amulet":
            self.equipment["Amulet"] = gear_piece
            
        if gear_piece.slot == "Ring":
            self.equipment["Ring"] = gear_piece
        
    def unequip(self, gear_slot):
        
        if self.equipment[gear_slot] != None:
            print(f"Unequipping {self.equipment.get(gear_slot).name}")    
            self.inventory.append(self.equipment[gear_slot])
            self.equipment[gear_slot] = None
    
        
    def apply_gear_boni(self):     
        gear_boni = []
        
        
    def initialize_inventory(self):
        self.inventory = []

        
    def add_to_inventory(self, item):
        self.inventory.append(item)
        
    def print_equipment(self):
        print("\nPlayer equipment:")
             
        for slot_name, item in self.equipment.items():
            if item == None:
                print(f"{slot_name:<{10}} -")
            else:
                print(f"{slot_name:<{10}} {item.name}")
                
    def print_inventory(self):
        print("\nInventory:")
             
        for item in self.inventory:
            print(f"{item.name}")
        
    def __str__(self):
        return f"Character: {self.name} | Level = {self.lvl}"
        


char = Character("Eminaz")
print(char)

#print(char.get_stat_by_id("ssl"))
bonus = Bonus.Bonus("ssl", 5, 0)

generator = ItemGenerator.ItemGenerator()

gear_piece = generator.generateItem(category="Gear", ilvl=1, gearSlot="Weapon")
char.equip(gear_piece)
print(char.equipment["Weapon"])
gear_piece = generator.generateItem(category="Gear", ilvl=1, gearSlot="Offhand")
char.equip(gear_piece)
gear_piece = generator.generateItem(category="Gear", ilvl=1, gearSlot="Helmet")
char.equip(gear_piece)
gear_piece = generator.generateItem(category="Gear", ilvl=1, gearSlot="BodyArmor")
char.equip(gear_piece)
gear_piece = generator.generateItem(category="Gear", ilvl=1, gearSlot="Boots")
char.equip(gear_piece)
gear_piece = generator.generateItem(category="Gear", ilvl=1, gearSlot="Belt")
char.equip(gear_piece)
gear_piece = generator.generateItem(category="Gear", ilvl=1, gearSlot="Ring")
char.equip(gear_piece)
gear_piece = generator.generateItem(category="Gear", ilvl=1, gearSlot="Amulet")
char.equip(gear_piece)


char.print_equipment()