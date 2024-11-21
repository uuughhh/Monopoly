import random

class Square:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def land_on(self, player):
        print(f"{player.name} landed on {self.position} {self.name}. No effect.")

    def to_dict(self):
        return {"name": self.name}

    @classmethod
    def from_dict(cls, data):
        return cls(name=data['name'])

class PropertySquare(Square):
    def __init__(self, name, position, price, rent):
        super().__init__(name,position)
        self.price = price
        self.rent = rent
        self.owner = None

    def land_on(self, player):
        if self.owner is None:
            if player.money >= self.price:
                choice = input(f"{self.name} is unowned. Buy for ${self.price}? (y/n): ").lower()
                if choice == 'y':
                    player.money -= self.price
                    self.owner = player
                    player.properties.append(self)
                    print(f"{player.name} bought {self.name}.")
        elif self.owner != player:
            print(f"{player.name} pays ${self.rent} rent to {self.owner.name}.")
            player.money -= self.rent
            self.owner.money += self.rent

class ChanceSquare(Square):
    def land_on(self, player):
        amount = random.choice([-300, -200, -100, 100, 200])
        player.money += amount
        action = "gained" if amount > 0 else "lost"
        print(f"{player.name} landed on Chance and {action} ${abs(amount)}.")

class TaxSquare(Square):
    def land_on(self, player):
        tax = player.money // 10
        player.money -= tax
        print(f"{player.name} paid ${tax} in taxes.")
