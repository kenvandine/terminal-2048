use chrono::Local;
use serde::{Serialize, Deserialize};
use std::fs;
use std::io;
use std::path::PathBuf;

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct ScoreEntry {
    pub score: u32,
    pub date: String,
    pub highest_tile: u16,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct HighScores {
    pub scores: Vec<ScoreEntry>,
}

impl HighScores {
    pub fn new() -> Self {
        Self { scores: Vec::new() }
    }
}

fn get_high_scores_path() -> Option<PathBuf> {
    dirs::home_dir().map(|mut path| {
        path.push(".2048_high_scores.json");
        path
    })
}

pub fn load_high_scores() -> HighScores {
    if let Some(path) = get_high_scores_path() {
        if path.exists() {
            let data = fs::read_to_string(path).unwrap_or_default();
            return serde_json::from_str(&data).unwrap_or_else(|_| HighScores::new());
        }
    }
    HighScores::new()
}

pub fn save_high_scores(high_scores: &HighScores) -> io::Result<()> {
    if let Some(path) = get_high_scores_path() {
        let data = serde_json::to_string_pretty(high_scores)?;
        fs::write(path, data)?;
    }
    Ok(())
}

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

pub fn is_new_high_score(high_scores: &HighScores, score: u32) -> bool {
    if high_scores.scores.len() < 10 {
        return true;
    }
    score > high_scores.scores.last().map_or(0, |s| s.score)
}
