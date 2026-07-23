#!/usr/bin/env python3
"""
Simple Calculator - GUI Application
=====================================

A professional, modern GUI calculator built with Python's Tkinter library.
Developed as part of the Codveda Python Development Internship.

Features:
    - Addition, Subtraction, Multiplication, Division
    - Modulus, Power, Square Root, Percentage
    - Dark, modern themed interface
    - Full input validation and error handling
    - Division-by-zero and invalid-input protection via messagebox alerts

Author: Codveda Python Development Intern
"""

import tkinter as tk
from tkinter import messagebox
import math


class CalculatorApp:
    """
    A modern, dark-themed GUI calculator application.

    This class encapsulates the entire calculator: the Tkinter window,
    the display, the button grid, and all arithmetic logic. Keeping
    everything inside a single class avoids relying on global state and
    keeps the widget layout and business logic cleanly organized.
    """

    # ------------------------------------------------------------------
    # Color palette and fonts (centralized for easy theming)
    # ------------------------------------------------------------------
    BG_COLOR = "#1e1e2e"          # Window background
    DISPLAY_BG = "#11111b"        # Display field background
    DISPLAY_FG = "#f5f5f5"        # Display text color
    BTN_NUM_BG = "#313244"        # Number button background
    BTN_NUM_FG = "#000000"        # Number button text
    BTN_OP_BG = "#89b4fa"         # Operator button background
    BTN_OP_FG = "#1e1e2e"         # Operator button text
    BTN_SPECIAL_BG = "#f38ba8"    # Clear / Exit button background
    BTN_SPECIAL_FG = "#1e1e2e"    # Clear / Exit button text
    BTN_EQUAL_BG = "#a6e3a1"      # Equals button background
    BTN_EQUAL_FG = "#1e1e2e"      # Equals button text
    BTN_ACTIVE_BG = "#585b70"     # Generic active/hover background

    FONT_DISPLAY = ("Consolas", 28, "bold")
    FONT_BUTTON = ("Segoe UI", 14, "bold")
    FONT_TITLE = ("Segoe UI", 16, "bold")

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the calculator window and all its widgets.

        Args:
            root: The root Tkinter window supplied by the caller.
        """
        self.root = root
        self._configure_window()

        # Holds the current expression being built by the user.
        self.expression: str = ""

        # StringVar bound to the display entry widget.
        self.display_var = tk.StringVar(value="0")

        self._build_title_bar()
        self._build_display()
        self._build_buttons()

    # ----------------------------------------------------------------
    # Window / layout setup
    # ----------------------------------------------------------------
    def _configure_window(self) -> None:
        """Configure root window properties: title, size, theme, icon."""
        self.root.title("Codveda | Simple Calculator")
        self.root.geometry("380x560")
        self.root.minsize(340, 520)
        self.root.configure(bg=self.BG_COLOR)

        # Center the window on the screen for a polished first impression.
        self.root.update_idletasks()
        width = 380
        height = 560
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Make the grid responsive so the layout adapts on resize.
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def _build_title_bar(self) -> None:
        """Create a simple header/title label for branding."""
        title_label = tk.Label(
            self.root,
            text="Simple Calculator",
            font=self.FONT_TITLE,
            bg=self.BG_COLOR,
            fg=self.BTN_OP_BG,
            pady=12,
        )
        title_label.grid(row=0, column=0, sticky="ew")

    def _build_display(self) -> None:
        """Create the read-only display where expressions/results appear."""
        display_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        display_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        display_frame.grid_columnconfigure(0, weight=1)

        self.display_entry = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=self.FONT_DISPLAY,
            bg=self.DISPLAY_BG,
            fg=self.DISPLAY_FG,
            insertbackground=self.DISPLAY_FG,
            justify="right",
            bd=0,
            relief="flat",
            state="readonly",
            readonlybackground=self.DISPLAY_BG,
        )
        self.display_entry.grid(row=0, column=0, sticky="ew", ipady=18, padx=4)

    def _build_buttons(self) -> None:
        """Create and place all calculator buttons in a responsive grid."""
        buttons_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        buttons_frame.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))

        # Make every column/row expand evenly -> responsive buttons.
        for col in range(4):
            buttons_frame.grid_columnconfigure(col, weight=1)
        for row in range(6):
            buttons_frame.grid_rowconfigure(row, weight=1)

        # Layout definition: (label, row, col, colspan, button_type)
        # button_type controls the color scheme applied to the button.
        layout = [
            ("C", 0, 0, 1, "special"),
            ("%", 0, 1, 1, "op"),
            ("√", 0, 2, 1, "op"),
            ("÷", 0, 3, 1, "op"),

            ("7", 1, 0, 1, "num"),
            ("8", 1, 1, 1, "num"),
            ("9", 1, 2, 1, "num"),
            ("×", 1, 3, 1, "op"),

            ("4", 2, 0, 1, "num"),
            ("5", 2, 1, 1, "num"),
            ("6", 2, 2, 1, "num"),
            ("-", 2, 3, 1, "op"),

            ("1", 3, 0, 1, "num"),
            ("2", 3, 1, 1, "num"),
            ("3", 3, 2, 1, "num"),
            ("+", 3, 3, 1, "op"),

            ("^", 4, 0, 1, "op"),
            ("0", 4, 1, 1, "num"),
            (".", 4, 2, 1, "num"),
            ("mod", 4, 3, 1, "op"),

            ("Exit", 5, 0, 2, "special"),
            ("=", 5, 2, 2, "equal"),
        ]

        for (text, row, col, colspan, kind) in layout:
            self._create_button(buttons_frame, text, row, col, colspan, kind)

    def _create_button(
        self,
        parent: tk.Frame,
        text: str,
        row: int,
        col: int,
        colspan: int,
        kind: str,
    ) -> None:
        """
        Create a single styled button and place it on the grid.

        Args:
            parent: The frame that will contain the button.
            text: The label displayed on the button.
            row: Grid row index.
            col: Grid column index.
            colspan: Number of columns the button should span.
            kind: One of 'num', 'op', 'special', 'equal' -> controls color.
        """
        color_map = {
            "num": (self.BTN_NUM_BG, self.BTN_NUM_FG),
            "op": (self.BTN_OP_BG, self.BTN_OP_FG),
            "special": (self.BTN_SPECIAL_BG, self.BTN_SPECIAL_FG),
            "equal": (self.BTN_EQUAL_BG, self.BTN_EQUAL_FG),
        }
        bg_color, fg_color = color_map.get(kind, (self.BTN_NUM_BG, self.BTN_NUM_FG))

        button = tk.Button(
            parent,
            text=text,
            font=self.FONT_BUTTON,
            bg=bg_color,
            fg=fg_color,
            activebackground=self.BTN_ACTIVE_BG,
            activeforeground=self.DISPLAY_FG,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=lambda t=text: self._on_button_click(t),
        )
        button.grid(
            row=row,
            column=col,
            columnspan=colspan,
            sticky="nsew",
            padx=6,
            pady=6,
            ipady=10,
        )

    # ----------------------------------------------------------------
    # Event handling
    # ----------------------------------------------------------------
    def _on_button_click(self, key: str) -> None:
        """
        Route a button press to the appropriate handler.

        Args:
            key: The text of the button that was pressed.
        """
        if key == "C":
            self._clear()
        elif key == "Exit":
            self._exit_app()
        elif key == "=":
            self._calculate()
        elif key == "√":
            self._square_root()
        elif key == "%":
            self._percentage()
        else:
            self._append_to_expression(key)

    def _append_to_expression(self, value: str) -> None:
        """
        Append a digit or operator symbol to the current expression.

        Args:
            value: The character/symbol to append (e.g. '5', '+', '×').
        """
        # Translate display symbols into Python-evaluable operators.
        symbol_map = {"×": "*", "÷": "/", "^": "**", "mod": "%"}
        self.expression += symbol_map.get(value, value)
        self._update_display(self.expression)

    def _update_display(self, text: str) -> None:
        """Update the on-screen display with the given text."""
        # Show '0' when the expression is empty, otherwise show as typed.
        self.display_var.set(text if text else "0")

    def _clear(self) -> None:
        """Reset the calculator to its initial empty state."""
        self.expression = ""
        self._update_display("0")

    def _exit_app(self) -> None:
        """Prompt for confirmation and close the application."""
        if messagebox.askyesno("Exit Calculator", "Are you sure you want to exit?"):
            self.root.destroy()

    # ----------------------------------------------------------------
    # Arithmetic logic
    # ----------------------------------------------------------------
    def _calculate(self) -> None:
        """
        Evaluate the current expression and display the result.

        Handles division/modulus by zero and malformed expressions
        gracefully, alerting the user via a messagebox rather than
        crashing the application.
        """
        if not self.expression:
            messagebox.showwarning("Input Required", "Please enter an expression first.")
            return

        try:
            # A restricted eval: only digits, operators and parentheses
            # are permitted in self.expression because _append_to_expression
            # only ever adds validated symbols, so this is safe in context.
            result = eval(self.expression, {"__builtins__": {}}, {})

            if isinstance(result, complex):
                raise ValueError("Result is not a real number.")

            # Round floating point noise, then present as int when whole.
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            else:
                result = round(result, 8)

            self._update_display(str(result))
            self.expression = str(result)

        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Cannot divide by zero.")
            self._clear()
        except (SyntaxError, TypeError, ValueError):
            messagebox.showerror("Invalid Expression", "Please check your input and try again.")
            self._clear()
        except OverflowError:
            messagebox.showerror("Overflow Error", "The result is too large to display.")
            self._clear()

    def _square_root(self) -> None:
        """
        Compute the square root of the current expression's value.

        Displays an error popup if the value is negative (no real square
        root) or if the expression is invalid/empty.
        """
        if not self.expression:
            messagebox.showwarning("Input Required", "Please enter a number first.")
            return

        try:
            value = eval(self.expression, {"__builtins__": {}}, {})
            if value < 0:
                raise ValueError("Cannot compute square root of a negative number.")

            result = math.sqrt(value)
            result = int(result) if result.is_integer() else round(result, 8)

            self._update_display(str(result))
            self.expression = str(result)

        except ValueError as error:
            messagebox.showerror("Math Error", str(error))
            self._clear()
        except (SyntaxError, TypeError, ZeroDivisionError):
            messagebox.showerror("Invalid Expression", "Please check your input and try again.")
            self._clear()

    def _percentage(self) -> None:
        """
        Convert the current expression's value into a percentage (value / 100).

        Displays an error popup if the expression cannot be evaluated.
        """
        if not self.expression:
            messagebox.showwarning("Input Required", "Please enter a number first.")
            return

        try:
            value = eval(self.expression, {"__builtins__": {}}, {})
            result = value / 100
            result = int(result) if float(result).is_integer() else round(result, 8)

            self._update_display(str(result))
            self.expression = str(result)

        except (SyntaxError, TypeError, ZeroDivisionError):
            messagebox.showerror("Invalid Expression", "Please check your input and try again.")
            self._clear()


def main() -> None:
    """Application entry point."""
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
