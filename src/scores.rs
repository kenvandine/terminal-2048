use chrono::Local;
use serde::{Serialize, Deserialize};
use std::fs;
use std::io;
use std::path::PathBuf;

/// Represents a single entry in the high scores list.
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct ScoreEntry {
    /// The score achieved in the game.
    pub score: u32,
    /// The date and time when the score was achieved.
    pub date: String,
    /// The highest tile value achieved in the game.
    pub highest_tile: u16,
}

/// Represents the list of high scores.
#[derive(Serialize, Deserialize, Debug)]
pub struct HighScores {
    /// A vector of `ScoreEntry` instances, sorted in descending order of score.
    pub scores: Vec<ScoreEntry>,
}

impl HighScores {
    /// Creates a new, empty `HighScores` instance.
    ///
    /// # Returns
    ///
    /// A new `HighScores` instance with an empty vector of scores.
    pub fn new() -> Self {
        Self { scores: Vec::new() }
    }
}

/// Gets the path to the high scores file.
///
/// The high scores are stored in a JSON file named `.2048_high_scores.json`
/// in the user's home directory.
///
/// # Returns
///
/// An `Option<PathBuf>` containing the path to the high scores file, or `None`
/// if the home directory cannot be determined.
fn get_high_scores_path() -> Option<PathBuf> {
    dirs::home_dir().map(|mut path| {
        path.push(".2048_high_scores.json");
        path
    })
}

/// Loads the high scores from the file system.
///
/// If the high scores file does not exist or fails to parse, a new, empty
/// `HighScores` instance is returned.
///
/// # Returns
///
/// A `HighScores` instance.
pub fn load_high_scores() -> HighScores {
    if let Some(path) = get_high_scores_path() {
        if path.exists() {
            let data = fs::read_to_string(path).unwrap_or_default();
            return serde_json::from_str(&data).unwrap_or_else(|_| HighScores::new());
        }
    }
    HighScores::new()
}

/// Saves the high scores to the file system.
///
/// # Arguments
///
/// * `high_scores` - A reference to the `HighScores` instance to save.
///
/// # Returns
///
/// An `io::Result` indicating the outcome of the operation.
pub fn save_high_scores(high_scores: &HighScores) -> io::Result<()> {
    if let Some(path) = get_high_scores_path() {
        let data = serde_json::to_string_pretty(high_scores)?;
        fs::write(path, data)?;
    }
    Ok(())
}

/// Adds a new high score to the list.
///
/// The new score is added, and the list is then sorted and truncated to keep
/// only the top 10 scores. The updated list is then saved to the file system.
///
/// # Arguments
///
/// * `high_scores` - A mutable reference to the `HighScores` instance.
/// * `score` - The new score to add.
/// * `board` - The game board at the end of the game, used to determine the
///   highest tile achieved.
pub fn add_high_score(high_scores: &mut HighScores, score: u32, board: &[[u16; 4]; 4]) {
    let highest_tile = *board.iter().flat_map(|row| row.iter()).max().unwrap_or(&0);
    let new_score = ScoreEntry {
        score,
        date: Local::now().format("%Y-%m-%d %H:%M:%S").to_string(),
        highest_tile,
    };

    high_scores.scores.push(new_score);
    high_scores.scores.sort_by(|a, b| b.score.cmp(&a.score));
    high_scores.scores.truncate(10);
    save_high_scores(high_scores).unwrap_or_default();
}

/// Checks if a given score qualifies as a new high score.
///
/// A score is considered a high score if it is greater than the lowest score
/// in the top 10, or if there are fewer than 10 scores in the list.
///
/// # Arguments
///
/// * `high_scores` - A reference to the `HighScores` instance.
/// * `score` - The score to check.
///
/// # Returns
///
/// `true` if the score is a new high score, `false` otherwise.
pub fn is_new_high_score(high_scores: &HighScores, score: u32) -> bool {
    if high_scores.scores.len() < 10 {
        return true;
    }
    score > high_scores.scores.last().map_or(0, |s| s.score)
}
