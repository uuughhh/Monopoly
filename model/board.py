import csv
from model.squares import Square, PropertySquare, ChanceSquare, TaxSquare, GoJailSquare, InJailSqaure

class Board:
    def __init__(self, csv_file=None, squares=None):
        self.squares = self.load_board_from_csv(csv_file) if csv_file else squares
        self.jail_position = None

    def load_board_from_csv(self, csv_file):
        squares = []
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                position = int(row['position'])
                name = row['name']
                price = row['price']
                rent = row['rent']

                if name == "Chance":
                    squares.append(ChanceSquare(name,position))
                elif name == "Income Tax":
                    squares.append(TaxSquare(name,position))
                elif name == "Go":
                    squares.append(Square(name,position))
                elif name == "Go To Jail":
                    squares.append(GoJailSquare(name,position))
                elif name == "In Jail":
                    self.jail_position = position
                    squares.append(InJailSqaure(name,position))
                elif price and rent:  # Property square
                    squares.append(PropertySquare(name, position, int(price), int(rent)))
                else:
                    squares.append(Square(name, position))  # Default square type for unclassified cases
        return squares

    def to_dict(self):
        return [square.to_dict() for square in self.squares]

    @classmethod
    def from_dict(cls, board_data):
        squares = []
        for data in board_data:
            if "rent" in data:
                squares.append(PropertySquare.from_dict(data))
            else:squares.append(Square.from_dict(data))
        return cls(squares=squares)

    def move_player(self, player, steps):
        player.position = (player.position + steps) % 20
        print(f"{player.name} moved to {self.squares[player.position].name}.")

    def resolve_square(self, player):
        square = self.squares[player.position]
        square.land_on(player)

        if self.squares[player.position].name == "Go To Jail":
            player.position = self.jail_position
            print(f"{player.name} moved to {self.jail_position}.")

