import csv
from model.squares import Square, PropertySquare, ChanceSquare, TaxSquare

class Board:
    def __init__(self, csv_file=None, squares=None):
        self.squares = self.load_board_from_csv(csv_file) if csv_file else squares

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
                elif price and rent:  # Property square
                    squares.append(PropertySquare(name, position, int(price), int(rent)))
                else:
                    squares.append(Square(name, position))  # Default square type for unclassified cases
        return squares

    def to_dict(self):
        return [square.to_dict() for square in self.squares]

    @classmethod
    def from_dict(cls, board_data):
        squares = [Square.from_dict(data) for data in board_data]
        return cls(squares=squares)

    def move_player(self, player, steps):
        player.position = (player.position + steps) % len(self.squares)
        print(f"{player.name} moved to {self.squares[player.position].name}.")

    def resolve_square(self, player):
        square = self.squares[player.position]
        square.land_on(player)
