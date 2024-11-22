import random
import json
import string
from model.board import Board
from model.player import Player
from model.gameboardDesign import GameboardDesigner
import os

def main():
    print("Welcome to Monopoly!")
    
    """Let the user select their role: Player or Gameboard Designer."""
    print("Select your role:\n1. Player - Play the game\n2. Gameboard Designer - Design or modify a gameboard")
    choice = input("Enter your choice (1 or 2): ").strip()
    if choice == "1":
        return play_game()
    elif choice == "2":
        return GameboardDesigner().start()
    else:
        print("Invalid choice. Please try again.")
        return main()
    

def play_game():
    """Play the game."""
    print("\n--- Game Start! ---")
    # Initialize or load the game
    board, players = initialize_game()
    current_round = 1

    # Game loop
    while current_round <= 100 and len(players) > 1:
        print(f"\n--- Round {current_round} ---")
        for player in players[:]:
            
            if len(players) == 1:
                break
            
            visualize_gameboard(board, players)
            print_all_players_status(players)
            print(f"\n{player.name}'s turn:")
            choice = player_turn_menu(player)
            if choice == 2:  # Stop and save the game
                save_game(board, players)
                print("Game saved. Exiting...")
                return
            
            if player.in_jail:
                handle_jail(player,board)
            else:
                take_turn(player, board)

            if player.money < 0:
                print(f"{player.name} is bankrupt and has retired from the game.")
                players.remove(player)
                continue
        
        current_round += 1
    
    # Determine winner(s)
    print("\nGame Over!")
    if len(players) == 1:
        print(f"The winner is {players[0].name}!")
    else:
        print("Game ended after 100 rounds. Final standings:")
        for player in sorted(players, key=lambda p: p.money, reverse=True):
            print(f"{player.name}: ${player.money}")

def initialize_game():
    choice = input("Do you want to load a saved game? (y/n): ").lower()
    if choice == 'y':
        return load_game()
    else:
        board = initialize_board()
        players = initialize_players()
        return board, players

def initialize_board():
    print("Choose a game board file from the available options:")
    csv_files = [f for f in os.listdir() if f.endswith('Board.csv')]
    
    if not csv_files:
        print("No CSV files found in the current directory. Exiting.")
        exit(1)
    
    for i, file in enumerate(csv_files):
        print(f"{i + 1}. {file}")
    
    while True:
        try:
            choice = int(input("Enter the number of the game board file to use: ")) - 1
            if 0 <= choice < len(csv_files):
                return Board(csv_files[choice])
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def initialize_players():
    while True:
        try:
            num_players = int(input("Enter the number of players (2-6): "))
            if 2<= num_players <=6:
                players = []
                for i in range(num_players):
                    name = input(f"Enter name for player {i + 1} or press Enter to randomly generate a name: ")
                    if len(name) == 0:
                        letters = string.ascii_lowercase
                        name = ''.join(random.choice(letters) for a in range(5))
                        print(f"Randomly generated name {name} for player {i+1}")
                    players.append(Player(name))
                return players
            else:
                print("Invalid number of players. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def player_turn_menu(player):
    while True:
        print("\nSelect an action:")
        print("1. Roll the dice")
        print("2. Stop and save the game")
        choice = input("Enter your choice (1 or 2): ")
        if choice in {'1', '2'}:
            return int(choice)
        print("Invalid choice. Please try again.")

def take_turn(player, board):
    dice = roll_dice()
    print(f"You rolled {dice[0]} and {dice[1]}.")
    steps = sum(dice)
    board.move_player(player, steps)
    board.resolve_square(player)

def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def handle_jail(player, board):
    if player.jail_turns == 3 :
        print(f"{player.name} has reached the third turn in jail. They must pay HKD 150 to get out.")
        if player.pay_jail_fine():
            print(f"{player.name} paid HKD 150.")
            player.release_from_jail()
            move_out_of_jail(player,board)
        else:
            print(f"{player.name} couldn't pay the fine and goes bankrupt.")
        

    else: 
        print(f"{player.name} is in jail (Turn {player.jail_turns + 1}/3).")
        print("Options:")
        print("1. Try to roll doubles to get out.")
        print("2. Pay HKD 150 to get out.")
        print("3. Remain In Jail.")

        choice = input("Enter 1 or 2 or 3: ").strip()
    if choice == "1":
        # Attempt to roll doubles
        dice = roll_dice()
        print(f"{player.name} rolled {dice[0]} and {dice[1]}.")
        if dice[0] == dice[1]:
            print(f"{player.name} rolled doubles and gets out of jail!")
            player.release_from_jail()
            move_out_of_jail(player,board, dice)
        else:
            print(f"{player.name} did not roll doubles and remains in jail.")
            player.jail_turns += 1

    elif choice == "2":
        # Pay the fine and move out of jail
        if player.pay_jail_fine():
            print(f"{player.name} paid HKD 150.")
            player.release_from_jail()
            move_out_of_jail(player,board)
        else:
            print(f"{player.name} couldn't pay the fine and goes bankrupt.")

    else:
        print("You remain in jail.")
        player.jail_turns += 1

def move_out_of_jail(player, board, dice=None,):
    """Handle movement for a player who gets out of jail."""
    if dice == None:
        dice = roll_dice()
    print(f"{player.name} rolled {dice[0]} and {dice[1]} to move forward.")
    board.move_player(player, sum(dice))
    board.resolve_square(player)
        
def visualize_gameboard(board, players):
    print("\n--- Game Board ---")
    for square in board.squares:
        player_markers = [player.name[0] for player in players if player.position == square.position]
        marker_str = ''.join(player_markers)
        print(f"[{square.name} - ${square.price if hasattr(square, 'price') else 'N/A'}] {marker_str}")

def print_all_players_status(players):
    print("\n--- Players Status ---")
    for player in players:
        print(f"{player.name} - Money: ${player.money}, Position: {player.position}, In Jail: {player.in_jail}")


def save_game(board, players):
    game_data = {
        "players": [player.to_dict() for player in players],
        "board": board.to_dict(),
    }
    with open('saved_game.json', 'w') as file:
        json.dump(game_data, file)
    print("Game saved successfully.")

def load_game():
    with open('saved_game.json', 'r') as file:
        game_data = json.load(file)
    board = Board.from_dict(game_data['board'])
    players = [Player.from_dict(p) for p in game_data['players']]
    print("Game loaded successfully.")
    return board, players

if __name__ == "__main__":
    main()
