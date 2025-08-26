import unittest
from unittest.mock import patch
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.core import GameLogic

class TestGameLogic(unittest.TestCase):

    def setUp(self):
        """Set up a new GameLogic instance for each test."""
        # We can't just instantiate GameLogic because its __init__ calls add_random_tile.
        # For most tests, we want a controlled board, so we'll create an instance
        # and then manually override the board.
        self.game = GameLogic()

    def test_move_left(self):
        """Test the move_left functionality."""
        # Test case 1: Simple merge
        self.game.board = [
            [2, 2, 0, 0],
            [4, 0, 4, 0],
            [8, 8, 8, 8],
            [2, 4, 8, 16]
        ]
        self.game.score = 0
        moved = self.game.move_left()
        self.assertTrue(moved)
        self.assertEqual(self.game.board[0], [4, 0, 0, 0])
        self.assertEqual(self.game.board[1], [8, 0, 0, 0])
        self.assertEqual(self.game.board[2], [16, 16, 0, 0])
        self.assertEqual(self.game.board[3], [2, 4, 8, 16])
        self.assertEqual(self.game.score, 4 + 8 + 16 + 16)

        # Test case 2: No move possible
        self.game.board = [
            [2, 4, 8, 16],
            [16, 8, 4, 2],
            [2, 4, 8, 16],
            [16, 8, 4, 2]
        ]
        moved = self.game.move_left()
        self.assertFalse(moved)

    def test_move_right(self):
        """Test the move_right functionality."""
        self.game.board = [
            [2, 2, 0, 0],
            [4, 0, 4, 0],
            [8, 8, 8, 8],
            [16, 8, 4, 2]
        ]
        self.game.score = 0
        moved = self.game.move_right()
        self.assertTrue(moved)
        self.assertEqual(self.game.board[0], [0, 0, 0, 4])
        self.assertEqual(self.game.board[1], [0, 0, 0, 8])
        self.assertEqual(self.game.board[2], [0, 0, 16, 16])
        self.assertEqual(self.game.board[3], [16, 8, 4, 2])
        self.assertEqual(self.game.score, 4 + 8 + 16 + 16)

    def test_move_up(self):
        """Test the move_up functionality."""
        self.game.board = [
            [2, 4, 8, 16],
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.score = 0
        moved = self.game.move_up()
        self.assertTrue(moved)
        expected_board = [
            [4, 8, 16, 32],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board, expected_board)
        self.assertEqual(self.game.score, 4 + 8 + 16 + 32)

    def test_move_down(self):
        """Test the move_down functionality."""
        self.game.board = [
            [2, 4, 8, 16],
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.score = 0
        moved = self.game.move_down()
        self.assertTrue(moved)
        expected_board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [4, 8, 16, 32]
        ]
        self.assertEqual(self.game.board, expected_board)
        self.assertEqual(self.game.score, 4 + 8 + 16 + 32)

    def test_can_move(self):
        """Test the can_move logic."""
        # Test case 1: Board with empty cells
        self.game.board = [[2, 4, 8, 16], [16, 8, 4, 2], [2, 4, 8, 16], [16, 8, 4, 0]]
        self.assertTrue(self.game.can_move())

        # Test case 2: Full board with possible horizontal move
        self.game.board = [[2, 2, 8, 16], [16, 8, 4, 2], [2, 4, 8, 16], [16, 8, 4, 2]]
        self.assertTrue(self.game.can_move())

        # Test case 3: Full board with possible vertical move
        self.game.board = [[2, 4, 8, 16], [2, 8, 4, 2], [4, 4, 8, 16], [16, 8, 4, 2]]
        self.assertTrue(self.game.can_move())

        # Test case 4: Full board with no possible moves
        self.game.board = [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]]
        self.assertFalse(self.game.can_move())

    @patch('random.choice')
    @patch('random.random')
    def test_add_random_tile(self, mock_random, mock_choice):
        """Test adding a random tile to the board."""
        # Make the board empty
        self.game.board = [[0] * 4 for _ in range(4)]

        # Scenario 1: Add a '2' tile at position (0, 0)
        mock_choice.return_value = (0, 0)
        mock_random.return_value = 0.8  # This will result in a 2
        self.game.add_random_tile()
        self.assertEqual(self.game.board[0][0], 2)

        # Count non-zero tiles
        non_zero_tiles = sum(cell != 0 for row in self.game.board for cell in row)
        self.assertEqual(non_zero_tiles, 1)

        # Scenario 2: Add a '4' tile at position (3, 3)
        mock_choice.return_value = (3, 3)
        mock_random.return_value = 0.95 # This will result in a 4
        self.game.add_random_tile()
        self.assertEqual(self.game.board[3][3], 4)

        non_zero_tiles = sum(cell != 0 for row in self.game.board for cell in row)
        self.assertEqual(non_zero_tiles, 2)

if __name__ == '__main__':
    unittest.main()
