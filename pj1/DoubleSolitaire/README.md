# 🃏 Double Solitaire

**Double Solitaire** is a card game developed in **Python** using the **Pygame** library. This project includes both human and AI (Artificial Intelligence) gameplay modes, as well as several customization and configuration options.

---

## 📦 Prerequisites

Before running the project, make sure you have the following installed on your system:

- **Python 3.8 or higher**
- **Pygame 2.6.1** (or compatible version)
- **ConfigParser 7.2.0**

---

## 🚀 Installation

# Navigate to the project directory
cd c:...\IA project\FEUP-IART\pj1\DoubleSolitaire

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the Game

```bash
# To start the game:
python run.py
```

---

## 🎮 How to Play

### 🏠 Main Menu

When you start the game, you will see the **main menu** with the following options:

- **PLAY**: Start a new game.
- **OPTIONS**: Adjust settings such as resolution, difficulty, and AI.
- **LOAD GAME**: Load a previously saved game.
- **QUIT**: Exit the game.

---

### 🕹️ In-Game

#### 🎴 Card Movement

- Click and drag cards to move them between slots or to the foundations.
- Double-click a card to automatically move it to the foundation, if possible.

#### 📚 Sidebar

- **Main Menu**: Return to the main menu.
- **Undo**: Undo the last move.
- **Options**: Open the options menu.
- **Hint**: Show a move suggestion.
- **Save**: Save the current game state.

---

### ⌨️ Controls

#### 🖱️ Mouse

- **Left click**: Select and move cards.
- Click on interface buttons to interact with the game.

#### ⌨️ Keyboard

- **R**: Restart the game.
- **M**: Return to the main menu.
- **F**: Toggle fullscreen/windowed mode.
- **ESC**: Exit the game.

---

## ⚙️ Configuration

Game settings can be adjusted in the **config.cfg** file. Here are some available options:

### 🖥️ Resolution

- **reswidth** and **resheight**: Set the width and height of the game window.

### 🖥️ Fullscreen Mode

- **fullscreen**: Set whether the game starts in fullscreen (`True` or `False`).

### ⚡ Other Options

- **fast mode**: Enable or disable fast mode.
- **no anims**: Remove animations for a faster experience.
- **difficulty**: Set the initial game difficulty (`easy`, `medium`, `hard`).

---

## AI Modes

The game supports an Artificial Intelligence (AI) algorithm to play automatically:

1. **DFS (Depth-First Search)**  
   Explores all possible moves until a solution is found. This method is exhaustive and guarantees a solution if one exists, but can be inefficient in games with many
