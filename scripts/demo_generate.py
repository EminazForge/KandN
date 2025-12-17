"""Quick demo: generate items for each slot and attempt equip."""
import os
import sys
import random

# Ensure project root is on sys.path when running from scripts/
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from systems.item_generator import ItemGenerator
from core.character import Character


def main():
    random.seed(123)
    gen = ItemGenerator()
    char = Character("Demo")

    slots = ["Weapon","Offhand","Helmet","BodyArmor","Boots","Belt","Amulet","Ring"]
    for s in slots:
        item = gen.generateItem(category="Gear", ilvl=1, gearSlot=s, baseType="random")
        print(item.to_tooltip())
        char.equip(item)

    char.print_equipment()

if __name__ == "__main__":
    main()
