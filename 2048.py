#!/usr/bin/env python3
"""
Terminal-based 2048 Game for Linux
Use WASD or arrow keys to move tiles
Goal: Reach 2048!
"""

import random
import os
import sys
import termios

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
    
    def setup_terminal(self):
        """Setup terminal for immediate key detection"""
        # Set terminal to cbreak mode manually using termios
        new_settings = termios.tcgetattr(self.fd)
        # Disable canonical mode and echo
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
        """Display the current board state"""
        self.clear_screen()
        print("=" * 50)
        print("🎮 2048 GAME 🎮")
        print("=" * 50)
        print(f"Score: {self.score}")
        print("Use WASD or Arrow Keys • Q to quit")
        print("-" * 50)
        
        for i, row in enumerate(self.board):
            print("│", end="")
            for cell in row:
                if cell == 0:
                    print("     ", end="│")
                else:
                    print(f"{cell:^5}", end="│")
            print()
            if i < 3:
                print("├─────┼─────┼─────┼─────┤")
        print("└─────┴─────┴─────┴─────┘")
        
        if self.won and not self.game_over:
            print("🎉 Congratulations! You reached 2048! 🎉")
            print("Keep playing to get an even higher score!")
        elif self.game_over:
            print("💀 Game Over! No more moves available.")
            print(f"Final Score: {self.score}")
        
        print("-" * 50)
        if not self.game_over:
            print("Press a key to move...")
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
    
    def play(self):
        """Main game loop"""
        try:
            self.clear_screen()
            print("Welcome to 2048!")
            print("Goal: Combine tiles to reach 2048!")
            print("Controls:")
            print("  W/↑ - Up    S/↓ - Down")
            print("  A/← - Left  D/→ - Right")
            print("  Q - Quit")
            print("\nPress any key to start...")
            
            # Wait for first key
            self.get_key()
            
            while not self.game_over and self.can_move():
                self.display_board()
                
                # Get user input - this will block until a key is pressed
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
                print("\nThanks for playing!")
            else:
                print("Game Over! Thanks for playing!")
            
            print("Press any key to exit...")
            self.get_key()
                
        except KeyboardInterrupt:
            pass
        finally:
            self.restore_terminal()
            print("\nGame ended. Thanks for playing!")

def main():
    """Start the game"""
    try:
        game = Game2048()
        game.play()
    except KeyboardInterrupt:
        print("\n\nGame interrupted!")
    except Exception as e:
        # Make sure terminal is restored even if there's an error
        try:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, 
                            termios.tcgetattr(sys.stdin.fileno()))
        except:
            pass
        print(f"\nAn error occurred: {e}")
    finally:
        # Ensure terminal is always restored
        try:
            os.system('stty sane')  # Fallback terminal reset
        except:
            pass

if __name__ == "__main__":
    main()
