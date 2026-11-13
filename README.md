# 🎮 Tic-Tac-Toe (Python + Pygame)

A complete desktop Tic-Tac-Toe game built with **Python** and **Pygame**. Play against a friend or take on an AI opponent with three different difficulty levels.

This was one of my first complete game projects after learning Python, and it helped me practice functions, game loops, event handling, matrix logic, and basic AI algorithms.

> **Note:** This project was originally uploaded to my previous GitHub account. I am re-uploading it here because that account had some problems. This new profile is my active and clean GitHub account.

---

## ✨ Features

- 🎯 **Two game modes**
  - **Player vs Player**  two humans take turns on the same board
  - **Player vs Bot** – play against the computer
- 🤖 **Three AI difficulties**
  - **Easy** – bot plays random moves
  - **Medium** – bot blocks your wins and takes its own winning moves
  - **Hard** – bot uses the **Minimax algorithm** (unbeatable)
- 🖱️ **Mouse controls** – click a cell to place your piece
- 🏆 **Win / Draw detection** with a highlighted winning line
- 🔁 **Play Again** button returns to the main menu
- ⌨️ **ESC** on the difficulty screen goes back to the mode menu
- 🖼️ Custom images for the board and pieces
- 🧠 Built with a simple, readable structure suitable for beginners learning game development

---

## 🕹️ How to Play

1. **Choose a mode** on the start screen:
   - *Player vs Player* → jump straight into the game
   - *Player vs Bot* → choose a difficulty (Easy / Medium / Hard)
2. **Player 1** is always **X** and moves first.
3. In **Player vs Bot**, you play as **X** and the bot plays as **O**.
4. Click any empty square on the 3×3 board to place your piece.
5. Get **three in a row** (horizontal, vertical, or diagonal) to win.
6. When the game ends, click **Play Again** to return to the main menu.

---

🤖 Built with AI help
The Player vs Bot mode specifically the bot's decision-making logic

The Easy bot (random moves)

The Medium bot (win/block logic)

The Hard bot (Minimax algorithm with depth-based scoring)

For this part, I used DeepSeek AI as a learning assistant. I described what I wanted the bot to do, worked through the logic with the AI, tested the results, and integrated the bot into the existing game I had already written. This was a great way for me to understand how game AI and the Minimax algorithm actually work in practice.

💡 Why I'm sharing this: I believe in being honest about how a project was made. Using AI as a learning tool to understand new concepts like Minimax is a valid way to grow as a developer, as long as the work is understood and not just copy-pasted. Everything in this project was reviewed, tested, and integrated by me.
## 🧩 Requirements

- **Python 3.10+**
- **pygame-ce** (Community Edition of Pygame  drop-in replacement, actively maintained and supports newer Python versions like 3.14)

> ⚠️ **Why `pygame-ce` and not `pygame`?** The original `pygame` package currently has no pre-built wheels for Python 3.14 on Windows, so installation fails. `pygame-ce` installs cleanly and your code still uses `import pygame` as usual.

Install with:

```bash
pip install pygame-ce
