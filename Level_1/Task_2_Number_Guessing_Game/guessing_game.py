"""
Codveda | Number Guessing Game
--------------------------------
A modern, dark-themed GUI Number Guessing Game built with Tkinter.

The computer picks a random number between 1 and 100, and the user
tries to guess it. The app gives feedback (Too High / Too Low / Correct!),
tracks the number of attempts, validates input, and never crashes on
bad input.

Author: Codveda
"""

import tkinter as tk
from tkinter import font as tkfont
import random


class NumberGuessingGame:
    """
    Object-oriented implementation of the Number Guessing Game.
    Encapsulates all game state and UI widgets inside the class.
    """

    # ---- Color palette (modern dark theme) ----
    BG_COLOR = "#1e1e2f"          # main window background
    CARD_COLOR = "#27293d"        # card/panel background
    ACCENT_COLOR = "#7f5af0"      # purple accent
    ACCENT_HOVER = "#9b7cf5"      # lighter purple for hover
    SUCCESS_COLOR = "#2cb67d"     # green for correct guess
    ERROR_COLOR = "#ff5470"       # red/pink for errors & exit
    WARNING_COLOR = "#ff8906"     # orange for too high/low
    TEXT_COLOR = "#A22B2B"        # near-white text
    SUBTEXT_COLOR = "#a7a9be"     # muted text for hints

    def __init__(self, root):
        self.root = root
        self.root.title("Codveda | Number Guessing Game")
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)

        # ---- Game state ----
        self.min_range = 1
        self.max_range = 100
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0

        # ---- Fonts ----
        self.title_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=10)
        self.entry_font = tkfont.Font(family="Segoe UI", size=14)
        self.button_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.message_font = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.attempts_font = tkfont.Font(family="Segoe UI", size=10)

        self._build_ui()
        self._center_window(420, 480)

    # ------------------------------------------------------------------
    # UI CONSTRUCTION
    # ------------------------------------------------------------------
    def _build_ui(self):
        """Builds and lays out all widgets in the window."""

        # Main card/container frame for a clean, modern look
        card = tk.Frame(self.root, bg=self.CARD_COLOR, padx=30, pady=30)
        card.pack(expand=True, fill="both", padx=20, pady=20)

        # Title label
        title_label = tk.Label(
            card,
            text="🎯 Number Guessing Game",
            font=self.title_font,
            bg=self.CARD_COLOR,
            fg=self.TEXT_COLOR,
        )
        title_label.pack(pady=(0, 5))

        # Subtitle / instructions
        subtitle_label = tk.Label(
            card,
            text=f"Guess a number between {self.min_range} and {self.max_range}",
            font=self.subtitle_font,
            bg=self.CARD_COLOR,
            fg=self.SUBTEXT_COLOR,
        )
        subtitle_label.pack(pady=(0, 20))

        # Entry widget for user input
        self.guess_entry = tk.Entry(
            card,
            font=self.entry_font,
            justify="center",
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            insertbackground=self.TEXT_COLOR,  # cursor color
            relief="flat",
            highlightthickness=2,
            highlightbackground=self.ACCENT_COLOR,
            highlightcolor=self.ACCENT_COLOR,
        )
        self.guess_entry.pack(fill="x", ipady=8, pady=(0, 15))
        self.guess_entry.focus_set()
        # Allow pressing Enter to submit a guess
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        # Guess button
        self.guess_button = self._create_button(
            card, "Guess", self.ACCENT_COLOR, self.ACCENT_HOVER, self.check_guess
        )
        self.guess_button.pack(fill="x", pady=(0, 10))

        # Message label (Too High / Too Low / Correct! / errors)
        self.message_label = tk.Label(
            card,
            text="Make your first guess!",
            font=self.message_font,
            bg=self.CARD_COLOR,
            fg=self.SUBTEXT_COLOR,
            wraplength=340,
        )
        self.message_label.pack(pady=(10, 5))

        # Attempts counter label
        self.attempts_label = tk.Label(
            card,
            text="Attempts: 0",
            font=self.attempts_font,
            bg=self.CARD_COLOR,
            fg=self.SUBTEXT_COLOR,
        )
        self.attempts_label.pack(pady=(0, 20))

        # Frame to hold New Game and Exit buttons side by side
        button_row = tk.Frame(card, bg=self.CARD_COLOR)
        button_row.pack(fill="x")

        self.new_game_button = self._create_button(
            button_row, "New Game", self.SUCCESS_COLOR, "#3fd39a", self.new_game
        )
        self.new_game_button.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.exit_button = self._create_button(
            button_row, "Exit", self.ERROR_COLOR, "#ff7a91", self.exit_game
        )
        self.exit_button.pack(side="left", expand=True, fill="x", padx=(5, 0))

    def _create_button(self, parent, text, bg_color, hover_color, command):
        """
        Helper to create a styled flat button with a simple hover effect.
        Returns the created Button widget.
        """
        button = tk.Button(
            parent,
            text=text,
            font=self.button_font,
            bg=bg_color,
            fg=self.TEXT_COLOR,
            activebackground=hover_color,
            activeforeground=self.TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=command,
            pady=8,
        )
        # Bind hover events for a subtle interactive feel
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=bg_color))
        return button

    def _center_window(self, width, height):
        """Centers the main window on the user's screen."""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # ------------------------------------------------------------------
    # GAME LOGIC
    # ------------------------------------------------------------------
    def check_guess(self):
        """
        Reads the user's guess, validates it, compares it to the secret
        number, and updates the UI accordingly. Wrapped in error handling
        so invalid input never crashes the app.
        """
        raw_value = self.guess_entry.get().strip()

        # ---- Input validation ----
        if raw_value == "":
            self._show_message("Please enter a number!", self.ERROR_COLOR)
            return

        try:
            guess = int(raw_value)
        except ValueError:
            self._show_message("Invalid input — enter a whole number!", self.ERROR_COLOR)
            self.guess_entry.delete(0, tk.END)
            return

        if guess < self.min_range or guess > self.max_range:
            self._show_message(
                f"Enter a number between {self.min_range} and {self.max_range}!",
                self.ERROR_COLOR,
            )
            self.guess_entry.delete(0, tk.END)
            return

        # ---- Valid guess: process it ----
        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}")

        if guess < self.secret_number:
            self._show_message("📉 Too Low! Try again.", self.WARNING_COLOR)
        elif guess > self.secret_number:
            self._show_message("📈 Too High! Try again.", self.WARNING_COLOR)
        else:
            self._show_message(
                f"🎉 Correct! The number was {self.secret_number}. "
                f"Solved in {self.attempts} attempt(s)!",
                self.SUCCESS_COLOR,
            )
            # Disable further guessing until a new game starts
            self.guess_button.config(state="disabled")
            self.guess_entry.config(state="disabled")

        self.guess_entry.delete(0, tk.END)

    def _show_message(self, text, color):
        """Updates the feedback message label with new text and color."""
        self.message_label.config(text=text, fg=color)

    def new_game(self):
        """Resets the game state for a fresh round."""
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.attempts_label.config(text="Attempts: 0")
        self._show_message("New round started — good luck!", self.SUBTEXT_COLOR)

        # Re-enable input in case it was disabled after a win
        self.guess_entry.config(state="normal")
        self.guess_button.config(state="normal")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus_set()

    def exit_game(self):
        """Closes the application safely."""
        self.root.destroy()


def main():
    """Entry point: creates the root window and starts the Tkinter main loop."""
    root = tk.Tk()
    NumberGuessingGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
