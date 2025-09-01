use crate::game::logic::GameLogic;
use crate::scores::{self, HighScores};
use std::io::stdout;
use crossterm::{
    event::{self, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
    style::{Attribute, Color, Print, ResetColor, SetAttribute, SetBackgroundColor, SetForegroundColor},
};

pub enum HighScoreAction {
    Continue,
    Quit,
}

pub struct GameUI {
    logic: GameLogic,
    high_scores: HighScores,
}

impl GameUI {
    pub fn new() -> Self {
        Self {
            logic: GameLogic::new(),
            high_scores: scores::load_high_scores(),
        }
    }

    pub fn show_welcome_screen(&self, stdout: &mut std::io::Stdout) -> std::io::Result<()> {
        execute!(stdout, crossterm::terminal::Clear(crossterm::terminal::ClearType::All))?;
        let mut y = 0;

        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Cyan), Print("=".repeat(60)), ResetColor)?;
        y += 1;
        execute!(stdout, crossterm::cursor::MoveTo(20, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Yellow), Print("🌟 TERMINAL 2048! 🌟"), ResetColor)?;
        y += 1;
        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Cyan), Print("=".repeat(60)), ResetColor)?;
        y += 2;

        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::White), Print("Goal:"), SetForegroundColor(Color::Green), Print(" Combine tiles to reach 2048!"), ResetColor)?;
        y += 2;

        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::White), Print("Controls:"), ResetColor)?;
        y += 1;
        execute!(stdout, crossterm::cursor::MoveTo(2, y), Print("W/↑ - Up    S/↓ - Down"))?;
        y += 1;
        execute!(stdout, crossterm::cursor::MoveTo(2, y), Print("A/← - Left  D/→ - Right"))?;
        y += 1;
        execute!(stdout, crossterm::cursor::MoveTo(2, y), Print("Q - Quit  H - High Scores"))?;
        y += 2;

        let description = [
            "✨ 2048 is a popular puzzle game where players combine",
            "✨ tiles with numerical values to create a single tile",
            "✨ with the value of 2048.",
            "✨ The game requires strategic thinking and planning",
            "✨ to achieve the goal.",
        ];
        for line in description.iter() {
            execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::Yellow), Print(line), ResetColor)?;
            y += 1;
        }
        y += 1;

        if let Some(high_score) = self.high_scores.scores.first() {
            let text = format!("Current High Score: {}", high_score.score);
            execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::Cyan), Print(&text), ResetColor)?;
            y += 2;
        }

        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::DarkGrey), Print("Press any key to start..."), ResetColor)?;

        self.wait_for_key_press()?;
        Ok(())
    }

    pub fn run(&mut self) -> std::io::Result<()> {
        let mut stdout = stdout();
        execute!(stdout, EnterAlternateScreen)?;
        enable_raw_mode()?;

        self.show_welcome_screen(&mut stdout)?;

        loop {
            self.draw_board(&mut stdout)?;

            if self.logic.game_over {
                if let HighScoreAction::Quit = self.show_final_score_screen(&mut stdout)? {
                    break;
                }
                self.logic = GameLogic::new();
                self.show_welcome_screen(&mut stdout)?;
                continue;
            }

            if let Event::Key(key_event) = event::read()? {
                let moved = match key_event.code {
                    KeyCode::Char('w') | KeyCode::Up => self.logic.move_up(),
                    KeyCode::Char('s') | KeyCode::Down => self.logic.move_down(),
                    KeyCode::Char('a') | KeyCode::Left => self.logic.move_left(),
                    KeyCode::Char('d') | KeyCode::Right => self.logic.move_right(),
                    KeyCode::Char('h') => {
                        if let HighScoreAction::Quit = self.show_high_scores(&mut stdout)? {
                            break;
                        }
                        false
                    }
                    KeyCode::Char('q') => break,
                    _ => false,
                };

                if moved {
                    self.logic.add_random_tile();
                }

                if !self.logic.can_move() {
                    self.logic.game_over = true;
                }
            }
        }

        disable_raw_mode()?;
        execute!(stdout, LeaveAlternateScreen)?;
        Ok(())
    }

    fn draw_board(&self, stdout: &mut std::io::Stdout) -> std::io::Result<()> {
        execute!(stdout, crossterm::terminal::Clear(crossterm::terminal::ClearType::All))?;
        let mut y = 0;

        // Header
        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Cyan), Print("=".repeat(55)), ResetColor)?;
        y += 1;
        execute!(stdout, crossterm::cursor::MoveTo(20, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Yellow), Print("🎮 2048 GAME 🎮"), ResetColor)?;
        y += 1;
        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Cyan), Print("=".repeat(55)), ResetColor)?;
        y += 2;

        // Score
        let score_text = format!("Score: {}", self.logic.score);
        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Green), Print(&score_text), ResetColor)?;
        if let Some(high_score) = self.high_scores.scores.first() {
            let high_score_text = format!("  |  High Score: {}", high_score.score);
            execute!(stdout, crossterm::cursor::MoveTo(score_text.chars().count() as u16, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Cyan), Print(&high_score_text), ResetColor)?;
        }
        y += 1;

        // Instructions
        execute!(stdout, crossterm::cursor::MoveTo(0, y), Print("Use WASD or Arrow Keys • Q to quit • H for high scores"))?;
        y += 1;
        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::Cyan), Print("-".repeat(55)), ResetColor)?;
        y += 1;

        // Board
        let board_y = y;
        let board_lines = [
            "┌─────┬─────┬─────┬─────┐",
            "│     │     │     │     │",
            "├─────┼─────┼─────┼─────┤",
            "│     │     │     │     │",
            "├─────┼─────┼─────┼─────┤",
            "│     │     │     │     │",
            "├─────┼─────┼─────┼─────┤",
            "│     │     │     │     │",
            "└─────┴─────┴─────┴─────┘",
        ];
        for (i, line) in board_lines.iter().enumerate() {
            execute!(stdout, crossterm::cursor::MoveTo(15, board_y + i as u16), Print(line))?;
        }

        for r in 0..4 {
            for c in 0..4 {
                if self.logic.board[r][c] != 0 {
                    let (fg, bg) = self.get_tile_colors(self.logic.board[r][c]);
                    let text = self.logic.board[r][c].to_string();
                    let tile_y = board_y + 1 + (r * 2) as u16;
                    let tile_x = 16 + c as u16 * 6;
                    execute!(stdout, crossterm::cursor::MoveTo(tile_x, tile_y), SetBackgroundColor(bg), SetForegroundColor(fg), Print(format!("{:^5}", text)), ResetColor)?;
                }
            }
        }
        y += board_lines.len() as u16;

        // Footer
        if self.logic.won && !self.logic.game_over {
            execute!(stdout, crossterm::cursor::MoveTo(0, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Yellow), Print("🎉 Congratulations! You reached 2048! 🎉"), ResetColor)?;
            y += 1;
            execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::Green), Print("Keep playing to get an even higher score!"), ResetColor)?;
        } else if self.logic.game_over {
            execute!(stdout, crossterm::cursor::MoveTo(0, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Red), Print("💀 Game Over! No more moves available."), ResetColor)?;
        }
        y += 2;

        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::Cyan), Print("-".repeat(55)), ResetColor)?;
        y += 1;

        if !self.logic.game_over {
            execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::DarkGrey), Print("Press a key to move..."), ResetColor)?;
        }

        Ok(())
    }

    fn get_tile_colors(&self, value: u16) -> (Color, Color) {
        match value {
            2 => (Color::Black, Color::White),
            4 => (Color::Black, Color::Rgb { r: 237, g: 224, b: 200 }),
            8 => (Color::White, Color::Rgb { r: 242, g: 177, b: 121 }),
            16 => (Color::White, Color::Rgb { r: 245, g: 149, b: 99 }),
            32 => (Color::White, Color::Rgb { r: 246, g: 124, b: 95 }),
            64 => (Color::White, Color::Rgb { r: 246, g: 94, b: 59 }),
            128 => (Color::White, Color::Rgb { r: 237, g: 207, b: 114 }),
            256 => (Color::White, Color::Rgb { r: 237, g: 204, b: 97 }),
            512 => (Color::White, Color::Rgb { r: 237, g: 200, b: 80 }),
            1024 => (Color::White, Color::Rgb { r: 237, g: 197, b: 63 }),
            2048 => (Color::White, Color::Rgb { r: 237, g: 194, b: 46 }),
            _ => (Color::DarkGrey, Color::Rgb { r: 205, g: 193, b: 180 }),
        }
    }

    fn show_final_score_screen(&mut self, stdout: &mut std::io::Stdout) -> std::io::Result<HighScoreAction> {
        execute!(stdout, crossterm::terminal::Clear(crossterm::terminal::ClearType::All))?;
        let mut y = 0;

        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Yellow), Print("🎮 GAME OVER 🎮"), ResetColor)?;
        y += 2;

        let is_new_high = scores::is_new_high_score(&self.high_scores, self.logic.score);
        if is_new_high {
            scores::add_high_score(&mut self.high_scores, self.logic.score, &self.logic.board);
            execute!(stdout, crossterm::cursor::MoveTo(0, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Green), Print("Congratulations! You've got a new high score!"), ResetColor)?;
        }

        self.show_high_scores(stdout)
    }

    fn show_high_scores(&self, stdout: &mut std::io::Stdout) -> std::io::Result<HighScoreAction> {
        execute!(stdout, crossterm::terminal::Clear(crossterm::terminal::ClearType::All))?;
        let mut y = 0;

        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::Yellow), Print("🏆 HIGH SCORES 🏆"), ResetColor)?;
        y += 1;
        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::Cyan), Print("=".repeat(65)), ResetColor)?;
        y += 1;

        if self.high_scores.scores.is_empty() {
            execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::DarkGrey), Print("No high scores yet. Be the first!"), ResetColor)?;
        } else {
            let header = format!("{:<4} {:<8} {:<12} {:<19}", "Rank", "Score", "Highest Tile", "Date");
            execute!(stdout, crossterm::cursor::MoveTo(0, y), SetAttribute(Attribute::Bold), SetForegroundColor(Color::White), Print(header), ResetColor)?;
            y += 1;
            execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::Cyan), Print("-".repeat(65)), ResetColor)?;
            y += 1;

            for (i, entry) in self.high_scores.scores.iter().enumerate() {
                let rank_color = if i < 3 { Color::Yellow } else { Color::White };
                let tile_color = if entry.highest_tile >= 2048 { Color::Green } else { Color::Cyan };

                let rank = format!("{:<4}", i + 1);
                let score = format!("{:<8}", entry.score);
                let tile = format!("{:<12}", entry.highest_tile);
                let date = format!("{:<19}", entry.date);

                execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(rank_color), Print(&rank), ResetColor)?;
                execute!(stdout, crossterm::cursor::MoveTo(5, y), SetForegroundColor(Color::White), Print(&score), ResetColor)?;
                execute!(stdout, crossterm::cursor::MoveTo(14, y), SetForegroundColor(tile_color), Print(&tile), ResetColor)?;
                execute!(stdout, crossterm::cursor::MoveTo(27, y), SetForegroundColor(Color::DarkGrey), Print(&date), ResetColor)?;
                y += 1;
            }
        }
        y += 1;
        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::Cyan), Print("=".repeat(65)), ResetColor)?;
        y += 2;
        execute!(stdout, crossterm::cursor::MoveTo(0, y), SetForegroundColor(Color::DarkGrey), Print("Press 'Q' to quit, or any other key to continue..."), ResetColor)?;

        loop {
            if let Event::Key(key_event) = event::read()? {
                match key_event.code {
                    KeyCode::Char('q') | KeyCode::Char('Q') => return Ok(HighScoreAction::Quit),
                    _ => return Ok(HighScoreAction::Continue),
                }
            }
        }
    }

    fn wait_for_key_press(&self) -> std::io::Result<()> {
        loop {
            if let Event::Key(_) = event::read()? {
                return Ok(());
            }
        }
    }
}
