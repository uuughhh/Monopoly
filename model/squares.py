import random
from model.player import Player

class Square:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def land_on(self, player):
        print(f"{player.name} landed on {self.position} {self.name}. No effect.")

    def to_dict(self):
        return {"name": self.name, "position": self.position}

    @classmethod
    def from_dict(cls, data):
        return cls(name=data['name'],position=data['position'])

class PropertySquare(Square):
    def __init__(self, name, position, price, rent, owner=None):
        super().__init__(name,position)
        self.price = price
        self.rent = rent
        self.owner = owner

    def to_dict(self):
        if self.owner == None:
            return {"name": self.name, 
                    "position": self.position,
                    "price" : self.price,
                    "rent" : self.rent,
                    "owner" : None
                    }
        else:
            return {"name": self.name, 
                    "position": self.position,
                    "price" : self.price,
                    "rent" : self.rent,
                    "owner" : self.owner.to_dict()
                    }

    @classmethod
    def from_dict(cls, data):
        if data['owner'] != None:
            owner = Player.from_dict(data['owner']),
            return cls(name=data['name'],
                    position=data['position'],
                    price=data['price'],
                    rent=data['rent'],
                    owner=owner
                )
        else:
            return cls(name=data['name'],
                    position=data['position'],
                    price=data['price'],
                    rent=data['rent'],
                    owner=None
                )

    def land_on(self, player):
        if self.owner is None:
            if player.money >= self.price:
                choice = input(f"{self.name} is unowned. Buy for ${self.price}? (y/n): ").lower()
                if choice == 'y':
                    player.money -= self.price
                    self.owner = player
                    player.properties.append(self.name)
                    print(f"{player.name} bought {self.name}.")
        elif self.owner != player.name:
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

class GoJailSquare(Square):
    def land_on(self,player):
        player.in_jail = True
        print(f"{player.name} landed on Jail and is sent to In Jail Square.")


class InJailSqaure (Square):
    def land_on(self, player):
        if player.in_jail == True:
            player.jail_turns += 1
            print(f"{player.name} is in Jail for {player.jail_turns} times")
        else:
            print(f"{player.name} landed on {self.position} {self.name}. No effect.")
        
