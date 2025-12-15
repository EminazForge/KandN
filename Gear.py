class Gear():
    def __init__(self,
                 name: str = "NoName",
                 rarity: str = "normal",
                 base = None,
                 exceptional: bool = False,
                 prefixes = None,
                 suffixes = None):

        # Inputs (do not mutate caller-provided lists)
        self.name = name
        self.rarity = rarity
        self.base = base
        self.exceptional = exceptional
        self.prefixes = prefixes
        self.suffixes = suffixes

        # Initialize derived/defaulted fields
        self.lvl_req_red = 0
        self.req_red = 0

        # Base-derived fields (set after base is present)
        # If base is None, keep sensible defaults to avoid attribute errors

        self.slot = self.base.slot
        self.lvl_req = self.base.lvl_req
        self.str_req = self.base.str_req
        self.int_req = self.base.int_req
        self.dex_req = self.base.dex_req

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
        # Build only the logical name_description string (no printing)
        # Mirror original casing checks and structure
        if self.rarity == "Normal":
            if self.exceptional:
                self.name_description = "Exceptional " + self.base.name
            else:
                self.name_description = self.base.name
        elif self.rarity == "Magic":
            if self.exceptional:
                self.name_description = self.name + "\nExceptional " + self.base.name
            else:
                self.name_description = self.name
        elif self.rarity == "Rare":
            if self.exceptional:
                self.name_description = self.name + "\nExceptional " + self.base.name
            else:
                self.name_description = self.name + "\n" + self.base.name
        else:
            # fallback behavior for unexpected rarity values
            self.name_description = self.name if self.name else (self.base.name if self.base else "NoName")

    def apply_affixes(self):
        # --------------------------- descriptions --------------------------
        self.affix_descriptions = ""
        for prefix in self.prefixes:
            self.affix_descriptions += "\n(P) " + prefix.description
        for suffix in self.suffixes:
            self.affix_descriptions += "\n(S) " + suffix.description

        if self.affix_descriptions:
            self.affix_descriptions = "\n------------------------------------------\n" + self.affix_descriptions

        # -------------------------- modify boni ----------------------------
        # handle implicit modifiers
        for prefix in self.prefixes:
            if prefix.xStat == "impl":
                if prefix.xType == "additive":
                    self.base.modify_base_values(add_mod=prefix.xValue)
                elif prefix.xType == "multiplicative":
                    self.base.modify_base_values(multi_mod=prefix.xValue)

        # handle suffixes that change requirements
        for suffix in self.suffixes:
            if suffix.xStat == "att_red":
                self.req_red += suffix.xValue
            if suffix.xStat == "lev_red":
                self.lvl_req_red += suffix.xValue

        # -------------------------- apply boni -----------------------------
        self.boni = []
        for bonus in self.base.boni:
            self.boni.append(bonus)

        for prefix in self.prefixes:
            self.boni.extend(prefix.boni)

        for suffix in self.suffixes:
            self.boni.extend(suffix.boni)

    def determine_reqs(self):
        # stat requirements (apply req_red collected from suffixes)
        self.stat_req_string = "\n"
        if self.base.str_req != 0:
            self.str_req = round(self.base.str_req * (1 - self.req_red / 100))
            self.stat_req_string += f"Req. Str.: {self.str_req}"
        if self.base.int_req != 0:
            self.int_req = round(self.base.int_req * (1 - self.req_red / 100))
            self.stat_req_string += f"Req. Int.: {self.int_req}"
        if self.base.dex_req != 0:
            self.dex_req = round(self.base.dex_req * (1 - self.req_red / 100))
            self.stat_req_string += f"Req. Dex.: {self.dex_req}"

        # level requirement (apply lvl_req_red)
        # Use self.lvl_req (initialized from base earlier) and reduce
        self.lvl_req = max(self.lvl_req - self.lvl_req_red, 1)

    def apply_description(self):
        # Keep this small helper (same behavior as original)
        if self.base.description == "":
            self.base_descriptions = "\n"
        else:
            self.base_descriptions = "\n------------------------------------------\n" + self.base.description

    def build_tooltip(self):
        # Build the base description string used by __str__
        # This keeps the separators and layout exactly like your original example.
        self.apply_description()  # ensure base_descriptions is set
        # Compose final block for printing
        self.full_description = (
            f"\n==========================================\n"
            f"{self.name_description} \n"
            f"Req. Level: {self.lvl_req}{self.stat_req_string}{self.base_descriptions}{self.affix_descriptions}\n"
            f"==========================================\n"
        )

    def __str__(self):
        # Return the prebuilt full description for performance/readability
        return self.full_description


if __name__ == "__main__":
    print("Error: Cannot create gear directly. Need initializations.")