# 🎯 Codveda | Number Guessing Game

A professional, modern **dark-themed GUI Number Guessing Game** built with Python's built-in `Tkinter` library. The computer picks a random number between **1 and 100**, and you try to guess it — with live feedback, attempt tracking, and robust input validation.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-7f5af0)
![License](https://img.shields.io/badge/License-MIT-2cb67d)

---

## ✨ Features

- 🎨 Modern dark-themed interface with a clean card-style layout
- 🔢 Random number generation between 1 and 100
- ⌨️ Guess via Entry widget (Enter key also submits)
- 🔘 Three actions: **Guess**, **New Game**, **Exit**
- 📊 Real-time feedback: **Too High**, **Too Low**, **Correct!**
- 🧮 Live attempts counter
- 🛡️ Full input validation — empty, non-numeric, or out-of-range input never crashes the app
- 🖥️ Window auto-centers on screen
- 🧱 Clean, object-oriented, and well-commented code
- 📦 Single-file application — no external dependencies

---

## 📸 Preview

```
🎯 Number Guessing Game
Guess a number between 1 and 100

[      Entry box      ]
[        Guess         ]

📉 Too Low! Try again.
Attempts: 3

[   New Game   ] [   Exit   ]
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8+**
- Tkinter (bundled with most standard Python installations)

> On some Linux distributions, Tkinter may need to be installed separately:
> ```bash
> sudo apt-get install python3-tk
> ```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/number-guessing-game.git
   cd number-guessing-game
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. Install dependencies (none required beyond the standard library):
   ```bash
   pip install -r requirements.txt
   ```

### Run the Game

```bash
python guessing_game.py
```

---

## 🕹️ How to Play

1. Launch the app — a random number between 1 and 100 is chosen.
2. Type your guess into the input box.
3. Click **Guess** or press **Enter**.
4. Read the feedback:
   - 📉 **Too Low** — guess higher
   - 📈 **Too High** — guess lower
   - 🎉 **Correct!** — you win, with your total attempts shown
5. Click **New Game** to play again, or **Exit** to close the app.

---

## 🗂️ Project Structure

```
number-guessing-game/
├── guessing_game.py     # Main application (GUI + game logic)
├── README.md            # Project documentation
├── requirements.txt     # Project dependencies
├── LICENSE              # MIT License
└── .gitignore           # Files/folders excluded from version control
```

---

## 🛠️ Built With

- [Python](https://www.python.org/) — core language
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — GUI framework (standard library)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙌 Author

Developed as part of **Codveda** learning projects.
