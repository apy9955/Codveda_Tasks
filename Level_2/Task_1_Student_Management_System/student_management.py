"""
==============================================================================
 Codveda | Student Management System
==============================================================================
 A professional desktop application for managing student records, built
 with Python's Tkinter (GUI) and SQLite3 (database).

 Features:
   - Add / Update / Delete / Search / View All student records
   - Modern dark-themed interface with hover effects on buttons
   - Input validation (empty fields, email format, phone number format)
   - Data persisted locally in an SQLite database (student.db)

 Author : Codveda Internship Submission
 File   : student_management.py
==============================================================================
"""

import re
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


# ==============================================================================
# CONFIGURATION / THEME CONSTANTS
# ==============================================================================
class Theme:
    """Centralized color & font configuration for the dark theme UI."""

    BG_MAIN = "#1e1e2e"        # Main window background
    BG_PANEL = "#262637"       # Panel / frame background
    BG_INPUT = "#2e2e42"       # Entry widget background
    BG_TREE = "#232335"        # Treeview background
    BG_TREE_HEAD = "#31314a"   # Treeview header background

    FG_TEXT = "#FFFFFF"        # Primary text color
    FG_LABEL = "#FFFFFF"       # Secondary / label text color
    FG_MUTED = "#FFFFFF"       # Muted / placeholder text color

    ACCENT = "#7f5af0"         # Primary accent (purple)
    ACCENT_HOVER = "#9b7bf5"   # Accent hover state
    SUCCESS = "#2cb67d"        # Add button
    SUCCESS_HOVER = "#3fd696"
    WARNING = "#ff8906"        # Update button
    WARNING_HOVER = "#ffa63d"
    DANGER = "#e53170"         # Delete / Exit button
    DANGER_HOVER = "#ff5c8a"
    INFO = "#3da9fc"           # Search / View button
    INFO_HOVER = "#63bdff"
    NEUTRAL = "#4a4a63"        # Clear button
    NEUTRAL_HOVER = "#5e5e7a"

    FONT_TITLE = ("Segoe UI", 20, "bold")
    FONT_SUBTITLE = ("Segoe UI", 10)
    FONT_LABEL = ("Segoe UI", 10, "bold")
    FONT_ENTRY = ("Segoe UI", 10)
    FONT_BUTTON = ("Segoe UI", 10, "bold")
    FONT_TREE_HEAD = ("Segoe UI", 10, "bold")
    FONT_TREE_ROW = ("Segoe UI", 9)


# ==============================================================================
# DATABASE LAYER
# ==============================================================================
class Database:
    """
    Handles all interactions with the SQLite database.
    Keeps SQL logic separate from the GUI for clean, maintainable code.
    """

    def __init__(self, db_name="student.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        """Create the students table if it does not already exist."""
        query = """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT NOT NULL,
                age        INTEGER NOT NULL,
                gender     TEXT NOT NULL,
                course     TEXT NOT NULL,
                phone      TEXT NOT NULL,
                email      TEXT NOT NULL
            )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def add_student(self, name, age, gender, course, phone, email):
        """Insert a new student record."""
        query = """
            INSERT INTO students (name, age, gender, course, phone, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (name, age, gender, course, phone, email))
        self.connection.commit()

    def update_student(self, student_id, name, age, gender, course, phone, email):
        """Update an existing student record by ID."""
        query = """
            UPDATE students
            SET name = ?, age = ?, gender = ?, course = ?, phone = ?, email = ?
            WHERE student_id = ?
        """
        self.cursor.execute(
            query, (name, age, gender, course, phone, email, student_id)
        )
        self.connection.commit()

    def delete_student(self, student_id):
        """Delete a student record by ID."""
        query = "DELETE FROM students WHERE student_id = ?"
        self.cursor.execute(query, (student_id,))
        self.connection.commit()

    def search_students(self, keyword):
        """Search students by name, course, phone, or email (partial match)."""
        query = """
            SELECT * FROM students
            WHERE name LIKE ? OR course LIKE ? OR phone LIKE ? OR email LIKE ?
        """
        like_kw = f"%{keyword}%"
        self.cursor.execute(query, (like_kw, like_kw, like_kw, like_kw))
        return self.cursor.fetchall()

    def fetch_all_students(self):
        """Retrieve all student records ordered by ID."""
        self.cursor.execute("SELECT * FROM students ORDER BY student_id ASC")
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection gracefully."""
        self.connection.close()


# ==============================================================================
# VALIDATION HELPERS
# ==============================================================================
class Validator:
    """Static helper methods for validating user input."""

    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    PHONE_REGEX = r"^\+?\d{7,15}$"  # optional leading +, 7-15 digits

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return re.match(Validator.EMAIL_REGEX, email) is not None

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        return re.match(Validator.PHONE_REGEX, phone) is not None

    @staticmethod
    def is_valid_age(age: str) -> bool:
        return age.isdigit() and 0 < int(age) < 120


# ==============================================================================
# HOVER BUTTON WIDGET
# ==============================================================================
class HoverButton(tk.Button):
    """
    A custom Tkinter Button with a smooth hover color effect.
    Extends the standard button to switch background color on mouse enter/leave.
    """

    def __init__(self, master, bg, hover_bg, fg="white", **kwargs):
        super().__init__(
            master,
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=Theme.FONT_BUTTON,
            **kwargs,
        )
        self.default_bg = bg
        self.hover_bg = hover_bg
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event):
        self.config(bg=self.hover_bg)

    def _on_leave(self, _event):
        self.config(bg=self.default_bg)


# ==============================================================================
# MAIN APPLICATION
# ==============================================================================
class StudentManagementApp:
    """
    Main application class that builds and controls the GUI, and links
    user actions to the underlying Database layer.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.db = Database("student.db")

        # Tracks the currently selected student ID (for update/delete)
        self.selected_id = None

        self._configure_window()
        self._configure_styles()
        self._build_layout()
        self._load_all_students()

    # --------------------------------------------------------------------
    # WINDOW CONFIGURATION
    # --------------------------------------------------------------------
    def _configure_window(self):
        """Set title, size, background, and center the window on screen."""
        self.root.title("Codveda | Student Management System")
        self.root.configure(bg=Theme.BG_MAIN)
        self.root.minsize(1000, 640)
        self._center_window(1000, 640)

        # Handle graceful shutdown via window close (X) button
        self.root.protocol("WM_DELETE_WINDOW", self._on_exit)

    def _center_window(self, width, height):
        """Compute screen dimensions and position the window in the center."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _configure_styles(self):
        """Configure ttk styles for a cohesive dark theme (Combobox, Treeview)."""
        style = ttk.Style()
        style.theme_use("clam")

        # Treeview body styling
        style.configure(
            "Custom.Treeview",
            background=Theme.BG_TREE,
            foreground=Theme.FG_TEXT,
            fieldbackground=Theme.BG_TREE,
            rowheight=28,
            font=Theme.FONT_TREE_ROW,
            borderwidth=0,
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", Theme.ACCENT)],
            foreground=[("selected", "white")],
        )

        # Treeview header styling
        style.configure(
            "Custom.Treeview.Heading",
            background=Theme.BG_TREE_HEAD,
            foreground=Theme.FG_TEXT,
            font=Theme.FONT_TREE_HEAD,
            relief="flat",
        )
        style.map("Custom.Treeview.Heading", background=[("active", Theme.ACCENT)])

        # Combobox (Gender dropdown) styling
        style.configure(
            "Custom.TCombobox",
            fieldbackground=Theme.BG_INPUT,
            background=Theme.BG_INPUT,
            foreground=Theme.FG_TEXT,
            arrowcolor=Theme.FG_TEXT,
            borderwidth=0,
        )
        style.map(
            "Custom.TCombobox",
            fieldbackground=[("readonly", Theme.BG_INPUT)],
            foreground=[("readonly", Theme.FG_TEXT)],
        )

    # --------------------------------------------------------------------
    # LAYOUT CONSTRUCTION
    # --------------------------------------------------------------------
    def _build_layout(self):
        """Build the full GUI layout: header, form panel, buttons, and table."""
        self._build_header()

        # Container splitting the form (left) and the table (right/below)
        body = tk.Frame(self.root, bg=Theme.BG_MAIN)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self._build_form_panel(body)
        self._build_table_panel(body)

    def _build_header(self):
        """Top banner with application title and subtitle."""
        header = tk.Frame(self.root, bg=Theme.BG_MAIN)
        header.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(
            header,
            text="🎓  Student Management System",
            font=Theme.FONT_TITLE,
            bg=Theme.BG_MAIN,
            fg=Theme.FG_TEXT,
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Codveda Internship Project — Manage student records with ease",
            font=Theme.FONT_SUBTITLE,
            bg=Theme.BG_MAIN,
            fg=Theme.FG_LABEL,
        ).pack(anchor="w")

    def _build_form_panel(self, parent):
        """Left-side panel containing input fields and action buttons."""
        panel = tk.Frame(parent, bg=Theme.BG_PANEL, padx=20, pady=20)
        panel.pack(side="left", fill="y", padx=(0, 15))

        tk.Label(
            panel,
            text="Student Details",
            font=Theme.FONT_LABEL,
            bg=Theme.BG_PANEL,
            fg=Theme.ACCENT,
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # Dictionary of Tkinter StringVars bound to each entry field
        self.vars = {
            "name": tk.StringVar(),
            "age": tk.StringVar(),
            "gender": tk.StringVar(),
            "course": tk.StringVar(),
            "phone": tk.StringVar(),
            "email": tk.StringVar(),
        }

        fields = [
            ("Full Name", "name", "entry"),
            ("Age", "age", "entry"),
            ("Gender", "gender", "combo"),
            ("Course", "course", "entry"),
            ("Phone Number", "phone", "entry"),
            ("Email Address", "email", "entry"),
        ]

        row = 1
        for label_text, key, widget_type in fields:
            tk.Label(
                panel,
                text=label_text,
                font=Theme.FONT_LABEL,
                bg=Theme.BG_PANEL,
                fg=Theme.FG_LABEL,
            ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(8, 2))
            row += 1

            if widget_type == "entry":
                entry = tk.Entry(
                    panel,
                    textvariable=self.vars[key],
                    font=Theme.FONT_ENTRY,
                    bg=Theme.BG_INPUT,
                    fg=Theme.FG_TEXT,
                    insertbackground=Theme.FG_TEXT,
                    relief="flat",
                    highlightthickness=1,
                    highlightbackground=Theme.NEUTRAL,
                    highlightcolor=Theme.ACCENT,
                )
                entry.grid(row=row, column=0, columnspan=2, sticky="ew", ipady=6)
            else:  # combo box for Gender
                combo = ttk.Combobox(
                    panel,
                    textvariable=self.vars[key],
                    values=["Male", "Female", "Other"],
                    state="readonly",
                    style="Custom.TCombobox",
                    font=Theme.FONT_ENTRY,
                )
                combo.grid(row=row, column=0, columnspan=2, sticky="ew", ipady=4)
            row += 1

        panel.grid_columnconfigure(0, weight=1)
        panel.grid_columnconfigure(1, weight=1)

        # ---------------- Action Buttons ----------------
        btn_frame = tk.Frame(panel, bg=Theme.BG_PANEL)
        btn_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        HoverButton(
            btn_frame, Theme.SUCCESS, Theme.SUCCESS_HOVER,
            text="➕ Add Student", command=self.add_student,
        ).grid(row=0, column=0, sticky="ew", padx=3, pady=4, ipady=6)

        HoverButton(
            btn_frame, Theme.WARNING, Theme.WARNING_HOVER,
            text="✏️ Update", command=self.update_student,
        ).grid(row=0, column=1, sticky="ew", padx=3, pady=4, ipady=6)

        HoverButton(
            btn_frame, Theme.DANGER, Theme.DANGER_HOVER,
            text="🗑️ Delete", command=self.delete_student,
        ).grid(row=1, column=0, sticky="ew", padx=3, pady=4, ipady=6)

        HoverButton(
            btn_frame, Theme.NEUTRAL, Theme.NEUTRAL_HOVER,
            text="🧹 Clear Form", command=self.clear_form,
        ).grid(row=1, column=1, sticky="ew", padx=3, pady=4, ipady=6)

        HoverButton(
            btn_frame, Theme.INFO, Theme.INFO_HOVER,
            text="📋 View All", command=self._load_all_students,
        ).grid(row=2, column=0, sticky="ew", padx=3, pady=4, ipady=6)

        HoverButton(
            btn_frame, Theme.DANGER, Theme.DANGER_HOVER,
            text="🚪 Exit", command=self._on_exit,
        ).grid(row=2, column=1, sticky="ew", padx=3, pady=4, ipady=6)

    def _build_table_panel(self, parent):
        """Right-side panel containing search bar and the records Treeview."""
        panel = tk.Frame(parent, bg=Theme.BG_MAIN)
        panel.pack(side="left", fill="both", expand=True)

        # ---------------- Search Bar ----------------
        search_frame = tk.Frame(panel, bg=Theme.BG_PANEL, padx=15, pady=12)
        search_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=Theme.FONT_LABEL,
            bg=Theme.BG_PANEL,
            fg=Theme.FG_LABEL,
        ).pack(side="left", padx=(0, 10))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=Theme.FONT_ENTRY,
            bg=Theme.BG_INPUT,
            fg=Theme.FG_TEXT,
            insertbackground=Theme.FG_TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=Theme.NEUTRAL,
            highlightcolor=Theme.ACCENT,
        )
        search_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 10))
        search_entry.bind("<Return>", lambda _e: self.search_student())

        HoverButton(
            search_frame, Theme.INFO, Theme.INFO_HOVER,
            text="Search", command=self.search_student,
        ).pack(side="left", ipadx=10, ipady=4)

        # ---------------- Treeview Table ----------------
        table_frame = tk.Frame(panel, bg=Theme.BG_MAIN)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "name", "age", "gender", "course", "phone", "email")
        headings = ["ID", "Name", "Age", "Gender", "Course", "Phone", "Email"]
        widths = [50, 140, 50, 80, 130, 110, 180]

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
        )
        for col, head, width in zip(columns, headings, widths):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=width, anchor="center")

        # Vertical scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # When a row is clicked, populate the form fields with its data
        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

    # --------------------------------------------------------------------
    # CRUD ACTIONS
    # --------------------------------------------------------------------
    def _get_form_values(self):
        """Return a dict of stripped values currently in the form fields."""
        return {key: var.get().strip() for key, var in self.vars.items()}

    def _validate_form(self, values) -> bool:
        """
        Validate all form fields before insert/update.
        Shows a message box and returns False on the first failure found.
        """
        # Check for empty fields
        for field_name, value in values.items():
            if not value:
                messagebox.showwarning(
                    "Validation Error", f"'{field_name.capitalize()}' cannot be empty."
                )
                return False

        # Validate age
        if not Validator.is_valid_age(values["age"]):
            messagebox.showwarning(
                "Validation Error", "Please enter a valid age (1-119)."
            )
            return False

        # Validate email
        if not Validator.is_valid_email(values["email"]):
            messagebox.showwarning(
                "Validation Error", "Please enter a valid email address."
            )
            return False

        # Validate phone
        if not Validator.is_valid_phone(values["phone"]):
            messagebox.showwarning(
                "Validation Error",
                "Please enter a valid phone number (7-15 digits, optional '+').",
            )
            return False

        return True

    def add_student(self):
        """Validate form input and insert a new student record."""
        values = self._get_form_values()
        if not self._validate_form(values):
            return

        self.db.add_student(
            values["name"], values["age"], values["gender"],
            values["course"], values["phone"], values["email"],
        )
        messagebox.showinfo("Success", "Student added successfully.")
        self.clear_form()
        self._load_all_students()

    def update_student(self):
        """Validate form input and update the currently selected student."""
        if self.selected_id is None:
            messagebox.showwarning(
                "No Selection", "Please select a student from the table to update."
            )
            return

        values = self._get_form_values()
        if not self._validate_form(values):
            return

        self.db.update_student(
            self.selected_id, values["name"], values["age"], values["gender"],
            values["course"], values["phone"], values["email"],
        )
        messagebox.showinfo("Success", "Student record updated successfully.")
        self.clear_form()
        self._load_all_students()

    def delete_student(self):
        """Delete the currently selected student after confirmation."""
        if self.selected_id is None:
            messagebox.showwarning(
                "No Selection", "Please select a student from the table to delete."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this student record?"
        )
        if confirm:
            self.db.delete_student(self.selected_id)
            messagebox.showinfo("Deleted", "Student record deleted successfully.")
            self.clear_form()
            self._load_all_students()

    def search_student(self):
        """Search for students matching the keyword and refresh the table."""
        keyword = self.search_var.get().strip()
        if not keyword:
            self._load_all_students()
            return

        results = self.db.search_students(keyword)
        self._populate_table(results)

        if not results:
            messagebox.showinfo("No Results", "No matching student records found.")

    def clear_form(self):
        """Reset all form fields and clear the current selection."""
        for var in self.vars.values():
            var.set("")
        self.selected_id = None
        self.search_var.set("")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

    # --------------------------------------------------------------------
    # TABLE / DATA REFRESH HELPERS
    # --------------------------------------------------------------------
    def _load_all_students(self):
        """Fetch every record from the database and display it in the table."""
        records = self.db.fetch_all_students()
        self._populate_table(records)

    def _populate_table(self, records):
        """Clear the Treeview and repopulate it with the given records."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for record in records:
            self.tree.insert("", "end", values=record)

    def _on_row_select(self, _event):
        """When a table row is clicked, load its values into the form fields."""
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.selected_id = int(values[0])
        self.vars["name"].set(values[1])
        self.vars["age"].set(values[2])
        self.vars["gender"].set(values[3])
        self.vars["course"].set(values[4])
        self.vars["phone"].set(values[5])
        self.vars["email"].set(values[6])

    # --------------------------------------------------------------------
    # APPLICATION EXIT
    # --------------------------------------------------------------------
    def _on_exit(self):
        """Confirm exit, close the database connection, and close the app."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
            self.db.close()
            self.root.destroy()


# ==============================================================================
# ENTRY POINT
# ==============================================================================
def main():
    """Application entry point."""
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
