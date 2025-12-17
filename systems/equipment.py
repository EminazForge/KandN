from typing import Optional

# Simple slot normalization to keep synonyms unified
SLOT_ALIASES = {
    "Wand": "Weapon",
    "Shield": "Offhand",
}


def normalize_slot(slot: str) -> str:
    return SLOT_ALIASES.get(slot, slot)


def check_requirements(character, gear_piece) -> Optional[str]:
    """Return None if ok, else an error reason string."""
    # Level
    if getattr(gear_piece, "lvl_req", 1) > getattr(character, "lvl", 1):
        return "level restrictions"
    # Strength
    if getattr(gear_piece, "str_req", 0) > character.get_stat_by_id("str").total:
        return "Strength restrictions"
    # Intelligence
    if getattr(gear_piece, "int_req", 0) > character.get_stat_by_id("int").total:
        return "Intelligence restrictions"
    # Dexterity
    if getattr(gear_piece, "dex_req", 0) > character.get_stat_by_id("dex").total:
        return "Dexterity restrictions"
    return None


def equip(character, gear_piece) -> bool:
    """Attempt to equip a gear piece on character. Returns True on success."""
    reason = check_requirements(character, gear_piece)
    if reason is not None:
        print(f"Player cannot equip \"{gear_piece.name}\" due to its {reason}")
        return False

    print(f"Player equips \"{gear_piece.name}\"")
    slot = normalize_slot(getattr(gear_piece, "slot", "unknown"))
    if slot not in character.equipment:
        # Unknown slot, abort equip
        print(f"Unknown slot '{slot}' for item {gear_piece.name}")
        return False

    character.equipment[slot] = gear_piece
    return True


def unequip(character, gear_slot: str) -> bool:
    slot = normalize_slot(gear_slot)
    item = character.equipment.get(slot)
    if item is None:
        return False
    print(f"Unequipping {item.name}")
    character.inventory.append(item)
    character.equipment[slot] = None
    return True
