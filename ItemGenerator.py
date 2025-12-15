import random as rand
from Affixes import AffixLoader
from Bases import BaseTypeLoader
import Gear

class ItemGenerator():
    
    def __init__(self):
        #rand.seed("eminaz")
        _ = []
            
    def random_category(self, category=None, exclude=[]):
        
        # weighting list
        categoryWeights = [
            ["NoDrop", 100],
            ["Gold", 50],
            ["Potion", 50],
            ["Gear", 100],
            # Add other categories here if you have them
        ]
        
        # apply exclusions
        # This will return a list like [["Gold", 50], ["Potion", 50]]
        processed_category_weights = self.apply_exclusions(categoryWeights, exclude)

        # Separate the category names (population) from their weights
        category_names = [cw[0] for cw in processed_category_weights]
        weights = [cw[1] for cw in processed_category_weights]

        # Use random.choices for weighted selection
        # k=1 means pick one item, [0] extracts it from the resulting list
        random_category = rand.choices(category_names, weights=weights, k=1)[0]
                
        print(f"Selected category: {random_category}")        
            
        return random_category
    
    
    def random_rarity(self, item_find=0, exclude=[]):
        
        rarityWeights = [
            ["Normal", 100],
            ["Magic", 20 * (1 + item_find)],
            ["Rare", 10 * (1 + item_find)],
            # Add other rarities here if you have them, e.g.,
            # ["Unique", 1 * (1 + item_find)],
        ]
    
        # Apply exclusions
        # This will return a list like [["Normal", 100], ["Magic", 200]]
        processed_rarity_weights = self.apply_exclusions(rarityWeights, exclude)

        # Separate the rarity names (population) from their weights
        rarity_names = [rw[0] for rw in processed_rarity_weights]
        weights = [rw[1] for rw in processed_rarity_weights]

        # Use random.choices for weighted selection
        # k=1 means pick one item, [0] extracts it from the resulting list
        randomized_rarity = rand.choices(rarity_names, weights=weights, k=1)[0]

        print(f"\nSelected rarity: {randomized_rarity}")    
        return randomized_rarity
        
    def random_potion(self, exclude=[]):    
        
        potionTypeWeights = [
            ["Life Potion", 100],
            ["Mana Potion", 100],
            # Add other potion types here if you have them, e.g.,
            # ["Rejuvenation Potion", 50],
        ]

        # apply exclusions
        # This will return a list like [["Life Potion", 100]] if Mana Potion is excluded
        processed_potion_type_weights = self.apply_exclusions(potionTypeWeights, exclude)

        # Separate the potion type names (population) from their weights
        potion_type_names = [ptw[0] for ptw in processed_potion_type_weights]
        weights = [ptw[1] for ptw in processed_potion_type_weights]

        # Use random.choices for weighted selection
        # k=1 means pick one item, [0] extracts it from the resulting list
        randomized_potion = rand.choices(potion_type_names, weights=weights, k=1)[0]
    
        print(f"Selected potionType: {randomized_potion}")
    
        return randomized_potion
    

    def apply_exclusions(self, probabilityList, exclude):
        probabilityList = [
            item for item in probabilityList 
            if item[0] not in exclude
        ]
        return probabilityList
    
    
    def random_affixes(self, rarity, ilvl, baseType):
        
        # number of affixes
        number_of_prefixes = 0
        number_of_suffixes = 0
        
        ran = rand.random()
            
        if rarity == "Magic":
            if ran <= 0.3:
                number_of_prefixes = 1
            elif 0.3 < ran and ran <= 0.6:
                number_of_suffixes = 1
            elif 0.6 < ran:
                number_of_prefixes = 1
                number_of_suffixes = 1
            
        elif rarity == "Rare":
            if ran <= 0.4:
                number_of_prefixes = 2
                number_of_suffixes = 1
            elif 0.4 < ran and ran <= 0.8:
                number_of_prefixes = 1
                number_of_suffixes = 2
            elif 0.8 < ran:
                number_of_prefixes = 2
                number_of_suffixes = 2
    
        # roll affixes
        affixLoader = AffixLoader()
        
        #print(f"Prefixes: {number_of_prefixes} | Suffixes: {number_of_suffixes}\n")
        
        gear_slot = baseType.slot
        
        prefixes = []
        suffixes = []
        for pre in range(number_of_prefixes):
            prefix = affixLoader.create_random_affix(affixType="Prefix", ilvl=ilvl, gear_slot=gear_slot)
            prefixes.append(prefix)
            #print(f"Added prefix: {prefix}")
        for suf in range(number_of_suffixes):
            suffix = affixLoader.create_random_affix(affixType="Suffix", ilvl=ilvl, gear_slot=gear_slot)
            suffixes.append(suffix)  
            #print(f"Added suffix: {suffix}")
                
        return prefixes, suffixes
    
    def random_baseType(self, ilvl, exclude, gearSlot="random"):
        
        # roll baseType
        baseTypeLoader = BaseTypeLoader()
        baseType = baseTypeLoader.create_random_baseType(ilvl, exclude, gearSlot)
        
        #print(f"\nSelected baseType: {baseType}")
    
        return baseType
            
    # Name is derived in Gear; legacy method removed for clarity.
    
    
    def generateItem(
            self,
            ilvl=25,
            category="Gear",
            rarity="Rare",
            gearSlot="random",
            baseType="random",
            potionType="random",
            item_find=0,
            exclude=[],
            ):
        
        base = []
        prefixes = []
        suffixes = []
        exceptional = False
        
        print("\nGenerating new item:",
              "\n- item level:", ilvl,
              "\n- category:", category,
              "\n- gearSlot:", gearSlot,
              "\n- rarity:", rarity,
              "\n- base type:", baseType,
              "\n- potion type:", potionType,
              )
        
        # category
        if category == "random":
            category = self.random_category(exclude)

        if category == "Gear":
            # rarity
            if rarity == "random":
                rarity = self.random_rarity(item_find, exclude)        

            # baseType
            if baseType== "random":
                base = self.random_baseType(ilvl, exclude, gearSlot)
            
            # affixes (gear)
            # roll number of affixes
            prefixes, suffixes = self.random_affixes(rarity, ilvl, base)
            
            # exceptionality
            exceptional = rand.choices([False, True], weights=[100, 5])[0]
            
            # create gear
            item = Gear.Gear(rarity=rarity, base=base, exceptional=exceptional, prefixes=prefixes, suffixes=suffixes)
            
            return item
            
            
        if category == "Potion":
            if potionType == "random":
                potionType = self.random_potion(exclude)
            
            # affixes (potion)
            # roll number of suffixes
            # roll suffixes
            # create potion
            
        if category == "Gold":
            # Roll gold amount (function of ilvl)
            gold_amount = round(1 + rand.random() * 20 * ilvl)
            print(f"Gold amount: {gold_amount}")
                    

if __name__ == "__main__":
    generator = ItemGenerator()
    item = generator.generateItem()
    print(item)
    
    print("Boni:")
    for bonus in item.boni:
        print(bonus)
