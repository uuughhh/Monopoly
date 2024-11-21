import csv


class GameboardDesigner:
    SQUARE_TYPES = [
        "Property",
        "Go",
        "Chance",
        "Income Tax",
        "Free Parking",
        "Go to Jail"
    ]

    def __init__(self):
        print("\n--- Gameboard Designer Mode ---")

    def start(self):
        """Gameboard designer main interface."""
        while True:
            print("\nSelect an action:")
            print("1. Create a new gameboard")
            print("2. Load and modify an existing gameboard")
            print("3. Save and exit designer mode")
            choice = input("Enter your choice (1, 2, or 3): ").strip()

            if choice == "1":
                self.create_gameboard()
            elif choice == "2":
                self.load_and_modify_gameboard()
            elif choice == "3":
                print("Exiting Gameboard Designer Mode. Goodbye!")
                return
            else:
                print("Invalid choice. Please try again.")

    def create_gameboard(self):
        """Create a new gameboard."""
        print("\n--- Create a New Gameboard ---")
        squares = []
        while True:
            position = len(squares)
            name = input(f"Enter name for square {position} (or type 'done' to finish): ").strip()
            if name.lower() == "done":
                break

            square_type = self.select_square_type()
            price, rent = None, None

            if square_type == "Property":
                price = input(f"Enter price for {name} (or leave blank for no price): ").strip()
                rent = input(f"Enter rent for {name} (or leave blank for no rent): ").strip()
                price = int(price) if price else None
                rent = int(rent) if rent else None

            squares.append({
                "position": position,
                "name": name,
                "type": square_type,
                "price": price,
                "rent": rent
            })

        # Save the new gameboard to a CSV file
        self.save_gameboard_to_csv(squares)
        print("New gameboard created and saved successfully!")

    def load_and_modify_gameboard(self):
        """Load an existing gameboard and modify its squares."""
        filename = input("\nEnter the name of the gameboard CSV file to load: ").strip()
        try:
            squares = self.load_gameboard_from_csv(filename)
            print("\nGameboard loaded successfully!")
            print(f"{len(squares)} squares found on the gameboard.")
            for square in squares:
                print(f"{square['position']}: {square['name']} ({square['type']}, "
                      f"Price: {square['price']}, Rent: {square['rent']})")

            # Modify the gameboard
            while True:
                position = input("\nEnter the position of the square to modify (or 'done' to finish): ").strip()
                if position.lower() == "done":
                    break

                if position.isdigit() and int(position) < len(squares):
                    position = int(position)
                    square = squares[position]
                    print(f"Current: {square['name']} ({square['type']}, "
                          f"Price: {square['price']}, Rent: {square['rent']})")

                    name = input("Enter new name (or leave blank to keep current): ").strip()
                    if name:
                        square["name"] = name

                    new_type = self.select_square_type(default=square["type"])
                    if new_type != square["type"]:
                        square["type"] = new_type
                        square["price"], square["rent"] = None, None  # Reset price and rent for non-property squares
                        if new_type == "Property":
                            square["price"] = int(input("Enter new price: ").strip() or 0)
                            square["rent"] = int(input("Enter new rent: ").strip() or 0)

                    squares[position] = square
                else:
                    print("Invalid position. Please try again.")

            # Save the modified gameboard
            self.save_gameboard_to_csv(squares, filename)
            print("Gameboard modified and saved successfully!")
        except FileNotFoundError:
            print("Gameboard file not found. Please try again.")

    def select_square_type(self, default=None):
        """Allow the designer to select a square type."""
        print("\nSelect a square type:")
        for i, square_type in enumerate(self.SQUARE_TYPES, 1):
            print(f"{i}. {square_type}")
        choice = input(f"Enter your choice (1-{len(self.SQUARE_TYPES)})"
                       f"{f' (default: {default})' if default else ''}: ").strip()

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(self.SQUARE_TYPES):
                return self.SQUARE_TYPES[index]
        if default:
            return default
        print("Invalid choice. Please try again.")
        return self.select_square_type(default)

    def save_gameboard_to_csv(self, squares, filename="gameboard.csv"):
        """Save the gameboard to a CSV file."""
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["position", "name", "type", "price", "rent"])
            for square in squares:
                writer.writerow([square["position"], square["name"], square["type"], square["price"], square["rent"]])
        print(f"Gameboard saved to {filename}.")

    def load_gameboard_from_csv(self, filename):
        """Load a gameboard from a CSV file."""
        squares = []
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                squares.append({
                    "position": int(row["position"]),
                    "name": row["name"],
                    "type": row["type"],
                    "price": int(row["price"]) if row["price"] else None,
                    "rent": int(row["rent"]) if row["rent"] else None
                })
        return squares
