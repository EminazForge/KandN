class Stat():
    def __init__(self, name="NoName", sid="NoID", base=0, decimals=2, minimum=-1e6, maximum=1e6):
        self.name= name
        self.sid = sid
        self.base = base
        self.decimals = decimals
        self.minimum = minimum
        self.maximum = maximum
        self.add_boni = []
        self.multi_boni = []
        self.total = 0
        self.total_additives = 0
        self.total_multiplier = 0
        self.update_total()
        
    def add_bonus(self, add_bonus=0, multi_bonus=0):
        self.total_additives += add_bonus
        self.total_multiplier += multi_bonus
        self.update_total()
        
    def update_total(self):
        self.total = (self.base + self.total_additives)*(1 + self.total_multiplier / 100)
        
        # rounding
        self.total = round(self.total, self.decimals)
        
        # validity checks
        if self.total > self.maximum:
            self.total = self. maximum
        if self.total < self.minimum:
            self.total = self.minimum
        
    
    def __str__(self):
        return f"{self.name} | {self.sid} | base: {self.base} | added: {self.total_additives} | multi: {self.total_multiplier} | total: {self.total}"     