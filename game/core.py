#!/usr/bin/env python3
"""
Core game logic and UI for the 2048 game.
"""

import random
import os
import sys
import termios
import json
from datetime import datetime

class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'

class GameLogic:
    def __init__(self):
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        """Add a random tile (2 or 4) to an empty position"""
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def move_left(self):
        """Move all tiles left"""
        moved = False
        for i in range(4):
            row = [cell for cell in self.board[i] if cell != 0]
            merged = []
            skip = False
            for j in range(len(row)):
                if skip:
                    skip = False
                    continue
                if j < len(row) - 1 and row[j] == row[j + 1]:
                    merged.append(row[j] * 2)
                    self.score += row[j] * 2
                    if row[j] * 2 == 2048:
                        self.won = True
                    skip = True
                else:
                    merged.append(row[j])

            merged.extend([0] * (4 - len(merged)))
            if self.board[i] != merged:
                moved = True
            self.board[i] = merged
        return moved

    def move_right(self):
        """Move all tiles right"""
        board_before = [row[:] for row in self.board]
        for i in range(4):
            self.board[i] = self.board[i][::-1]
        self.move_left()
        for i in range(4):
            self.board[i] = self.board[i][::-1]
        return board_before != self.board

    def move_up(self):
        """Move all tiles up"""
        board_before = [row[:] for row in self.board]
        self.board = list(map(list, zip(*self.board)))
        self.move_left()
        self.board = list(map(list, zip(*self.board)))
        return board_before != self.board

    def move_down(self):
        """Move all tiles down"""
        board_before = [row[:] for row in self.board]
        self.board = list(map(list, zip(*self.board)))
        self.move_right()
        self.board = list(map(list, zip(*self.board)))
        return board_before != self.board

    def can_move(self):
        """Check if any moves are possible"""
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return True
        for i in range(4):
            for j in range(4):
                current = self.board[i][j]
                if j < 3 and self.board[i][j + 1] == current:
                    return True
                if i < 3 and self.board[i + 1][j] == current:
                    return True
        return False

class GameUI:
    def __init__(self, interactive=True):
        self.logic = GameLogic()
        self.interactive = interactive
        if self.interactive:
            self.fd = sys.stdin.fileno()
            try:
                self.old_settings = termios.tcgetattr(self.fd)
                self.setup_terminal()
            except termios.error:
                self.interactive = False


        self.high_scores_file = os.path.expanduser("~/.2048_high_scores.json")
        self.high_scores = self.load_high_scores()

        self.tile_colors = {
            0: (Colors.BG_BRIGHT_BLACK, Colors.DIM + Colors.WHITE),
            2: (Colors.BG_WHITE, Colors.BOLD + Colors.BLACK),
            4: (Colors.BG_BRIGHT_YELLOW, Colors.BOLD + Colors.BLACK),
            8: (Colors.BG_YELLOW, Colors.BOLD + Colors.WHITE),
            16: (Colors.BG_BRIGHT_MAGENTA, Colors.BOLD + Colors.WHITE),
            32: (Colors.BG_MAGENTA, Colors.BOLD + Colors.WHITE),
            64: (Colors.BG_BRIGHT_RED, Colors.BOLD + Colors.WHITE),
            128: (Colors.BG_RED, Colors.BOLD + Colors.BRIGHT_YELLOW),
            256: (Colors.BG_BRIGHT_CYAN, Colors.BOLD + Colors.BLACK),
            512: (Colors.BG_CYAN, Colors.BOLD + Colors.WHITE),
            1024: (Colors.BG_BRIGHT_GREEN, Colors.BOLD + Colors.BLACK),
            2048: (Colors.BG_GREEN, Colors.BOLD + Colors.BRIGHT_YELLOW),
            4096: (Colors.BG_BRIGHT_BLUE, Colors.BOLD + Colors.WHITE),
            8192: (Colors.BG_BLUE, Colors.BOLD + Colors.BRIGHT_WHITE)
        }

    def load_high_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(self.high_scores_file):
                with open(self.high_scores_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return {"scores": data}
                    return data
            return {"scores": []}
        except (FileNotFoundError, json.JSONDecodeError, PermissionError):
            return {"scores": []}

    def save_high_scores(self):
        """Save high scores to file"""
        try:
            with open(self.high_scores_file, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except (PermissionError, OSError):
            print(f"{Colors.BRIGHT_RED}Warning: Could not save high scores to file.{Colors.RESET}")

    def add_high_score(self, score):
        """Add a new high score and keep top 10"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        highest_tile = max(max(row) for row in self.logic.board)
        score_entry = {"score": score, "date": current_time, "highest_tile": highest_tile}
        self.high_scores["scores"].append(score_entry)
        self.high_scores["scores"].sort(key=lambda x: x["score"], reverse=True)
        self.high_scores["scores"] = self.high_scores["scores"][:10]
        self.save_high_scores()

    def is_new_high_score(self, score):
        """Check if current score is a new high score (top 10)"""
        if len(self.high_scores["scores"]) < 10:
            return True
        if not self.high_scores["scores"]:
            return True
        return score > min(entry["score"] for entry in self.high_scores["scores"])

    def get_rank(self, score):
        """Get the rank of current score among high scores"""
        scores = [entry["score"] for entry in self.high_scores["scores"]]
        scores.append(score)
        scores.sort(reverse=True)
        return scores.index(score) + 1

    def display_high_scores(self):
        """Display the high scores table"""
        print(f"\n{Colors.BOLD}{Colors.BRIGHT_YELLOW}🏆 HIGH SCORES 🏆{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'=' * 65}{Colors.RESET}")
        if not self.high_scores["scores"]:
            print(f"{Colors.DIM}No high scores yet. Be the first!{Colors.RESET}")
            return
        print(f"{Colors.BOLD}{Colors.BRIGHT_WHITE}{'Rank':<4} {'Score':<8} {'Highest Tile':<12} {'Date':<19}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'-' * 65}{Colors.RESET}")
        for i, entry in enumerate(self.high_scores["scores"], 1):
            rank_color = Colors.BRIGHT_YELLOW if i <= 3 else Colors.BRIGHT_WHITE
            tile_color = Colors.BRIGHT_GREEN if entry["highest_tile"] >= 2048 else Colors.BRIGHT_CYAN
            print(f"{rank_color}{i:<4}{Colors.RESET} "
                  f"{Colors.BRIGHT_WHITE}{entry['score']:<8}{Colors.RESET} "
                  f"{tile_color}{entry['highest_tile']:<12}{Colors.RESET} "
                  f"{Colors.DIM}{entry['date']:<19}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'=' * 65}{Colors.RESET}")

    def setup_terminal(self):
        """Setup terminal for immediate key detection"""
        new_settings = termios.tcgetattr(self.fd)
        new_settings[3] = new_settings[3] & ~(termios.ICANON | termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSADRAIN, new_settings)

    def restore_terminal(self):
        """Restore normal terminal behavior"""
        if self.interactive:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    def get_char(self):
        """Get a single character from stdin"""
        return sys.stdin.read(1)

    def get_key(self):
        """Get and process keyboard input"""
        char = self.get_char()
        if char == '\x1b':
            char += self.get_char()
            char += self.get_char()
            if char == '\x1b[A': return 'UP'
            elif char == '\x1b[B': return 'DOWN'
            elif char == '\x1b[C': return 'RIGHT'
            elif char == '\x1b[D': return 'LEFT'
            else: return 'ESC'
        char = char.upper()
        if char in 'WASDQH': return char
        elif char == '\x03': return 'Q'
        elif char == '\x1a': return 'Q'
        else: return None

    def get_tile_color(self, value):
        """Get color scheme for a tile value"""
        return self.tile_colors.get(value, (Colors.BG_BRIGHT_WHITE, Colors.BOLD + Colors.BLACK))

    def format_tile(self, value):
        """Format a tile with appropriate colors"""
        bg_color, fg_color = self.get_tile_color(value)
        if value == 0:
            return f"{bg_color}{fg_color}     {Colors.RESET}"
        return f"{bg_color}{fg_color}{value:^5}{Colors.RESET}"

    def clear_screen(self):
        """Clear screen using system command"""
        if self.interactive:
            os.system('clear')

    def display_board(self):
        """Display the current board state with colors"""
        self.clear_screen()
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{'=' * 55}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}🎮 {Colors.BRIGHT_YELLOW}2048 GAME{Colors.BRIGHT_MAGENTA} 🎮{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{'=' * 55}{Colors.RESET}")

        score_color = Colors.BRIGHT_GREEN if self.logic.score < 1000 else Colors.BRIGHT_YELLOW if self.logic.score < 5000 else Colors.BRIGHT_RED
        print(f"{Colors.BOLD}Score: {score_color}{self.logic.score}{Colors.RESET}", end="")
        if self.high_scores["scores"]:
            current_high = self.high_scores["scores"][0]["score"]
            print(f"  |  High Score: {Colors.BRIGHT_CYAN}{current_high}{Colors.RESET}", end="")
            if self.logic.score > 0 and self.is_new_high_score(self.logic.score):
                rank = self.get_rank(self.logic.score)
                if rank == 1:
                    print(f"  |  {Colors.BOLD}{Colors.BRIGHT_YELLOW}🔥 NEW RECORD! 🔥{Colors.RESET}", end="")
                else:
                    print(f"  |  {Colors.BRIGHT_GREEN}#{rank} High Score!{Colors.RESET}", end="")
        print()
        print(f"{Colors.BRIGHT_BLUE}Use {Colors.BRIGHT_WHITE}WASD{Colors.BRIGHT_BLUE} or {Colors.BRIGHT_WHITE}Arrow Keys{Colors.BRIGHT_BLUE} • {Colors.BRIGHT_RED}Q{Colors.BRIGHT_BLUE} to quit • {Colors.BRIGHT_MAGENTA}H{Colors.BRIGHT_BLUE} for high scores{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'-' * 55}{Colors.RESET}")
        border_color = Colors.BRIGHT_WHITE
        print(f"{border_color}┌─────┬─────┬─────┬─────┐{Colors.RESET}")
        for i, row in enumerate(self.logic.board):
            print(f"{border_color}│{Colors.RESET}", end="")
            for cell in row:
                print(self.format_tile(cell), end=f"{border_color}│{Colors.RESET}")
            print()
            if i < 3:
                print(f"{border_color}├─────┼─────┼─────┼─────┤{Colors.RESET}")
        print(f"{border_color}└─────┴─────┴─────┴─────┘{Colors.RESET}")
        if self.logic.won and not self.logic.game_over:
            print(f"\n{Colors.BOLD}{Colors.BRIGHT_YELLOW}🎉 Congratulations! You reached 2048! 🎉{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}Keep playing to get an even higher score!{Colors.RESET}")
        elif self.logic.game_over:
            print(f"\n{Colors.BOLD}{Colors.BRIGHT_RED}💀 Game Over! No more moves available.{Colors.RESET}")
            final_score_color = Colors.BRIGHT_YELLOW
            if self.is_new_high_score(self.logic.score):
                final_score_color = Colors.BRIGHT_GREEN
                rank = self.get_rank(self.logic.score)
                if rank == 1:
                    print(f"{Colors.BOLD}{Colors.BRIGHT_YELLOW}🏆 NEW HIGH SCORE RECORD! 🏆{Colors.RESET}")
                else:
                    print(f"{Colors.BRIGHT_GREEN}🎯 New High Score #{rank}! 🎯{Colors.RESET}")
            print(f"Final Score: {final_score_color}{self.logic.score}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'-' * 55}{Colors.RESET}")
        if not self.logic.game_over:
            print(f"{Colors.DIM}Press a key to move...{Colors.RESET}")
        print()

    def show_welcome_screen(self):
        """Display colorful welcome screen"""
        self.clear_screen()
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}🌟 {Colors.BRIGHT_YELLOW}TERMINAL 2048!{Colors.BRIGHT_MAGENTA} 🌟{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{'=' * 60}{Colors.RESET}")
        print(f"\n{Colors.BRIGHT_WHITE}Goal:{Colors.RESET} {Colors.BRIGHT_GREEN}Combine tiles to reach 2048!{Colors.RESET}")
        print(f"\n{Colors.BRIGHT_WHITE}Controls:{Colors.RESET}")
        print(f"  {Colors.BRIGHT_BLUE}W{Colors.RESET}/{Colors.BRIGHT_BLUE}↑{Colors.RESET} - Up    {Colors.BRIGHT_BLUE}S{Colors.RESET}/{Colors.BRIGHT_BLUE}↓{Colors.RESET} - Down")
        print(f"  {Colors.BRIGHT_BLUE}A{Colors.RESET}/{Colors.BRIGHT_BLUE}←{Colors.RESET} - Left  {Colors.BRIGHT_BLUE}D{Colors.RESET}/{Colors.BRIGHT_BLUE}→{Colors.RESET} - Right")
        print(f"  {Colors.BRIGHT_RED}Q{Colors.RESET} - Quit  {Colors.BRIGHT_MAGENTA}H{Colors.RESET} - High Scores")
        print(f"\n{Colors.BRIGHT_YELLOW}✨ 2048 is a popular puzzle game where players combine\n✨ tiles with numerical values to create a single tile\n✨ with the value of 2048.\n✨ The game requires strategic thinking and planning\n✨ to achieve the goal.{Colors.RESET}")
        if self.high_scores["scores"]:
            current_high = self.high_scores["scores"][0]["score"]
            print(f"\n{Colors.BRIGHT_CYAN}Current High Score: {Colors.BRIGHT_WHITE}{current_high}{Colors.RESET}")
        print(f"\n{Colors.DIM}Press any key to start...{Colors.RESET}")

    def show_final_score_screen(self):
        """Show final score and high score information"""
        self.clear_screen()
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_YELLOW}🎮 GAME OVER 🎮{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{'=' * 60}{Colors.RESET}")
        highest_tile = max(max(row) for row in self.logic.board)
        print(f"\n{Colors.BRIGHT_WHITE}Final Score: {Colors.BRIGHT_YELLOW}{self.logic.score}{Colors.RESET}")
        print(f"{Colors.BRIGHT_WHITE}Highest Tile: {Colors.BRIGHT_CYAN}{highest_tile}{Colors.RESET}")
        if self.is_new_high_score(self.logic.score):
            self.add_high_score(self.logic.score)
            rank = self.get_rank(self.logic.score)
            if rank == 1:
                print(f"\n{Colors.BOLD}{Colors.BRIGHT_YELLOW}🏆 CONGRATULATIONS! NEW HIGH SCORE RECORD! 🏆{Colors.RESET}")
            else:
                print(f"\n{Colors.BRIGHT_GREEN}🎯 Congratulations! New High Score #{rank}! 🎯{Colors.RESET}")
        else:
            if self.high_scores["scores"]:
                print(f"\n{Colors.BRIGHT_CYAN}High Score to Beat: {Colors.BRIGHT_WHITE}{self.high_scores['scores'][0]['score']}{Colors.RESET}")
        self.display_high_scores()
        print(f"\n{Colors.BRIGHT_GREEN}Thanks for playing!{Colors.RESET}")
        print(f"{Colors.DIM}Press any key to exit...{Colors.RESET}")

    def play(self):
        """Main game loop"""
        try:
            self.show_welcome_screen()
            self.get_key()
            while not self.logic.game_over and self.logic.can_move():
                self.display_board()
                key = self.get_key()
                moved = False
                if key in ['W', 'UP']: moved = self.logic.move_up()
                elif key in ['S', 'DOWN']: moved = self.logic.move_down()
                elif key in ['A', 'LEFT']: moved = self.logic.move_left()
                elif key in ['D', 'RIGHT']: moved = self.logic.move_right()
                elif key == 'H':
                    self.clear_screen()
                    self.display_high_scores()
                    print(f"\n{Colors.DIM}Press any key to continue...{Colors.RESET}")
                    self.get_key()
                    continue
                elif key == 'Q':
                    break
                if moved:
                    self.logic.add_random_tile()
            if not self.logic.can_move():
                self.logic.game_over = True
            if self.logic.game_over:
                self.show_final_score_screen()
            else:
                self.display_board()
                print(f"\n{Colors.BRIGHT_CYAN}Thanks for playing!{Colors.RESET}")
                print(f"{Colors.DIM}Press any key to exit...{Colors.RESET}")
            self.get_key()
        except KeyboardInterrupt:
            pass
        finally:
            if self.interactive:
                self.restore_terminal()
                print(f"\n{Colors.BRIGHT_GREEN}Game ended. Thanks for playing!{Colors.RESET}")

def main():
    """Start the game"""
    try:
        game = GameUI()
        game.play()
    except Exception as e:
        print(f"\n{Colors.BRIGHT_RED}An error occurred: {e}{Colors.RESET}")
    finally:
        try:
            os.system('stty sane')
        except:
            pass
