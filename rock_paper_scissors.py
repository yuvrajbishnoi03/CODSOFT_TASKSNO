"""
Rock-Paper-Scissors Game
=========================
A simple, interactive command-line game where you play against the computer.

Rules:
    Rock beats Scissors
    Scissors beats Paper
    Paper beats Rock
"""

import random

CHOICES = ["rock", "paper", "scissors"]
SHORTCUTS = {"r": "rock", "p": "paper", "s": "scissors"}

# key beats value
BEATS = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
}

EMOJI = {
    "rock": "🪨",
    "paper": "📄",
    "scissors": "✂️",
}


def print_header():
    print("=" * 42)
    print("     ROCK  •  PAPER  •  SCISSORS")
    print("=" * 42)
    print("Enter 'rock', 'paper', or 'scissors'")
    print("(shortcuts 'r', 'p', 's' also work).")
    print("Type 'quit' at any time to exit.\n")


def get_user_choice():
    """Prompt the user for a choice, validating input until it's usable."""
    while True:
        user_input = input("Your choice: ").strip().lower()

        if user_input in ("quit", "exit", "q"):
            return None
        if user_input in SHORTCUTS:
            return SHORTCUTS[user_input]
        if user_input in CHOICES:
            return user_input

        print("Invalid input. Please enter rock, paper, scissors (or r/p/s).\n")


def get_computer_choice():
    """Generate a random choice for the computer."""
    return random.choice(CHOICES)


def determine_winner(user, computer):
    """Return 'user', 'computer', or 'tie' based on the game rules."""
    if user == computer:
        return "tie"
    if BEATS[user] == computer:
        return "user"
    return "computer"


def display_round(user, computer, winner):
    print(f"\nYou chose:      {user.capitalize():<10} {EMOJI[user]}")
    print(f"Computer chose: {computer.capitalize():<10} {EMOJI[computer]}")
    print("-" * 42)

    if winner == "tie":
        print("It's a TIE! 🤝")
    elif winner == "user":
        print("You WIN this round! 🎉")
    else:
        print("Computer WINS this round! 💻")
    print("-" * 42)


def display_score(user_score, computer_score, ties):
    print(f"\nSCORE  ->  You: {user_score}   Computer: {computer_score}   Ties: {ties}\n")


def ask_play_again():
    while True:
        answer = input("Play again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def display_final_results(user_score, computer_score, ties):
    print("\n" + "=" * 42)
    print("FINAL SCORE")
    print(f"You: {user_score}   Computer: {computer_score}   Ties: {ties}")

    if user_score > computer_score:
        print("🏆 You are the overall winner! 🏆")
    elif computer_score > user_score:
        print("💻 Computer wins overall. Better luck next time!")
    else:
        print("🤝 Overall, it's a tie!")
    print("=" * 42)


def main():
    print_header()

    user_score = 0
    computer_score = 0
    ties = 0
    round_number = 1

    while True:
        print(f"--- Round {round_number} ---")
        user_choice = get_user_choice()

        if user_choice is None:
            print("\nThanks for playing!")
            break

        computer_choice = get_computer_choice()
        winner = determine_winner(user_choice, computer_choice)

        if winner == "user":
            user_score += 1
        elif winner == "computer":
            computer_score += 1
        else:
            ties += 1

        display_round(user_choice, computer_choice, winner)
        display_score(user_score, computer_score, ties)

        if not ask_play_again():
            print("\nThanks for playing!")
            break

        round_number += 1
        print()

    display_final_results(user_score, computer_score, ties)


if __name__ == "__main__":
    main()
