class Bonus:
    """
    A bonus that can be added to the player stats
    """
    def __init__(self, sid, add_bonus=0, multi_bonus=0):
        self.sid = sid
        self.add_bonus = add_bonus
        self.multi_bonus = multi_bonus
    
    def __str__(self):
        return f"{self.sid} | added: {self.add_bonus} | multi: {self.multi_bonus}"
