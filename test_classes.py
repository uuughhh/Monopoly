import unittest
from unittest.mock import patch, MagicMock, mock_open
from model.player import Player
from model.squares import Square,TaxSquare,ChanceSquare,PropertySquare,GoJailSquare,InJailSqaure
from model.board import Board
from model.gameboardDesign import GameboardDesigner

class TestPlayer(unittest.TestCase):
    def test_player_initialization(self):
        player = Player("Alice", money=2000, position=5, properties=["Park Place"], in_jail=True, jail_turns=2)
        self.assertEqual(player.name, "Alice")
        self.assertEqual(player.money, 2000)
        self.assertEqual(player.position, 5)
        self.assertEqual(player.properties, ["Park Place"])
        self.assertTrue(player.in_jail)
        self.assertEqual(player.jail_turns, 2)

    def test_pay_jail_fine_success(self):
        player = Player("Bob", money=200)
        result = player.pay_jail_fine()
        self.assertTrue(result)
        self.assertEqual(player.money, 50)

    def test_pay_jail_fine_failure(self):
        player = Player("Charlie", money=100)
        result = player.pay_jail_fine()
        self.assertFalse(result)
        self.assertEqual(player.money, 100)

    def test_release_from_jail(self):
        player = Player("Dave", in_jail=True, jail_turns=3)
        player.release_from_jail()
        self.assertFalse(player.in_jail)
        self.assertEqual(player.jail_turns, 0)

    def test_to_dict(self):
        player = Player("Eve", money=1500, position=6, properties=["Boardwalk"], in_jail=False, jail_turns=0)
        expected_dict = {
            "name": "Eve",
            "money": 1500,
            "position": 6,
            "properties": ["Boardwalk"],
            "in_jail": False,
            "jail_turns": 0
        }
        self.assertEqual(player.to_dict(), expected_dict)

    def test_from_dict(self):
        data = {
            "name": "Frank",
            "money": 1800,
            "position": 3,
            "properties": ["Baltic Avenue"],
            "in_jail": True,
            "jail_turns": 2
        }
        player = Player.from_dict(data)
        self.assertEqual(player.name, "Frank")
        self.assertEqual(player.money, 1800)
        self.assertEqual(player.position, 3)
        self.assertEqual(player.properties, ["Baltic Avenue"])
        self.assertTrue(player.in_jail)
        self.assertEqual(player.jail_turns, 2)


class TestSquares(unittest.TestCase):
    def test_square_land_on(self):
        square = Square("Go", 0)
        player = Player("Alice")
        with patch("builtins.print") as mocked_print:
            square.land_on(player)
            mocked_print.assert_called_with("Alice landed on 0 Go. No effect.")

    def test_property_square_buy(self):
        property_square = PropertySquare("Boardwalk", 1, price=400, rent=50)
        player = Player("Alice", money=500)
        with patch("builtins.input", return_value="y"):
            with patch("builtins.print") as mocked_print:
                property_square.land_on(player)
                self.assertEqual(player.money, 100)
                self.assertEqual(property_square.owner, player)
                self.assertIn("Boardwalk", player.properties)
                mocked_print.assert_called_with("Alice bought Boardwalk.")

    def test_property_square_pay_rent(self):
        owner = Player("Bob", money=1000)
        property_square = PropertySquare("Boardwalk", 1, price=400, rent=50, owner=owner)
        player = Player("Alice", money=500)
        with patch("builtins.print") as mocked_print:
            property_square.land_on(player)
            self.assertEqual(player.money, 450)
            self.assertEqual(owner.money, 1050)
            mocked_print.assert_called_with("Alice pays $50 rent to Bob.")

    def test_chance_square_land_on(self):
        chance_square = ChanceSquare("Chance", 2)
        player = Player("Alice", money=1000)
        with patch("random.choice", return_value=200):
            with patch("builtins.print") as mocked_print:
                chance_square.land_on(player)
                self.assertEqual(player.money, 1200)
                mocked_print.assert_called_with("Alice landed on Chance and gained $200.")

    def test_tax_square_land_on(self):
        tax_square = TaxSquare("Income Tax", 3)
        player = Player("Alice", money=1000)
        with patch("builtins.print") as mocked_print:
            tax_square.land_on(player)
            self.assertEqual(player.money, 900)
            mocked_print.assert_called_with("Alice paid $100 in taxes.")

    def test_go_jail_square_land_on(self):
        jail_square = GoJailSquare("Go to Jail", 10)
        player = Player("Alice")
        with patch("builtins.print") as mocked_print:
            jail_square.land_on(player)
            self.assertTrue(player.in_jail)
            mocked_print.assert_called_with("Alice landed on Jail and is sent to In Jail Square.")

    def test_in_jail_square_land_on(self):
        jail_square = InJailSqaure("In Jail", 11)
        player = Player("Alice", in_jail=True)
        with patch("builtins.print") as mocked_print:
            jail_square.land_on(player)
            self.assertEqual(player.jail_turns, 1)
            mocked_print.assert_called_with("Alice is in Jail for 1 times")


class TestBoard(unittest.TestCase):
    @patch("board.csv.DictReader")
    def test_board_load_from_csv(self, mock_csv_reader):
        mock_csv_reader.return_value = [
            {"position": "0", "name": "Go", "price": "", "rent": ""},
            {"position": "1", "name": "Baltic Avenue", "price": "100", "rent": "10"},
            {"position": "2", "name": "Income Tax", "price": "", "rent": ""},
        ]
        board = Board(csv_file="mock.csv")
        self.assertEqual(len(board.squares), 3)
        self.assertIsInstance(board.squares[0], Square)
        self.assertIsInstance(board.squares[1], PropertySquare)
        self.assertIsInstance(board.squares[2], TaxSquare)

    def test_board_move_player(self):
        squares = [Square("Go", 0), Square("Park Place", 1)]
        board = Board(squares=squares)
        player = Player("Alice", position=0)
        with patch("builtins.print") as mocked_print:
            board.move_player(player, 1)
            self.assertEqual(player.position, 1)
            mocked_print.assert_called_with("Alice moved to Park Place.")

    def test_board_resolve_square(self):
        square_mock = MagicMock()
        square_mock.name = "Chance"
        square_mock.land_on = MagicMock()
        board = Board(squares=[square_mock])
        player = Player("Alice")
        board.resolve_square(player)
        square_mock.land_on.assert_called_once_with(player)


class TestGameboardDesigner(unittest.TestCase):
    @patch("builtins.input", side_effect=["mock_board.csv", "done"])
    @patch("builtins.print")
    @patch("gameboardDesign.open", new_callable=mock_open, read_data="position,name,price,rent\n0,Go,,\n1,Baltic Avenue,100,10\n")
    def test_load_and_modify_gameboard(self, mock_open_file, mock_print, mock_input):
        designer = GameboardDesigner()
        designer.load_and_modify_gameboard()
        mock_print.assert_any_call("\nGameboard loaded successfully!")

    @patch("builtins.input", side_effect=["mock_board.csv", "1", "Property", "New Property", "500", "50", "done"])
    @patch("builtins.print")
    @patch("gameboardDesign.open", new_callable=mock_open, read_data="position,name,price,rent\n0,Go,,\n1,Baltic Avenue,100,10\n")
    def test_modify_property_square(self, mock_open_file, mock_print, mock_input):
        designer = GameboardDesigner()
        designer.load_and_modify_gameboard()
        mock_print.assert_any_call("Gameboard modified and saved successfully!")


if __name__ == "__main__":
    unittest.main()