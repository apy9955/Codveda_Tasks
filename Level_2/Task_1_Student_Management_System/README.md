# 🎓 Student Management System

A professional desktop application for managing student records, built with **Python**, **Tkinter**, and **SQLite3**. Developed as part of the **Codveda Internship** program.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-purple)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview

The **Student Management System** is a full-featured desktop application that allows administrators to add, update, delete, search, and view student records through a clean, modern, dark-themed graphical interface. All data is persisted locally using an embedded SQLite database, requiring no external server or setup.

---

## ✨ Features

- ➕ **Add Student** — Insert new student records with full field validation
- ✏️ **Update Student** — Edit existing records by selecting a row from the table
- 🗑️ **Delete Student** — Remove records with a confirmation prompt
- 🔍 **Search Student** — Instantly filter by name, course, phone, or email
- 📋 **View All Students** — Display the complete list of records in a sortable table
- 🧹 **Clear Form** — Reset all input fields in one click
- 🚪 **Exit** — Safely close the database connection and exit the app
- 🎨 **Modern Dark Theme UI** — Custom color palette with smooth button hover effects
- 🖥️ **Auto-Centered Window** — Application launches centered on the user's screen
- ✅ **Input Validation** — Prevents empty fields and validates email/phone formats

---

## 🗂️ Project Structure

```
student-management-system/
├── student_management.py   # Main application source code
├── student.db               # SQLite database (auto-created on first run)
├── README.md                 # Project documentation
├── requirements.txt          # Project dependencies
├── LICENSE                    # MIT License
└── .gitignore                  # Git ignore rules
```

---

## 🗃️ Database Schema

The application uses a single `students` table inside `student.db`:

| Field      | Type    | Constraints                  |
|------------|---------|-------------------------------|
| student_id | INTEGER | Primary Key, Auto Increment  |
| name       | TEXT    | Not Null                     |
| age        | INTEGER | Not Null                     |
| gender     | TEXT    | Not Null                     |
| course     | TEXT    | Not Null                     |
| phone      | TEXT    | Not Null                     |
| email      | TEXT    | Not Null                     |

The table is created automatically the first time the application runs, if it doesn't already exist.

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8 or higher**
- `tkinter` (bundled with standard Python installers on Windows/macOS)

> **Linux users:** If `tkinter` isn't pre-installed, run:
> ```bash
> sudo apt-get install python3-tk      # Debian/Ubuntu
> sudo dnf install python3-tkinter     # Fedora
> ```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/student-management-system.git
   cd student-management-system
   ```

2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate     # On Windows: venv\Scripts\activate
   ```

3. **Run the application**
   ```bash
   python student_management.py
   ```

   No external dependencies are required — the project uses only Python's standard library (`tkinter` and `sqlite3`).

---

## 🧭 Usage Guide

1. Fill in the **Student Details** form on the left panel (Name, Age, Gender, Course, Phone, Email).
2. Click **➕ Add Student** to save a new record to the database.
3. Click any row in the table to load its data back into the form.
4. Modify the fields and click **✏️ Update** to save changes, or **🗑️ Delete** to remove the record.
5. Use the **🔍 Search** bar to filter records by name, course, phone, or email.
6. Click **📋 View All** to reset the table and display every record.
7. Click **🧹 Clear Form** to reset the input fields without affecting the database.
8. Click **🚪 Exit** to safely close the application.

---

## ✅ Validation Rules

| Field | Rule |
|-------|------|
| All fields | Cannot be left empty |
| Age | Must be a number between 1 and 119 |
| Email | Must match a standard email format (e.g., `name@example.com`) |
| Phone | Must be 7–15 digits, with an optional leading `+` |

---

## 🛠️ Built With

- **[Python](https://www.python.org/)** — Core programming language
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)** — GUI toolkit
- **[SQLite3](https://docs.python.org/3/library/sqlite3.html)** — Embedded relational database

---

## 🏗️ Design Notes

- The codebase follows an object-oriented structure, separating concerns into distinct classes: `Database` (data layer), `Validator` (input validation), `Theme` (styling constants), `HoverButton` (reusable UI component), and `StudentManagementApp` (main controller/GUI).
- The interface uses a custom dark color palette with `ttk` styling for the Treeview and Combobox widgets, and hover-responsive buttons for a polished, professional feel.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

Developed as part of the **Codveda Internship Program** to demonstrate practical skills in Python GUI development, database integration, and clean software architecture.
