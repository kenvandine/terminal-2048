import unittest
from unittest.mock import patch
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.core import GameLogic

class TestIntegration(unittest.TestCase):

    def setUp(self):
        """Set up a new GameLogic instance for each test."""
        # By instantiating GameLogic here, we get the two initial random tiles.
        # For integration tests, this is often fine as we're testing the flow.
        # However, for specific scenarios like winning or losing, we'll override the board.
        self.game = GameLogic()

    def test_win_scenario(self):
        """Test a sequence of moves leading to a win."""
        self.game.board = [
            [1024, 1024, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.score = 0
        self.game.won = False

        # The move that should trigger the win condition
        moved = self.game.move_left()

        self.assertTrue(moved)
        self.assertTrue(self.game.won, "Game should be marked as won")
        self.assertEqual(self.game.board[0], [2048, 0, 0, 0])
        self.assertEqual(self.game.score, 2048)

    def test_game_over_scenario(self):
        """Test a board state where no moves are possible."""
        # A full board with no adjacent matching tiles
        self.game.board = [
            [2, 4, 8, 16],
            [16, 8, 4, 2],
            [2, 4, 8, 16],
            [16, 8, 4, 2]
        ]

        # Verify that the game recognizes there are no more moves
        can_move = self.game.can_move()
        self.assertFalse(can_move, "Game should be over (no moves possible)")

        # Try to make a move and ensure the board does not change
        board_before = [row[:] for row in self.game.board]
        self.game.move_left()
        self.assertEqual(self.game.board, board_before, "Board should not change after a move when game is over")
        self.game.move_right()
        self.assertEqual(self.game.board, board_before, "Board should not change after a move when game is over")
        self.game.move_up()
        self.assertEqual(self.game.board, board_before, "Board should not change after a move when game is over")
        self.game.move_down()
        self.assertEqual(self.game.board, board_before, "Board should not change after a move when game is over")

    @patch('random.choice')
    @patch('random.random')
    def test_short_gameplay_sequence(self, mock_random, mock_choice):
        """Simulate a short, deterministic sequence of moves."""
        # Start with an empty board
        self.game.board = [[0] * 4 for _ in range(4)]
        self.game.score = 0

        # Mock the random tile generation for a predictable game
        # Sequence of new tiles: 2 at (0,0), 2 at (1,0), 4 at (2,2)
        mock_choice.side_effect = [(0, 0), (1, 0), (2, 2)]
        mock_random.side_effect = [0.1, 0.1, 0.95] # two 2s, one 4

        # Add the first two tiles
        self.game.add_random_tile()
        self.game.add_random_tile()

        initial_board = [
            [2, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board, initial_board)

        # Move up -> should merge the two 2s
        self.game.move_up()
        board_after_move_up = [
            [4, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board, board_after_move_up)
        self.assertEqual(self.game.score, 4)

        # A new tile should be added. Let's say it's a 4 at (2,2)
        self.game.add_random_tile()
        board_after_add = [
            [4, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 4, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board, board_after_add)

        # Move right
        self.game.move_right()
        board_after_move = [
            [0, 0, 0, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 4],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board, board_after_move)
        # Score should still be 4, as no merge happened
        self.assertEqual(self.game.score, 4)

if __name__ == '__main__':
    unittest.main()
