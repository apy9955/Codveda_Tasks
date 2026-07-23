"""
Codveda | File Encryption & Decryption
========================================
A desktop application for encrypting and decrypting files using
symmetric encryption (Fernet, from the `cryptography` library).

Author: Codveda Internship Project
License: MIT
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from cryptography.fernet import Fernet, InvalidToken


# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
KEY_FILE = "key.key"

# Dark theme color palette
COLOR_BG = "#1e1e2e"
COLOR_BG_SECONDARY = "#27293d"
COLOR_FG = "#e0e0e0"
COLOR_ACCENT = "#4f8cff"
COLOR_ACCENT_HOVER = "#3b6fd9"
COLOR_SUCCESS = "#3fb950"
COLOR_DANGER = "#f85149"
COLOR_DANGER_HOVER = "#da3a32"
COLOR_ENTRY_BG = "#2b2d42"
COLOR_BORDER = "#3a3d5c"


class KeyManager:
    """Handles generation, storage, and retrieval of the Fernet key."""

    def __init__(self, key_path: str = KEY_FILE):
        self.key_path = key_path

    def key_exists(self) -> bool:
        """Check whether a key file already exists on disk."""
        return os.path.isfile(self.key_path)

    def generate_key(self) -> bytes:
        """Generate a new Fernet key and store it securely on disk."""
        key = Fernet.generate_key()
        with open(self.key_path, "wb") as key_file:
            key_file.write(key)
        return key

    def load_key(self) -> bytes:
        """Load the Fernet key from disk, generating one if it is missing."""
        if not self.key_exists():
            return self.generate_key()
        with open(self.key_path, "rb") as key_file:
            return key_file.read()


class FileEncryptorApp:
    """Main application class for the File Encryption & Decryption tool."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.key_manager = KeyManager()
        self.selected_file_path = tk.StringVar()

        self._configure_window()
        self._configure_styles()
        self._build_layout()

    # ----------------------------------------------------------------
    # Window / Style setup
    # ----------------------------------------------------------------
    def _configure_window(self) -> None:
        """Set up the main window: title, size, background, centering."""
        self.root.title("Codveda | File Encryption & Decryption")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        window_width, window_height = 560, 420
        self._center_window(window_width, window_height)

    def _center_window(self, width: int, height: int) -> None:
        """Center the application window on the user's screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _configure_styles(self) -> None:
        """Configure ttk styles for a modern dark theme look."""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TFrame",
            background=COLOR_BG,
        )
        style.configure(
            "Card.TFrame",
            background=COLOR_BG_SECONDARY,
        )
        style.configure(
            "TLabel",
            background=COLOR_BG,
            foreground=COLOR_FG,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Title.TLabel",
            background=COLOR_BG,
            foreground=COLOR_FG,
            font=("Segoe UI", 16, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=COLOR_BG,
            foreground="#9a9ab0",
            font=("Segoe UI", 9),
        )
        style.configure(
            "Path.TLabel",
            background=COLOR_ENTRY_BG,
            foreground=COLOR_FG,
            font=("Segoe UI", 9),
            padding=8,
        )

        # Generic accent button
        style.configure(
            "Accent.TButton",
            background=COLOR_ACCENT,
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=8,
            borderwidth=0,
        )
        style.map(
            "Accent.TButton",
            background=[("active", COLOR_ACCENT_HOVER)],
        )

        # Danger (exit) button
        style.configure(
            "Danger.TButton",
            background=COLOR_DANGER,
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=8,
            borderwidth=0,
        )
        style.map(
            "Danger.TButton",
            background=[("active", COLOR_DANGER_HOVER)],
        )

        # Neutral (secondary) button
        style.configure(
            "Neutral.TButton",
            background=COLOR_BORDER,
            foreground=COLOR_FG,
            font=("Segoe UI", 10),
            padding=8,
            borderwidth=0,
        )
        style.map(
            "Neutral.TButton",
            background=[("active", "#4a4d70")],
        )

    # ----------------------------------------------------------------
    # Layout
    # ----------------------------------------------------------------
    def _build_layout(self) -> None:
        """Build and place all widgets in the main window."""
        container = ttk.Frame(self.root, style="TFrame", padding=24)
        container.pack(fill="both", expand=True)

        # Header
        title_label = ttk.Label(
            container, text="File Encryption & Decryption", style="Title.TLabel"
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            container,
            text="Secure your files locally using Fernet (AES-based) encryption.",
            style="Subtitle.TLabel",
        )
        subtitle_label.pack(anchor="w", pady=(2, 20))

        # File selection card
        file_card = ttk.Frame(container, style="Card.TFrame", padding=16)
        file_card.pack(fill="x", pady=(0, 20))

        file_label = ttk.Label(
            file_card,
            text="Selected File:",
            background=COLOR_BG_SECONDARY,
            foreground=COLOR_FG,
            font=("Segoe UI", 10, "bold"),
        )
        file_label.pack(anchor="w", pady=(0, 8))

        self.path_display = ttk.Label(
            file_card,
            textvariable=self.selected_file_path,
            style="Path.TLabel",
            anchor="w",
            wraplength=480,
        )
        self.path_display.pack(fill="x", pady=(0, 12))
        self.selected_file_path.set("No file selected")

        browse_button = ttk.Button(
            file_card,
            text="📂  Browse File",
            style="Accent.TButton",
            command=self.browse_file,
        )
        browse_button.pack(fill="x")

        # Action buttons
        actions_frame = ttk.Frame(container, style="TFrame")
        actions_frame.pack(fill="x", pady=(0, 16))
        actions_frame.columnconfigure((0, 1), weight=1)

        encrypt_button = ttk.Button(
            actions_frame,
            text="🔒  Encrypt",
            style="Accent.TButton",
            command=self.encrypt_file,
        )
        encrypt_button.grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=(0, 8))

        decrypt_button = ttk.Button(
            actions_frame,
            text="🔓  Decrypt",
            style="Accent.TButton",
            command=self.decrypt_file,
        )
        decrypt_button.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=(0, 8))

        clear_button = ttk.Button(
            actions_frame,
            text="🧹  Clear",
            style="Neutral.TButton",
            command=self.clear_selection,
        )
        clear_button.grid(row=1, column=0, sticky="ew", padx=(0, 6))

        exit_button = ttk.Button(
            actions_frame,
            text="🚪  Exit",
            style="Danger.TButton",
            command=self.root.destroy,
        )
        exit_button.grid(row=1, column=1, sticky="ew", padx=(6, 0))

        # Footer / status
        footer_label = ttk.Label(
            container,
            text=f"Encryption key is stored in '{KEY_FILE}'. Keep it safe — "
                 f"without it, encrypted files cannot be recovered.",
            style="Subtitle.TLabel",
            wraplength=512,
            justify="left",
        )
        footer_label.pack(anchor="w", pady=(12, 0))

    # ----------------------------------------------------------------
    # Event handlers / core logic
    # ----------------------------------------------------------------
    def browse_file(self) -> None:
        """Open a file dialog and store the selected file path."""
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            self.selected_file_path.set(file_path)

    def clear_selection(self) -> None:
        """Reset the currently selected file."""
        self.selected_file_path.set("No file selected")

    def _get_valid_selected_path(self) -> str | None:
        """Return the selected path if valid, otherwise show an error and None."""
        path = self.selected_file_path.get()
        if not path or path == "No file selected":
            messagebox.showerror("No File Selected", "Please select a file first.")
            return None
        if not os.path.isfile(path):
            messagebox.showerror("File Not Found", "The selected file no longer exists.")
            return None
        return path

    def encrypt_file(self) -> None:
        """Encrypt the selected file and save the result as a new file."""
        source_path = self._get_valid_selected_path()
        if not source_path:
            return

        try:
            key = self.key_manager.load_key()
            fernet = Fernet(key)

            with open(source_path, "rb") as file:
                original_data = file.read()

            encrypted_data = fernet.encrypt(original_data)

            default_name = os.path.basename(source_path) + ".encrypted"
            save_path = filedialog.asksaveasfilename(
                title="Save Encrypted File As",
                initialfile=default_name,
                defaultextension=".encrypted",
                filetypes=[("Encrypted File", "*.encrypted"), ("All Files", "*.*")],
            )
            if not save_path:
                return  # User cancelled save dialog

            with open(save_path, "wb") as file:
                file.write(encrypted_data)

            messagebox.showinfo(
                "Success",
                f"File encrypted successfully!\n\nSaved to:\n{save_path}",
            )
        except Exception as error:  # noqa: BLE001 - show any failure to the user
            messagebox.showerror("Encryption Failed", f"An error occurred:\n{error}")

    def decrypt_file(self) -> None:
        """Decrypt the selected file and save the restored original file."""
        source_path = self._get_valid_selected_path()
        if not source_path:
            return

        if not self.key_manager.key_exists():
            messagebox.showerror(
                "Key Not Found",
                f"No encryption key found ('{KEY_FILE}').\n"
                f"Cannot decrypt without the original key.",
            )
            return

        try:
            key = self.key_manager.load_key()
            fernet = Fernet(key)

            with open(source_path, "rb") as file:
                encrypted_data = file.read()

            decrypted_data = fernet.decrypt(encrypted_data)

            default_name = os.path.basename(source_path).replace(".encrypted", "")
            save_path = filedialog.asksaveasfilename(
                title="Save Decrypted File As",
                initialfile=default_name or "decrypted_file",
            )
            if not save_path:
                return  # User cancelled save dialog

            with open(save_path, "wb") as file:
                file.write(decrypted_data)

            messagebox.showinfo(
                "Success",
                f"File decrypted successfully!\n\nSaved to:\n{save_path}",
            )
        except InvalidToken:
            messagebox.showerror(
                "Decryption Failed",
                "Invalid key or corrupted file. Unable to decrypt.",
            )
        except Exception as error:  # noqa: BLE001 - show any failure to the user
            messagebox.showerror("Decryption Failed", f"An error occurred:\n{error}")


def main() -> None:
    """Application entry point."""
    root = tk.Tk()
    FileEncryptorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
