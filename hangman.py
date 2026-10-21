#!/usr/bin/env python3
"""A console-based Hangman game.

Place google-10000-english-no-swears.txt in the same folder as this file
to use the supplied word list. If it is missing, a built-in list is used.
"""

from pathlib import Path
import random
import string

MAX_MISTAKES = 6
WORD_LIST_FILE = Path(__file__).with_name("google-10000-english-no-swears.txt")

HANGMAN_STAGES = [
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========""",
]


def load_words():
    """Load usable words from the provided text file, or use a fallback list."""
    fallback_words = [
        "python", "computer", "hangman", "keyboard", "program",
        "developer", "function", "variable", "internet", "science",
        "college", "student", "project", "software", "algorithm",
    ]

    try:
        words = [
            line.strip().lower()
            for line in WORD_LIST_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip().isalpha() and 4 <= len(line.strip()) <= 12
        ]
        if words:
            return words
    except OSError:
        pass

    return fallback_words


def display_game(secret_word, guessed_letters, mistakes):
    """Print the current gallows, masked word, and guessed letters."""
    print(HANGMAN_STAGES[mistakes])
    masked_word = " ".join(
        letter if letter in guessed_letters else "_" for letter in secret_word
    )
    print(f"\nWord: {masked_word}")
    print(f"Mistakes remaining: {MAX_MISTAKES - mistakes}")
    if guessed_letters:
        print("Guessed letters: " + " ".join(sorted(guessed_letters)))
    else:
        print("Guessed letters: (none)")
    print()


def play_game():
    secret_word = random.choice(load_words())
    guessed_letters = set()
    mistakes = 0

    print("=" * 42)
    print("           HANGMAN WORD GAME")
    print("=" * 42)
    print(f"Guess the hidden word one letter at a time. You have {MAX_MISTAKES} wrong guesses.")
    print("Enter 'quit' at any time to leave the game.\n")

    while mistakes < MAX_MISTAKES:
        display_game(secret_word, guessed_letters, mistakes)

        if all(letter in guessed_letters for letter in secret_word):
            print(f"You win! The word was: {secret_word.upper()}")
            return

        guess = input("Enter a letter: ").strip().lower()

        if guess in {"quit", "exit"}:
            print(f"Game ended. The word was: {secret_word.upper()}")
            return

        if len(guess) != 1 or guess not in string.ascii_lowercase:
            print("Invalid input. Please enter one English letter (A-Z).\n")
            continue

        if guess in guessed_letters:
            print(f"You already guessed '{guess.upper()}'. No penalty applied.\n")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"Correct! '{guess.upper()}' is in the word.\n")
        else:
            mistakes += 1
            print(f"Sorry, '{guess.upper()}' is not in the word.\n")

    display_game(secret_word, guessed_letters, mistakes)
    print(f"Game over! You ran out of attempts. The word was: {secret_word.upper()}")


def main():
    while True:
        play_game()
        again = input("\nWould you like to play again? (y/n): ").strip().lower()
        if again not in {"y", "yes"}:
            print("Thanks for playing Hangman. Goodbye!")
            break
        print()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted. Goodbye!")
