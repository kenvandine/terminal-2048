#!/usr/bin/env python3
"""
Terminal-based 2048 Game for Linux - Colorful Edition
Use WASD or arrow keys to move tiles
Goal: Reach 2048!
"""

import sys
from game.core import main, GameUI, Colors

def start_game():
    """Check for interactive terminal and start the game."""
    if sys.stdout.isatty():
        main()
    else:
        print(f"{Colors.BRIGHT_RED}Not running in an interactive terminal.{Colors.RESET}")
        print("This game requires an interactive terminal to run.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        start_game()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.BRIGHT_RED}Game interrupted by user!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.BRIGHT_RED}An unexpected error occurred: {e}{Colors.RESET}")
    finally:
        # In case the terminal state is messed up, try to restore it
        if sys.stdout.isatty():
            import os
            os.system('stty sane')
