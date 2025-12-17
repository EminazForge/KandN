from __future__ import annotations

import core.stats as Stat


class Character:
    def __init__(self, name: str):
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

        # resources
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

        # slots
        self.stats.append(Stat.Stat("Skill Slots", "ssl", 3, decimals=0))
        self.stats.append(Stat.Stat("Habit slots", "hsl", 2, decimals=0))
        self.stats.append(Stat.Stat("Potion slots", "psl", 1, decimals=0))
        self.stats.append(Stat.Stat("Inventory slots", "isl", 10, decimals=0))

    def get_stat_by_name(self, name: str):
        for stat in self.stats:
            if stat.name == name:
                break
        return stat

    def get_stat_by_id(self, sid: str):
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

    # Transitional wrapper: keep method but delegate to systems layer via local import
    def equip(self, gear_piece):
        from systems import equipment as equipment_system
        return equipment_system.equip(self, gear_piece)

    def unequip(self, gear_slot):
        from systems import equipment as equipment_system
        return equipment_system.unequip(self, gear_slot)

    def apply_gear_boni(self):
        gear_boni = []
        return gear_boni

    def initialize_inventory(self):
        self.inventory = []

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def print_equipment(self):
        print("\nPlayer equipment:")
        for slot_name, item in self.equipment.items():
            if item is None:
                print(f"{slot_name:<{10}} -")
            else:
                print(f"{slot_name:<{10}} {item.name}")

    def print_inventory(self):
        print("\nInventory:")
        for item in self.inventory:
            print(f"{item.name}")

    def __str__(self):
        return f"Character: {self.name} | Level = {self.lvl}"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Quick Character sandbox")
    parser.add_argument("--name", default="Eminaz", help="Character name")
    parser.add_argument("--stats", action="store_true", help="Print all stats")
    parser.add_argument("--equipment", action="store_true", help="Print equipment")
    args = parser.parse_args()

    ch = Character(args.name)
    print(ch)

    if args.stats:
        print("\nStats:")
        for s in ch.stats:
            print(f"- {s.name} ({s.sid}): {s.total}")

    if args.equipment:
        ch.print_equipment()
