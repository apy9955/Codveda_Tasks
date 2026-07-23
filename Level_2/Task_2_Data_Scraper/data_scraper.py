#!/usr/bin/env python3
"""
Codveda | Data Scraper
=======================

A professional, dark-themed desktop GUI application for scraping heading
text (h1, h2, h3) from a given website URL, previewing the results in a
table, and exporting them to a CSV file.

Modules used:
    - tkinter / tkinter.ttk / tkinter.messagebox : GUI framework
    - requests                                    : HTTP requests
    - bs4 (BeautifulSoup)                         : HTML parsing
    - pandas                                      : CSV export

Author: Codveda
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup


class DataScraperApp:
    """
    Main application class for the Codveda Data Scraper.

    This class builds and manages the Tkinter GUI, handles user
    interaction (Scrape / Save CSV / Clear / Exit), performs the
    web-scraping logic, and manages the in-memory scraped dataset.
    """

    # ----------------------------- THEME ------------------------------ #
    BG_COLOR = "#1e1e2e"
    SECONDARY_BG = "#27293d"
    ACCENT_COLOR = "#7c3aed"
    ACCENT_HOVER = "#9333ea"
    TEXT_COLOR = "#e4e4e7"
    SUBTEXT_COLOR = "#9ca3af"
    ENTRY_BG = "#313244"
    SUCCESS_COLOR = "#22c55e"
    ERROR_COLOR = "#ef4444"

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the application, configure the window, and build the UI.

        Args:
            root: The root Tkinter window instance.
        """
        self.root = root
        self.scraped_data: list[dict[str, str]] = []  # Holds scraped rows

        self._configure_window()
        self._configure_styles()
        self._build_ui()

    # ------------------------------------------------------------------ #
    # WINDOW / STYLE CONFIGURATION
    # ------------------------------------------------------------------ #
    def _configure_window(self) -> None:
        """Set up the main window title, size, and background color."""
        self.root.title("Codveda | Data Scraper")
        self.root.geometry("900x600")
        self.root.minsize(760, 520)
        self.root.configure(bg=self.BG_COLOR)

    def _configure_styles(self) -> None:
        """Configure ttk styles to achieve a modern dark theme look."""
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # Treeview styling
        style.configure(
            "Treeview",
            background=self.SECONDARY_BG,
            foreground=self.TEXT_COLOR,
            fieldbackground=self.SECONDARY_BG,
            rowheight=28,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=self.ACCENT_COLOR,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        style.map(
            "Treeview",
            background=[("selected", self.ACCENT_HOVER)],
            foreground=[("selected", "white")],
        )

        # Scrollbar styling
        style.configure(
            "Vertical.TScrollbar",
            background=self.SECONDARY_BG,
            troughcolor=self.BG_COLOR,
            bordercolor=self.BG_COLOR,
            arrowcolor=self.TEXT_COLOR,
        )

    # ------------------------------------------------------------------ #
    # UI CONSTRUCTION
    # ------------------------------------------------------------------ #
    def _build_ui(self) -> None:
        """Construct and place all widgets in the main window."""
        self._build_header()
        self._build_input_bar()
        self._build_results_table()
        self._build_status_bar()
        self._build_action_buttons()

    def _build_header(self) -> None:
        """Create the title/header section of the app."""
        header_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        header_frame.pack(fill="x", padx=20, pady=(18, 6))

        title_label = tk.Label(
            header_frame,
            text="Codveda Data Scraper",
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            font=("Segoe UI", 18, "bold"),
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            header_frame,
            text="Extract page headings (h1, h2, h3) from any website",
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
            font=("Segoe UI", 10),
        )
        subtitle_label.pack(anchor="w")

    def _build_input_bar(self) -> None:
        """Create the URL entry field and the Scrape button row."""
        input_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        input_frame.pack(fill="x", padx=20, pady=10)

        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(
            input_frame,
            textvariable=self.url_var,
            font=("Segoe UI", 11),
            bg=self.ENTRY_BG,
            fg=self.TEXT_COLOR,
            insertbackground=self.TEXT_COLOR,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.SECONDARY_BG,
            highlightcolor=self.ACCENT_COLOR,
        )
        self.url_entry.insert(0, "https://example.com")
        self.url_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.url_entry.bind("<Return>", lambda _event: self.scrape_website())

        scrape_btn = self._make_button(
            input_frame, "🔍  Scrape", self.scrape_website, self.ACCENT_COLOR
        )
        scrape_btn.pack(side="left", ipadx=10, ipady=6)

    def _build_results_table(self) -> None:
        """Create the Treeview widget used to display scraped headings."""
        table_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        columns = ("tag", "text")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )
        self.tree.heading("tag", text="Tag")
        self.tree.heading("text", text="Heading Text")
        self.tree.column("tag", width=80, anchor="center")
        self.tree.column("text", width=700, anchor="w")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _build_status_bar(self) -> None:
        """Create a status label to show live feedback to the user."""
        self.status_var = tk.StringVar(value="Ready. Enter a URL and click Scrape.")
        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
            font=("Segoe UI", 9),
            anchor="w",
        )
        status_label.pack(fill="x", padx=22, pady=(0, 6))

    def _build_action_buttons(self) -> None:
        """Create the bottom action bar with Save CSV, Clear, and Exit."""
        button_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        button_frame.pack(fill="x", padx=20, pady=(0, 18))

        save_btn = self._make_button(
            button_frame, "💾  Save CSV", self.save_to_csv, self.SUCCESS_COLOR
        )
        save_btn.pack(side="left", ipadx=10, ipady=6, padx=(0, 10))

        clear_btn = self._make_button(
            button_frame, "🧹  Clear", self.clear_results, self.SECONDARY_BG
        )
        clear_btn.pack(side="left", ipadx=10, ipady=6, padx=(0, 10))

        exit_btn = self._make_button(
            button_frame, "🚪  Exit", self.exit_app, self.ERROR_COLOR
        )
        exit_btn.pack(side="right", ipadx=10, ipady=6)

    def _make_button(
        self, parent: tk.Widget, text: str, command, bg_color: str
    ) -> tk.Button:
        """
        Create a styled flat button consistent with the dark theme.

        Args:
            parent: Parent widget to attach the button to.
            text: Button label text.
            command: Callback function to invoke on click.
            bg_color: Background color for the button.

        Returns:
            The configured tk.Button instance (not yet packed/gridded).
        """
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg="white",
            activebackground=self.ACCENT_HOVER,
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
        )

    # ------------------------------------------------------------------ #
    # CORE LOGIC
    # ------------------------------------------------------------------ #
    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """
        Validate that a URL has a proper scheme and network location.

        Args:
            url: The URL string to validate.

        Returns:
            True if the URL appears valid, False otherwise.
        """
        try:
            result = urlparse(url)
            return all([result.scheme in ("http", "https"), result.netloc])
        except ValueError:
            return False

    def scrape_website(self) -> None:
        """
        Fetch the entered URL, parse its HTML, and extract heading tags
        (h1, h2, h3). Populates the Treeview with results and shows
        success/error messages as appropriate.
        """
        url = self.url_var.get().strip()

        if not url:
            messagebox.showerror("Input Error", "Please enter a website URL.")
            return

        if not self._is_valid_url(url):
            messagebox.showerror(
                "Invalid URL",
                "The URL entered is invalid.\n"
                "Please include the scheme, e.g. https://example.com",
            )
            return

        self.status_var.set("Fetching page, please wait...")
        self.root.update_idletasks()

        try:
            headers = {"User-Agent": "Mozilla/5.0 (Codveda Data Scraper)"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.MissingSchema:
            messagebox.showerror("Invalid URL", "The URL is missing http:// or https://")
            self.status_var.set("Failed: invalid URL.")
            return
        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "Connection Error",
                "Could not connect to the website. Check your internet "
                "connection or the URL and try again.",
            )
            self.status_var.set("Failed: connection error.")
            return
        except requests.exceptions.Timeout:
            messagebox.showerror("Timeout Error", "The request timed out. Please try again.")
            self.status_var.set("Failed: request timed out.")
            return
        except requests.exceptions.HTTPError as http_err:
            messagebox.showerror("HTTP Error", f"Server returned an error:\n{http_err}")
            self.status_var.set("Failed: HTTP error.")
            return
        except requests.exceptions.RequestException as err:
            messagebox.showerror("Request Error", f"An unexpected error occurred:\n{err}")
            self.status_var.set("Failed: request error.")
            return

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            headings = soup.find_all(["h1", "h2", "h3"])
        except Exception as parse_err:  # noqa: BLE001 - surfacing to user
            messagebox.showerror("Parsing Error", f"Failed to parse HTML:\n{parse_err}")
            self.status_var.set("Failed: parsing error.")
            return

        self.clear_results(show_confirm=False)

        for tag in headings:
            text = tag.get_text(strip=True)
            if text:
                self.scraped_data.append({"tag": tag.name.upper(), "text": text})
                self.tree.insert("", "end", values=(tag.name.upper(), text))

        if not self.scraped_data:
            messagebox.showinfo(
                "No Headings Found",
                "The page was fetched successfully, but no h1/h2/h3 "
                "headings were found.",
            )
            self.status_var.set("No headings found on this page.")
            return

        self.status_var.set(f"Scraped {len(self.scraped_data)} heading(s) from {url}")
        messagebox.showinfo(
            "Success", f"Successfully scraped {len(self.scraped_data)} heading(s)."
        )

    def save_to_csv(self) -> None:
        """
        Export the currently scraped data to a CSV file using pandas.
        Prompts the user with a save dialog to choose the file location.
        """
        if not self.scraped_data:
            messagebox.showwarning(
                "No Data", "There is no scraped data to save. Please scrape a website first."
            )
            return

        from tkinter import filedialog  # Local import: only needed here

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="scraped_data.csv",
            title="Save Scraped Data As",
        )

        if not file_path:
            return  # User cancelled the dialog

        try:
            dataframe = pd.DataFrame(self.scraped_data)
            dataframe.to_csv(file_path, index=False, encoding="utf-8")
        except (OSError, PermissionError) as file_err:
            messagebox.showerror("Save Error", f"Could not save file:\n{file_err}")
            self.status_var.set("Failed to save CSV.")
            return

        self.status_var.set(f"Data saved to {file_path}")
        messagebox.showinfo("Success", f"Data successfully saved to:\n{file_path}")

    def clear_results(self, show_confirm: bool = True) -> None:
        """
        Clear the Treeview results and the internal scraped data list.

        Args:
            show_confirm: Whether to display a confirmation message box.
                Set to False when clearing is done internally before a
                fresh scrape (no need to notify the user twice).
        """
        self.tree.delete(*self.tree.get_children())
        self.scraped_data.clear()
        self.status_var.set("Results cleared. Ready for a new scrape.")

        if show_confirm:
            messagebox.showinfo("Cleared", "All results have been cleared.")

    def exit_app(self) -> None:
        """Prompt for confirmation and close the application."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


def main() -> None:
    """Application entry point: create the root window and run the app."""
    root = tk.Tk()
    DataScraperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
