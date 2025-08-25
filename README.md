# Terminal 2048

A simple but feature-rich implementation of the classic 2048 game that runs in your terminal. This version is written in Python and uses ANSI color codes to provide a colorful and engaging gameplay experience.

## Features

- **Colorful UI**: The game uses ANSI escape codes to display a colorful and visually appealing board.
- **High Score Tracking**: Your top 10 high scores are saved locally in `~/.2048_high_scores.json`.
- **Flexible Controls**: Play with either WASD or the arrow keys.
- **Smooth Gameplay**: The game is responsive and provides a smooth experience.
- **Cross-platform**: Runs on any system that supports Python and ANSI escape codes (Linux, macOS, and modern Windows terminals).

## How to Play

### Prerequisites

- Python 3

### Running the game

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
2.  Run the game:
    ```bash
    python3 2048.py
    ```

### Controls

- **W** or **Up Arrow**: Move tiles up
- **S** or **Down Arrow**: Move tiles down
- **A** or **Left Arrow**: Move tiles left
- **D** or **Right Arrow**: Move tiles right
- **H**: View high scores
- **Q**: Quit the game

## Gameplay Preview

Here is a preview of what the game board looks like:

```
=======================================================
🎮 2048 GAME 🎮
=======================================================
Score: 124  |  High Score: 2048
Use WASD or Arrow Keys • Q to quit • H for high scores
-------------------------------------------------------
┌─────┬─────┬─────┬─────┐
│  2  │  4  │  8  │  16 │
├─────┼─────┼─────┼─────┤
│  32 │  64 │ 128 │ 256 │
├─────┼─────┼─────┼─────┤
│ 512 │ 1024│ 2048│     │
├─────┼─────┼─────┼─────┤
│     │     │     │     │
└─────┴─────┴─────┴─────┘
-------------------------------------------------------
Press a key to move...

```

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
