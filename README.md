# 🐍 Classic Snake Game (Python + Pygame)

A robust implementation of the classic Snake arcade game built with Python and Pygame using Gemini 3 Pro model. This project features a polished Start Menu, adjustable difficulty settings, sound effects, and a definitive victory condition.

**Developed as a rapid 2-hour coding challenge.**

## 🎮 Features

* **Start Menu:** Interactive landing screen to select difficulty.
* **3 Difficulty Modes:**
    * **Easy:** For a relaxed experience.
    * **Medium:** The standard challenge.
    * **Hard:** High-speed reflex test.
* **Victory Condition:** The game is beatable! Reach a score of **30** to trigger the Win Screen.
* **Audio Integration:** Sound effects for Game Over and Victory.
* **Visual Polish:** border rendering to clearly define the play area and custom score display.
* **Fail-safe Audio:** The game runs smoothly even if sound files are missing.

## 🛠️ Prerequisites

* Python 3.x
* `pygame` library

## 🚀 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/snake-game.git](https://github.com/your-username/snake-game.git)
    cd snake-game
    ```

2.  **Install dependencies:**
    ```bash
    pip install pygame
    ```

3.  **Add Sound Files (Optional):**
    For the full experience, add two `.wav` files to the root directory:
    * `gameover.wav` (Sound played on collision)
    * `win.wav` (Sound played on victory)
    
    *Note: The game will still run without these files.*

4.  **Run the game:**
    ```bash
    python snake.py
    ```

## 🕹️ Controls

| Key | Action |
| :--- | :--- |
| **Arrow Keys** | Move Snake (Up, Down, Left, Right) |
| **1 / 2 / 3** | Select Difficulty (Easy / Med / Hard) |
| **C** | Play Again (After Win/Loss) |
| **M** | Return to Main Menu |
| **Q** | Quit Game |

## 📂 Project Structure

```text
📦 snake-game
 ┣ 📜 snake.py        # Main game source code
 ┣ 📜 gameover.wav    # (Optional) Audio file
 ┣ 📜 win.wav         # (Optional) Audio file
 ┗ 📜 README.md       # Project documentation