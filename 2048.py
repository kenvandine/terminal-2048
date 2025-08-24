#!/usr/bin/env python3
"""
Terminal-based 2048 Game for Linux - Colorful Edition
Use WASD or arrow keys to move tiles
Goal: Reach 2048!
"""

import random
import os
import sys
import termios

class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Foreground colors
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
    
    # Background colors
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

class Game2048:
    def __init__(self):
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        self.setup_terminal()
        self.add_random_tile()
        self.add_random_tile()
        
        # Color scheme for different tile values
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
    
    def setup_terminal(self):
        """Setup terminal for immediate key detection"""
        new_settings = termios.tcgetattr(self.fd)
        new_settings[3] = new_settings[3] & ~(termios.ICANON | termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSADRAIN, new_settings)
    
    def restore_terminal(self):
        """Restore normal terminal behavior"""
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
    
    def get_char(self):
        """Get a single character from stdin"""
        return sys.stdin.read(1)
    
    def get_key(self):
        """Get and process keyboard input"""
        char = self.get_char()
        
        if char == '\x1b':  # Escape sequence (arrow keys)
            char += self.get_char()  # Should be '['
            char += self.get_char()  # Direction key
            
            if char == '\x1b[A':
                return 'UP'
            elif char == '\x1b[B':
                return 'DOWN' 
            elif char == '\x1b[C':
                return 'RIGHT'
            elif char == '\x1b[D':
                return 'LEFT'
            else:
                return 'ESC'
        
        # Regular keys
        char = char.upper()
        if char in 'WASDQ':
            return char
        elif char == '\x03':  # Ctrl+C
            return 'Q'
        elif char == '\x1a':  # Ctrl+Z
            return 'Q'
        else:
            return None
    
    def get_tile_color(self, value):
        """Get color scheme for a tile value"""
        if value in self.tile_colors:
            return self.tile_colors[value]
        else:
            # For values higher than 8192, use a rainbow effect
            return (Colors.BG_BRIGHT_WHITE, Colors.BOLD + Colors.BLACK)
    
    def format_tile(self, value):
        """Format a tile with appropriate colors"""
        if value == 0:
            bg_color, fg_color = self.get_tile_color(0)
            return f"{bg_color}{fg_color}     {Colors.RESET}"
        else:
            bg_color, fg_color = self.get_tile_color(value)
            return f"{bg_color}{fg_color}{value:^5}{Colors.RESET}"
    
    def add_random_tile(self):
        """Add a random tile (2 or 4) to an empty position"""
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4
    
    def clear_screen(self):
        """Clear screen using system command"""
        os.system('clear')
    
    def display_board(self):
        """Display the current board state with colors"""
        self.clear_screen()
        
        # Header with gradient effect
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{'=' * 55}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}🎮 {Colors.BRIGHT_YELLOW}2048 GAME{Colors.BRIGHT_MAGENTA} 🎮{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{'=' * 55}{Colors.RESET}")
        
        # Score display
        score_color = Colors.BRIGHT_GREEN if self.score < 1000 else Colors.BRIGHT_YELLOW if self.score < 5000 else Colors.BRIGHT_RED
        print(f"{Colors.BOLD}Score: {score_color}{self.score}{Colors.RESET}")
        
        # Controls info
        print(f"{Colors.BRIGHT_BLUE}Use {Colors.BRIGHT_WHITE}WASD{Colors.BRIGHT_BLUE} or {Colors.BRIGHT_WHITE}Arrow Keys{Colors.BRIGHT_BLUE} • {Colors.BRIGHT_RED}Q{Colors.BRIGHT_BLUE} to quit{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'-' * 55}{Colors.RESET}")
        
        # Game board with colorful borders
        border_color = Colors.BRIGHT_WHITE
        print(f"{border_color}┌─────┬─────┬─────┬─────┐{Colors.RESET}")
        
        for i, row in enumerate(self.board):
            print(f"{border_color}│{Colors.RESET}", end="")
            for cell in row:
                print(self.format_tile(cell), end=f"{border_color}│{Colors.RESET}")
            print()
            if i < 3:
                print(f"{border_color}├─────┼─────┼─────┼─────┤{Colors.RESET}")
        
        print(f"{border_color}└─────┴─────┴─────┴─────┘{Colors.RESET}")
        
        # Game status messages
        if self.won and not self.game_over:
            print(f"\n{Colors.BOLD}{Colors.BRIGHT_YELLOW}🎉 Congratulations! You reached 2048! 🎉{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}Keep playing to get an even higher score!{Colors.RESET}")
        elif self.game_over:
            print(f"\n{Colors.BOLD}{Colors.BRIGHT_RED}💀 Game Over! No more moves available.{Colors.RESET}")
            print(f"{Colors.BRIGHT_YELLOW}Final Score: {Colors.BRIGHT_WHITE}{self.score}{Colors.RESET}")
        
        print(f"{Colors.BRIGHT_CYAN}{'-' * 55}{Colors.RESET}")
        if not self.game_over:
            print(f"{Colors.DIM}Press a key to move...{Colors.RESET}")
        print()  # Extra newline for better spacing
    
    def move_left(self):
        """Move all tiles left"""
        moved = False
        for i in range(4):
            # Remove zeros
            row = [cell for cell in self.board[i] if cell != 0]
            
            # Merge tiles
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
            
            # Pad with zeros
            merged.extend([0] * (4 - len(merged)))
            
            # Check if move changed anything
            if self.board[i] != merged:
                moved = True
            
            self.board[i] = merged
        
        return moved
    
    def move_right(self):
        """Move all tiles right"""
        for i in range(4):
            self.board[i] = self.board[i][::-1]
        moved = self.move_left()
        for i in range(4):
            self.board[i] = self.board[i][::-1]
        return moved
    
    def move_up(self):
        """Move all tiles up"""
        self.board = list(map(list, zip(*self.board)))
        moved = self.move_left()
        self.board = list(map(list, zip(*self.board)))
        return moved
    
    def move_down(self):
        """Move all tiles down"""
        self.board = list(map(list, zip(*self.board)))
        moved = self.move_right()
        self.board = list(map(list, zip(*self.board)))
        return moved
    
    def can_move(self):
        """Check if any moves are possible"""
        # Check for empty cells
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return True
        
        # Check for possible merges
        for i in range(4):
            for j in range(4):
                current = self.board[i][j]
                # Check right neighbor
                if j < 3 and self.board[i][j + 1] == current:
                    return True
                # Check bottom neighbor
                if i < 3 and self.board[i + 1][j] == current:
                    return True
        
        return False
    
    def show_welcome_screen(self):
        """Display colorful welcome screen"""
        self.clear_screen()
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}🌟 {Colors.BRIGHT_YELLOW}WELCOME TO COLORFUL 2048!{Colors.BRIGHT_MAGENTA} 🌟{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{'=' * 60}{Colors.RESET}")
        print(f"\n{Colors.BRIGHT_WHITE}Goal:{Colors.RESET} {Colors.BRIGHT_GREEN}Combine tiles to reach 2048!{Colors.RESET}")
        print(f"\n{Colors.BRIGHT_WHITE}Controls:{Colors.RESET}")
        print(f"  {Colors.BRIGHT_BLUE}W{Colors.RESET}/{Colors.BRIGHT_BLUE}↑{Colors.RESET} - Up    {Colors.BRIGHT_BLUE}S{Colors.RESET}/{Colors.BRIGHT_BLUE}↓{Colors.RESET} - Down")
        print(f"  {Colors.BRIGHT_BLUE}A{Colors.RESET}/{Colors.BRIGHT_BLUE}←{Colors.RESET} - Left  {Colors.BRIGHT_BLUE}D{Colors.RESET}/{Colors.BRIGHT_BLUE}→{Colors.RESET} - Right")
        print(f"  {Colors.BRIGHT_RED}Q{Colors.RESET} - Quit")
        print(f"\n{Colors.BRIGHT_YELLOW}✨ Each tile value has its own unique color! ✨{Colors.RESET}")
        print(f"\n{Colors.DIM}Press any key to start...{Colors.RESET}")
    
    def play(self):
        """Main game loop"""
        try:
            self.show_welcome_screen()
            
            # Wait for first key
            self.get_key()
            
            while not self.game_over and self.can_move():
                self.display_board()
                
                # Get user input
                key = self.get_key()
                
                moved = False
                
                # Handle movement keys
                if key in ['W', 'UP']:
                    moved = self.move_up()
                elif key in ['S', 'DOWN']:
                    moved = self.move_down()
                elif key in ['A', 'LEFT']:
                    moved = self.move_left()
                elif key in ['D', 'RIGHT']:
                    moved = self.move_right()
                elif key == 'Q':
                    break
                
                if moved:
                    self.add_random_tile()
            
            # Game over
            if not self.can_move():
                self.game_over = True
            
            self.display_board()
            if not self.game_over:
                print(f"\n{Colors.BRIGHT_CYAN}Thanks for playing!{Colors.RESET}")
            else:
                print(f"\n{Colors.BRIGHT_YELLOW}Game Over! Thanks for playing!{Colors.RESET}")
            
            print(f"{Colors.DIM}Press any key to exit...{Colors.RESET}")
            self.get_key()
                
        except KeyboardInterrupt:
            pass
        finally:
            self.restore_terminal()
            print(f"\n{Colors.BRIGHT_GREEN}Game ended. Thanks for playing!{Colors.RESET}")

def main():
    """Start the game"""
    try:
        game = Game2048()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.BRIGHT_RED}Game interrupted!{Colors.RESET}")
    except Exception as e:
        # Make sure terminal is restored even if there's an error
        try:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, 
                            termios.tcgetattr(sys.stdin.fileno()))
        except:
            pass
        print(f"\n{Colors.BRIGHT_RED}An error occurred: {e}{Colors.RESET}")
    finally:
        # Ensure terminal is always restored
        try:
            os.system('stty sane')  # Fallback terminal reset
        except:
            pass

if __name__ == "__main__":
    main()
