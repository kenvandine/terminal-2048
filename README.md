# Terminal 2048

A simple but feature-rich implementation of the classic 2048 game that runs in your terminal. This version is written in Rust and uses the `crossterm` library to provide a colorful and engaging gameplay experience.

## Features

- **Colorful UI**: The game uses ANSI escape codes to display a colorful and visually appealing board.
- **High Score Tracking**: Your top 10 high scores are saved locally in `~/.2048_high_scores.json`.
- **Flexible Controls**: Play with either WASD or the arrow keys.
- **Smooth Gameplay**: The game is responsive and provides a smooth experience.
- **Cross-platform**: Runs on any system that supports Rust and `crossterm` (Linux, macOS, and modern Windows terminals).

## How to Play

### Prerequisites

- Rust toolchain (https://rustup.rs/)

### Running the game

1.  Clone the repository:
    ```bash
    git clone https://github.com/kenvandine/terminal-2048.git
    cd terminal-2048
    ```
2.  Run the game:
    ```bash
    cargo run --release
    ```

### Controls

- **W** or **Up Arrow**: Move tiles up
- **S** or **Down Arrow**: Move tiles down
- **A** or **Left Arrow**: Move tiles left
- **D** or **Right Arrow**: Move tiles right
- **H**: View high scores
- **Q**: Quit the game

## Project Structure

The repository is organized as a standard Rust project:

- `src/main.rs`: The entry point of the application. It initializes the `GameUI` and starts the game.
- `src/lib.rs`: The library crate root, which exposes the `game` and `scores` modules.
- `src/game/`: This module contains the core game functionality.
  - `logic.rs`: Implements the game's state, rules, and logic (e.g., moving and merging tiles).
  - `ui.rs`: Handles all terminal rendering, user input, and the main game loop.
- `src/scores.rs`: Manages high score persistence, including loading from and saving to a JSON file.
- `tests/`: Contains integration tests for the game logic.
- `Cargo.toml`: The package manifest for Rust's package manager, Cargo.

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

## Fun Facts

This project has been a fun experiment with vibe coding and Jules.
