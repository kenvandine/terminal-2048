use rand::Rng;

/// Represents the state and logic of the 2048 game.
///
/// This struct holds the game board, the player's score, and the game's
/// status (e.g., whether it's over or won).
pub struct GameLogic {
    /// The 4x4 grid representing the game board. Each cell contains a `u16`
    /// value, where 0 represents an empty cell.
    pub board: [[u16; 4]; 4],
    /// The player's current score.
    pub score: u32,
    /// A boolean flag indicating whether the game is over (i.e., no more
    /// valid moves can be made).
    pub game_over: bool,
    /// A boolean flag indicating whether the player has won (i.e., created a
    /// 2048 tile).
    pub won: bool,
}

impl GameLogic {
    /// Creates a new `GameLogic` instance.
    ///
    /// The game starts with an empty board, a score of 0, and two randomly
    /// placed tiles.
    ///
    /// # Returns
    ///
    /// A new `GameLogic` instance.
    pub fn new() -> Self {
        let board = [[0; 4]; 4];
        let mut logic = Self {
            board,
            score: 0,
            game_over: false,
            won: false,
        };
        logic.add_random_tile();
        logic.add_random_tile();
        logic
    }

    /// Adds a new random tile (either a 2 or a 4) to an empty cell on the board.
    ///
    /// There's a 90% chance of the new tile being a 2, and a 10% chance of it
    /// being a 4.
    pub fn add_random_tile(&mut self) {
        let mut empty_cells = Vec::new();
        for r in 0..4 {
            for c in 0..4 {
                if self.board[r][c] == 0 {
                    empty_cells.push((r, c));
                }
            }
        }

        if let Some(&(r, c)) = empty_cells.get(rand::thread_rng().gen_range(0..empty_cells.len())) {
            self.board[r][c] = if rand::thread_rng().gen_bool(0.9) { 2 } else { 4 };
        }
    }

    /// Handles the logic for moving tiles to the left.
    ///
    /// This function iterates through each row, slides all tiles to the left,
    /// merges adjacent tiles of the same value, and updates the score.
    ///
    /// # Returns
    ///
    /// `true` if any tiles were moved or merged, `false` otherwise.
    pub fn move_left(&mut self) -> bool {
        let mut moved = false;
        for i in 0..4 {
            let row = self.board[i];
            let row_without_zeros: Vec<u16> = row.iter().filter(|&&c| c != 0).cloned().collect();
            let mut merged_row: Vec<u16> = Vec::new();
            let mut skip = false;

            for j in 0..row_without_zeros.len() {
                if skip {
                    skip = false;
                    continue;
                }
                if j < row_without_zeros.len() - 1 && row_without_zeros[j] == row_without_zeros[j + 1] {
                    let new_tile = row_without_zeros[j] * 2;
                    merged_row.push(new_tile);
                    self.score += new_tile as u32;
                    if new_tile == 2048 {
                        self.won = true;
                    }
                    skip = true;
                } else {
                    merged_row.push(row_without_zeros[j]);
                }
            }

            let mut new_row = [0; 4];
            for (idx, &val) in merged_row.iter().enumerate() {
                new_row[idx] = val;
            }

            if self.board[i] != new_row {
                moved = true;
                self.board[i] = new_row;
            }
        }
        moved
    }

    /// Handles the logic for moving tiles to the right.
    ///
    /// This is implemented by reversing each row, performing a `move_left`
    /// operation, and then reversing the rows back.
    ///
    /// # Returns
    ///
    /// `true` if the board state changed, `false` otherwise.
    pub fn move_right(&mut self) -> bool {
        let original_board = self.board;
        for r in 0..4 {
            self.board[r].reverse();
        }
        self.move_left();
        for r in 0..4 {
            self.board[r].reverse();
        }
        self.board != original_board
    }

    /// Transposes the game board.
    ///
    /// This helper function is used to implement `move_up` and `move_down`
    /// by reusing the `move_left` and `move_right` logic.
    fn transpose(&mut self) {
        for r in 0..4 {
            for c in r..4 {
                let temp = self.board[r][c];
                self.board[r][c] = self.board[c][r];
                self.board[c][r] = temp;
            }
        }
    }

    /// Handles the logic for moving tiles up.
    ///
    /// This is implemented by transposing the board, performing a `move_left`
    /// operation, and then transposing the board back.
    ///
    /// # Returns
    ///
    /// `true` if the board state changed, `false` otherwise.
    pub fn move_up(&mut self) -> bool {
        let original_board = self.board;
        self.transpose();
        self.move_left();
        self.transpose();
        self.board != original_board
    }

    /// Handles the logic for moving tiles down.
    ///
    /// This is implemented by transposing the board, performing a `move_right`
    /// operation, and then transposing the board back.
    ///
    /// # Returns
    ///
    /// `true` if the board state changed, `false` otherwise.
    pub fn move_down(&mut self) -> bool {
        let original_board = self.board;
        self.transpose();
        self.move_right();
        self.transpose();
        self.board != original_board
    }

    /// Checks if there are any valid moves left on the board.
    ///
    /// A move is possible if there is an empty cell or if there are adjacent
    /// tiles with the same value.
    ///
    /// # Returns
    ///
    /// `true` if a move can be made, `false` otherwise.
    pub fn can_move(&self) -> bool {
        for r in 0..4 {
            for c in 0..4 {
                if self.board[r][c] == 0 {
                    return true;
                }
                if c < 3 && self.board[r][c] == self.board[r][c + 1] {
                    return true;
                }
                if r < 3 && self.board[r][c] == self.board[r + 1][c] {
                    return true;
                }
            }
        }
        false
    }
}
