class Player:
    def __init__(self, name, money=1500, position=0, properties=None, in_jail=False, jail_turns=0):
        self.name = name
        self.money = money
        self.position = position
        self.properties = properties or []
        self.in_jail = in_jail
        self.jail_turns = jail_turns

    def pay_jail_fine(self):
        if self.money >=150:
            self.money -= 150
            return True
        else: return False

    def release_from_jail(self):
        self.in_jail = False
        self.jail_turns = 0

    def to_dict(self):
        return {
            "name": self.name,
            "money": self.money,
            "position": self.position,
            "properties": self.properties,
            "in_jail": self.in_jail,
            "jail_turns": self.jail_turns
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            money=data['money'],
            position=data['position'],
            properties=['properties'],
            in_jail=data['in_jail'],
            jail_turns=data['jail_turns']
        )
