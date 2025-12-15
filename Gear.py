class Gear():
    def __init__(self,
                 name: str | None = None,
                 rarity: str = "normal",
                 base = None,
                 exceptional: bool = False,
                 prefixes = None,
                 suffixes = None):

        # Inputs (do not mutate caller-provided lists)
        self.name = name  # optional override; if None, derive from components
        self.rarity = rarity
        self.base = base
        self.exceptional = exceptional
        self.prefixes = prefixes or []
        self.suffixes = suffixes or []

        # Initialize derived/defaulted fields
        self.lvl_req_red = 0
        self.req_red = 0

        # Base-derived fields (set after base is present)
        # If base is None, keep sensible defaults to avoid attribute errors
        if self.base is not None:
            self.slot = self.base.slot
            self.lvl_req = self.base.lvl_req
            self.str_req = self.base.str_req
            self.int_req = self.base.int_req
            self.dex_req = self.base.dex_req
        else:
            self.slot = "unknown"
            self.lvl_req = 1
            self.str_req = 0
            self.int_req = 0
            self.dex_req = 0

        # Apply exceptional base modification if requested (same behavior as original)
        if self.exceptional and self.base is not None:
            # keep original call to base.modify_base_values to preserve behavior
            self.base.modify_base_values(multi_mod=50)

        # Orchestrate building the gear
        self.construct_name()
        self.apply_affixes()
        self.determine_reqs()
        self.build_tooltip()

    def construct_name(self):
        # Derive the display name based on base and affixes if no explicit name provided.
        base_name = (self.base.name if self.base else "Gear")
        vague_name = (getattr(self.base, "vagueName", base_name) if self.base else base_name)

        # If explicit name is provided, honor it for Magic/Rare primary line
        explicit = bool(self.name)

        if self.rarity == "Normal":
            derived = base_name
            if self.exceptional:
                derived = "Exceptional " + base_name
            self.name_description = derived

        elif self.rarity == "Magic":
            # Magic naming: "<Prefix.clearName> <Base.name> <Suffix.clearName>" if available
            pref = self.prefixes[0].clearName + " " if (self.prefixes and getattr(self.prefixes[0], "clearName", "")) else ""
            suf = (" " + self.suffixes[0].clearName) if (self.suffixes and getattr(self.suffixes[0], "clearName", "")) else ""
            derived = f"{pref}{base_name}{suf}".strip()
            primary = self.name if explicit else derived
            if self.exceptional:
                self.name_description = primary + "\nExceptional " + base_name
            else:
                self.name_description = primary

        elif self.rarity == "Rare":
            # Rare naming: choose one affix.name and combine with base.vagueName
            affix_names = [getattr(a, "name", "") for a in (self.prefixes + self.suffixes) if getattr(a, "name", "")]
            chosen = affix_names[0] if affix_names else (self.name if explicit else "Nameless")
            primary = self.name if explicit else f"{chosen} {vague_name}".strip()
            if self.exceptional:
                self.name_description = primary + "\nExceptional " + base_name
            else:
                self.name_description = primary + "\n" + base_name

        else:
            # Fallback for unexpected rarity values
            self.name_description = self.name if explicit else base_name

    def apply_affixes(self):
        # --------------------------- descriptions --------------------------
        affix_lines = []
        for prefix in self.prefixes:
            affix_lines.append("(P) " + getattr(prefix, "description", str(prefix)))
        for suffix in self.suffixes:
            affix_lines.append("(S) " + getattr(suffix, "description", str(suffix)))

        if affix_lines:
            self.affix_descriptions = "\n------------------------------------------\n" + "\n".join(affix_lines)
        else:
            self.affix_descriptions = ""

        # -------------------------- apply effects --------------------------
        # Separate base boni (from base after local modifiers) and global affix boni
        # 1) Apply local affixes to base implicits
        if self.base is not None:
            for aff in (self.prefixes + self.suffixes):
                if getattr(aff, "scope", "global") == "local":
                    xType = getattr(aff, "xType", None)
                    xValue = getattr(aff, "xValue", 0)
                    if xType == "additive":
                        self.base.modify_base_values(add_mod=xValue)
                    elif xType == "multiplicative":
                        self.base.modify_base_values(multi_mod=xValue)

        # 2) Requirement reducers (global effects that aren't normal boni)
        for aff in (self.prefixes + self.suffixes):
            if getattr(aff, "xStat", None) == "att_red":
                self.req_red += getattr(aff, "xValue", 0)
            if getattr(aff, "xStat", None) == "lvl_red":
                self.lvl_req_red += getattr(aff, "xValue", 0)

        # 3) Aggregate boni
        self.base_boni = []
        self.affix_boni = []

        if self.base is not None:
            self.base_boni.extend(getattr(self.base, "boni", []))

        for aff in (self.prefixes + self.suffixes):
            if getattr(aff, "scope", "global") == "global":
                self.affix_boni.extend(getattr(aff, "boni", []))

        # Public combined view
        self.boni = self.base_boni + self.affix_boni

    def determine_reqs(self):
        # stat requirements (apply req_red collected from suffixes)
        req_parts = []
        if self.base is not None and getattr(self.base, "str_req", 0) != 0:
            self.str_req = round(self.base.str_req * (1 - self.req_red / 100))
            req_parts.append(f"Req. Str.: {self.str_req}")
        if self.base is not None and getattr(self.base, "int_req", 0) != 0:
            self.int_req = round(self.base.int_req * (1 - self.req_red / 100))
            req_parts.append(f"Req. Int.: {self.int_req}")
        if self.base is not None and getattr(self.base, "dex_req", 0) != 0:
            self.dex_req = round(self.base.dex_req * (1 - self.req_red / 100))
            req_parts.append(f"Req. Dex.: {self.dex_req}")

        self.stat_req_string = ("\n" + " ".join(req_parts)) if req_parts else ""

        # level requirement (apply lvl_req_red)
        # Use self.lvl_req (initialized from base earlier) and reduce
        self.lvl_req = max(self.lvl_req - self.lvl_req_red, 1)

    def apply_description(self):
        # Keep this small helper (same behavior as original)
        if self.base is None or getattr(self.base, "description", "") == "":
            self.base_descriptions = ""
        else:
            self.base_descriptions = "\n------------------------------------------\n" + self.base.description

    def build_tooltip(self):
        # Build the base description string used by __str__
        # This keeps the separators and layout exactly like your original example.
        self.apply_description()  # ensure base_descriptions is set
        # Compose final block for printing avoiding empty lines
        body = []
        body.append(self.name_description)
        req_line = f"Req. Level: {self.lvl_req}"
        body.append(req_line + (self.stat_req_string if self.stat_req_string else ""))
        if self.base_descriptions:
            body.append(self.base_descriptions.strip("\n"))
        if self.affix_descriptions:
            body.append(self.affix_descriptions.strip("\n"))

        content = "\n".join(body)
        self.full_description = (
            f"\n==========================================\n" +
            content +
            f"\n==========================================\n"
        )

    def to_tooltip(self):
        # Public method to retrieve the full multi-line tooltip
        return self.full_description

    def to_dict(self):
        # Structured representation for testing/UI
        return {
            "name": self.name_description.split("\n")[0],
            "rarity": self.rarity,
            "slot": self.slot,
            "ilvl_req": self.lvl_req,
            "reqs": {
                "str": getattr(self, "str_req", 0),
                "int": getattr(self, "int_req", 0),
                "dex": getattr(self, "dex_req", 0),
            },
            "base_description": self.base_descriptions,
            "affix_descriptions": self.affix_descriptions,
            "base_boni": [str(b) for b in getattr(self, "base_boni", [])],
            "affix_boni": [str(b) for b in getattr(self, "affix_boni", [])],
        }

    def __str__(self):
        # Concise one-liner for logging/debugging
        primary = self.name_description.split("\n")[0]
        return f"{primary} ({self.rarity})"


if __name__ == "__main__":
    # Standalone demo using real Bases and Affixes loaders.
    import Affixes
    import Bases

    # Choose an item level and slot to demonstrate
    ilvl = 20
    gear_slot = "Helmet"

    # Load a random base that fits ilvl and slot
    base_loader = Bases.BaseTypeLoader()
    base = base_loader.create_random_baseType(ilvl=ilvl, gearSlot=gear_slot)

    # Create one random prefix and one random suffix for the chosen slot
    affix_loader = Affixes.AffixLoader()
    prefixes = [affix_loader.create_random_affix("Prefix", ilvl, base.slot)]
    suffixes = [affix_loader.create_random_affix("Suffix", ilvl, base.slot)]

    gear = Gear(rarity="Magic", base=base, exceptional=False, prefixes=prefixes, suffixes=suffixes)
    print(gear.to_tooltip())