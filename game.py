import random
import json
from model.board import Board
from model.player import Player
import os

def main():
    print("Welcome to Monopoly!")
    
    # Initialize or load the game
    board, players = initialize_game()
    current_round = 1

    # Game loop
    while current_round <= 100 and len(players) > 1:
        print(f"\n--- Round {current_round} ---")
        visualize_gameboard(board, players)
        print_all_players_status(players)
        for player in players[:]:
            if player.money < 0:
                print(f"{player.name} is bankrupt and has retired from the game.")
                players.remove(player)
                continue
            
            if len(players) == 1:
                break
            
            print(f"\n{player.name}'s turn:")
            if prompt_save_game(board, players, player):
                print("Game saved. Exiting...")
                return
            if player.in_jail:
                handle_jail(player)
            else:
                take_turn(player, board)
        
        current_round += 1
    
    # Determine winner(s)
    print("\nGame Over!")
    if len(players) == 1:
        print(f"The winner is {players[0].name}!")
    else:
        print("Game ended after 100 rounds. Final standings:")
        for player in sorted(players, key=lambda p: p.money, reverse=True):
            print(f"{player.name}: ${player.money}")
    
    save_game(board, players)

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
                    name = input(f"Enter name for player {i + 1}: ")
                    players.append(Player(name))
                return players
            else:
                print("Invalid number of players. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def prompt_save_game(board, players, current_player):
    choice = input(f"{current_player.name}, would you like to save the game and exit? (y/n): ").lower()
    if choice == 'y':
        save_game(board, players)
        return True
    return False

def take_turn(player, board):
    input(f"{player.name}, press Enter to roll the dice.")
    dice = roll_dice()
    print(f"You rolled {dice[0]} and {dice[1]}.")
    steps = sum(dice)
    board.move_player(player, steps)
    board.resolve_square(player)

def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def handle_jail(player):
    if player.jail_turns == 3 or player.pay_jail_fine():
        player.release_from_jail()
        print(f"{player.name} is out of jail.")
    else:
        print(f"{player.name} remains in jail.")
        
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
        "board": board.to_dict(),
        "players": [player.to_dict() for player in players]
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
