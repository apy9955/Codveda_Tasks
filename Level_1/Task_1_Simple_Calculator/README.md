# 🧮 Simple Calculator — Codveda Python Development Internship

A professional, GUI-based calculator built with **Python** and **Tkinter**, featuring a modern dark theme, full arithmetic operation support, and robust error handling.

> Developed as part of the **Codveda Technologies Python Development Internship** program.

---

## 📸 Preview

```
┌────────────────────────────────┐
│        Simple Calculator        │
│  ┌────────────────────────────┐ │
│  │                     123 + 45│ │
│  └────────────────────────────┘ │
│   C     %      √      ÷         │
│   7     8      9      ×         │
│   4     5      6      -         │
│   1     2      3      +         │
│   ^     0      .      mod       │
│      Exit          =            │
└────────────────────────────────┘
```

---

## ✨ Features

| Category | Details |
|---|---|
| **Operations** | Addition, Subtraction, Multiplication, Division, Modulus, Power, Square Root, Percentage |
| **UI/UX** | Modern dark theme, responsive grid-based buttons, centered window, clean typography |
| **Validation** | Handles empty input, invalid expressions, division/modulus by zero, and negative square roots |
| **Error Handling** | User-friendly `messagebox` popups instead of crashes or silent failures |
| **Controls** | `C` (Clear) and `Exit` (with confirmation prompt) |
| **Code Quality** | PEP 8 compliant, fully commented, organized into a single well-structured `CalculatorApp` class |

---

## 🗂️ Project Structure

```
codveda-calculator/
├── calculator.py       # Main application (GUI + logic)
├── README.md            # Project documentation (this file)
├── requirements.txt     # Project dependencies
└── LICENSE               # (optional) open-source license
```

---

## ⚙️ Requirements

- Python 3.8 or higher
- `tkinter` (included with standard Python installations)

No external/third-party packages are required — see [`requirements.txt`](./requirements.txt) for details.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/codveda-calculator.git
cd codveda-calculator
```

### 2. (Optional) Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
> Note: This project relies solely on the Python Standard Library, so this step installs nothing extra — it's included for completeness and best practice.

### 4. Run the application
```bash
python calculator.py
```

---

## 🧠 How It Works

The application is built around a single `CalculatorApp` class that encapsulates:

1. **Window setup** — configures size, title, dark theme, and centers the window on screen.
2. **Display** — a read-only `Entry` widget bound to a `StringVar`, showing the live expression and results.
3. **Button grid** — a responsive `grid` layout where every row/column has a defined weight, so buttons resize proportionally with the window.
4. **Event routing** — every button press flows through `_on_button_click()`, which dispatches to the correct handler (digit entry, clear, exit, calculate, square root, percentage).
5. **Safe evaluation** — expressions are evaluated using a restricted `eval()` call (`{"__builtins__": {}}`) that only ever receives characters the app itself appended, preventing arbitrary code execution.
6. **Error handling** — every arithmetic path is wrapped in `try/except` blocks that catch `ZeroDivisionError`, `ValueError`, `SyntaxError`, `TypeError`, and `OverflowError`, surfacing a clear `messagebox` alert to the user.

---

## 🖱️ Usage Guide

| Button | Action |
|---|---|
| `0`–`9`, `.` | Build up the current number |
| `+` `-` `×` `÷` | Basic arithmetic operators |
| `^` | Power (exponentiation) |
| `mod` | Modulus (remainder) |
| `√` | Square root of current value |
| `%` | Converts current value to a percentage (÷ 100) |
| `=` | Evaluates the full expression |
| `C` | Clears the display and resets input |
| `Exit` | Closes the app (with confirmation) |

---

## 🛡️ Error Handling Highlights

- **Division/Modulus by zero** → `"Cannot divide by zero"` popup, display auto-clears.
- **Negative square root** → `"Cannot compute square root of a negative number"` popup.
- **Empty input on `=`, `√`, or `%`** → prompts the user to enter a value first.
- **Malformed expressions** (e.g. `5++`) → `"Invalid Expression"` popup instead of a crash.

---

## 🎨 Design Notes

The interface uses a **Catppuccin-inspired dark palette** for a professional, portfolio-ready aesthetic:

- Background: `#1e1e2e`
- Display: `#11111b`
- Operators: `#89b4fa` (soft blue)
- Clear / Exit: `#f38ba8` (soft red)
- Equals: `#a6e3a1` (soft green)

Colors are centralized as class constants in `calculator.py`, making the theme easy to customize.

---

## 👤 Author

**Codveda Python Development Intern**
Submitted as part of the Codveda Technologies internship program.

---

## 📄 License

This project is open source and available under the [MIT License](./LICENSE).
