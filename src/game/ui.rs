use crate::game::logic::GameLogic;
use crate::scores::{self, HighScores};
use std::io::stdout;
use crossterm::{
    event::{self, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
    style::{Attribute, Color, Print, ResetColor, SetAttribute, SetBackgroundColor, SetForegroundColor},
};

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
        execute!(
            stdout,
            crossterm::terminal::Clear(crossterm::terminal::ClearType::All),
            crossterm::cursor::MoveTo(0, 0)
        )?;
        execute!(
            stdout,
            SetAttribute(Attribute::Bold),
            SetForegroundColor(Color::Cyan),
            Print("=".repeat(60)),
            Print("\n"),
            SetForegroundColor(Color::Magenta),
            Print("🌟 "),
            SetForegroundColor(Color::Yellow),
            Print("TERMINAL 2048!"),
            SetForegroundColor(Color::Magenta),
            Print(" 🌟\n"),
            SetForegroundColor(Color::Cyan),
            Print("=".repeat(60)),
            Print("\n\n"),
            ResetColor,
            SetForegroundColor(Color::White),
            Print("Goal:"),
            ResetColor,
            SetForegroundColor(Color::Green),
            Print(" Combine tiles to reach 2048!\n\n"),
            ResetColor,
            SetForegroundColor(Color::White),
            Print("Controls:\n"),
            ResetColor,
            Print("  W/↑ - Up    S/↓ - Down\n"),
            Print("  A/← - Left  D/→ - Right\n"),
            Print("  Q - Quit  H - High Scores\n\n"),
            SetForegroundColor(Color::Yellow),
            Print("✨ 2048 is a popular puzzle game where players combine\n"),
            Print("✨ tiles with numerical values to create a single tile\n"),
            Print("✨ with the value of 2048.\n"),
            Print("✨ The game requires strategic thinking and planning\n"),
            Print("✨ to achieve the goal.\n\n"),
            ResetColor,
        )?;

        if let Some(high_score) = self.high_scores.scores.first() {
            execute!(
                stdout,
                SetForegroundColor(Color::Cyan),
                Print("Current High Score: "),
                SetForegroundColor(Color::White),
                Print(high_score.score),
                Print("\n\n"),
                ResetColor
            )?;
        }

        execute!(
            stdout,
            SetForegroundColor(Color::DarkGrey),
            Print("Press any key to start...\n"),
            ResetColor
        )?;

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
                self.show_final_score_screen(&mut stdout)?;
                break;
            }

            if let Event::Key(key_event) = event::read()? {
                let moved = match key_event.code {
                    KeyCode::Char('w') | KeyCode::Up => self.logic.move_up(),
                    KeyCode::Char('s') | KeyCode::Down => self.logic.move_down(),
                    KeyCode::Char('a') | KeyCode::Left => self.logic.move_left(),
                    KeyCode::Char('d') | KeyCode::Right => self.logic.move_right(),
                    KeyCode::Char('h') => {
                        self.show_high_scores(&mut stdout)?;
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
        execute!(
            stdout,
            crossterm::terminal::Clear(crossterm::terminal::ClearType::All),
            crossterm::cursor::MoveTo(0, 0)
        )?;

        let border_color = Color::Rgb {
            r: 100,
            g: 100,
            b: 100,
        };

        // Header
        execute!(
            stdout,
            SetAttribute(Attribute::Bold),
            SetForegroundColor(Color::Cyan),
            Print("=".repeat(55)),
            Print("\n"),
            SetForegroundColor(Color::Magenta),
            Print("🎮 "),
            SetForegroundColor(Color::Yellow),
            Print("2048 GAME"),
            SetForegroundColor(Color::Magenta),
            Print(" 🎮\n"),
            SetForegroundColor(Color::Cyan),
            Print("=".repeat(55)),
            Print("\n"),
            ResetColor
        )?;

        // Score
        let score_color = if self.logic.score < 1000 {
            Color::Green
        } else if self.logic.score < 5000 {
            Color::Yellow
        } else {
            Color::Red
        };
        execute!(
            stdout,
            SetAttribute(Attribute::Bold),
            Print("Score: "),
            SetForegroundColor(score_color),
            Print(self.logic.score),
            ResetColor
        )?;
        if let Some(high_score) = self.high_scores.scores.first() {
            execute!(
                stdout,
                SetAttribute(Attribute::Bold),
                Print("  |  High Score: "),
                SetForegroundColor(Color::Cyan),
                Print(high_score.score),
                ResetColor
            )?;
        }
        execute!(stdout, Print("\n"))?;

        // Instructions
        execute!(
            stdout,
            SetForegroundColor(Color::Blue),
            Print("Use "),
            SetForegroundColor(Color::White),
            Print("WASD"),
            SetForegroundColor(Color::Blue),
            Print(" or "),
            SetForegroundColor(Color::White),
            Print("Arrow Keys"),
            SetForegroundColor(Color::Blue),
            Print(" • "),
            SetForegroundColor(Color::Red),
            Print("Q"),
            SetForegroundColor(Color::Blue),
            Print(" to quit • "),
            SetForegroundColor(Color::Magenta),
            Print("H"),
            SetForegroundColor(Color::Blue),
            Print(" for high scores\n"),
            SetForegroundColor(Color::Cyan),
            Print("-".repeat(55)),
            Print("\n"),
            ResetColor
        )?;

        // Board
        execute!(
            stdout,
            SetForegroundColor(border_color),
            Print("┌─────┬─────┬─────┬─────┐\n"),
            ResetColor
        )?;
        for (r_idx, row) in self.logic.board.iter().enumerate() {
            execute!(
                stdout,
                SetForegroundColor(border_color),
                Print("│"),
                ResetColor
            )?;
            for cell in row.iter() {
                let (fg, bg) = self.get_tile_colors(*cell);
                execute!(
                    stdout,
                    SetBackgroundColor(bg),
                    SetForegroundColor(fg),
                    Print(format!(
                        "{:^5}",
                        if *cell == 0 {
                            "".to_string()
                        } else {
                            cell.to_string()
                        }
                    )),
                    ResetColor,
                    SetForegroundColor(border_color),
                    Print("│"),
                    ResetColor
                )?;
            }
            execute!(stdout, Print("\n"))?;
            if r_idx < 3 {
                execute!(
                    stdout,
                    SetForegroundColor(border_color),
                    Print("├─────┼─────┼─────┼─────┤\n"),
                    ResetColor
                )?;
            }
        }
        execute!(
            stdout,
            SetForegroundColor(border_color),
            Print("└─────┴─────┴─────┴─────┘\n"),
            ResetColor
        )?;

        // Footer
        if self.logic.won && !self.logic.game_over {
            execute!(
                stdout,
                SetAttribute(Attribute::Bold),
                SetForegroundColor(Color::Yellow),
                Print("\n🎉 Congratulations! You reached 2048! 🎉\n"),
                SetForegroundColor(Color::Green),
                Print("Keep playing to get an even higher score!\n"),
                ResetColor
            )?;
        } else if self.logic.game_over {
            execute!(
                stdout,
                SetAttribute(Attribute::Bold),
                SetForegroundColor(Color::Red),
                Print("\n💀 Game Over! No more moves available.\n"),
                ResetColor
            )?;
        }

        execute!(
            stdout,
            SetForegroundColor(Color::Cyan),
            Print("-".repeat(55)),
            Print("\n"),
            ResetColor
        )?;

        if !self.logic.game_over {
            execute!(
                stdout,
                SetForegroundColor(Color::DarkGrey),
                Print("Press a key to move...\n"),
                ResetColor
            )?;
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

    fn show_final_score_screen(&mut self, stdout: &mut std::io::Stdout) -> std::io::Result<()> {
        execute!(
            stdout,
            crossterm::terminal::Clear(crossterm::terminal::ClearType::All),
            crossterm::cursor::MoveTo(0, 0)
        )?;

        execute!(
            stdout,
            SetAttribute(Attribute::Bold),
            SetForegroundColor(Color::Yellow),
            Print("🎮 GAME OVER 🎮\n"),
            ResetColor
        )?;

        let is_new_high = scores::is_new_high_score(&self.high_scores, self.logic.score);
        if is_new_high {
            scores::add_high_score(&mut self.high_scores, self.logic.score, &self.logic.board);
            execute!(
                stdout,
                SetAttribute(Attribute::Bold),
                SetForegroundColor(Color::Green),
                Print("\nCongratulations! You've got a new high score!\n"),
                ResetColor
            )?;
        }

        self.show_high_scores(stdout)?;

        Ok(())
    }

    fn show_high_scores(&self, stdout: &mut std::io::Stdout) -> std::io::Result<()> {
        execute!(
            stdout,
            crossterm::terminal::Clear(crossterm::terminal::ClearType::All),
            crossterm::cursor::MoveTo(0, 0)
        )?;

        execute!(
            stdout,
            SetAttribute(Attribute::Bold),
            SetForegroundColor(Color::Yellow),
            Print("🏆 HIGH SCORES 🏆\n"),
            ResetColor
        )?;
        execute!(
            stdout,
            SetForegroundColor(Color::Cyan),
            Print("=".repeat(65)),
            Print("\n"),
            ResetColor
        )?;

        if self.high_scores.scores.is_empty() {
            execute!(
                stdout,
                SetForegroundColor(Color::DarkGrey),
                Print("No high scores yet. Be the first!\n"),
                ResetColor
            )?;
        } else {
            execute!(
                stdout,
                SetAttribute(Attribute::Bold),
                SetForegroundColor(Color::White),
                Print(format!(
                    "{:<4} {:<8} {:<12} {:<19}\n",
                    "Rank", "Score", "Highest Tile", "Date"
                )),
                ResetColor
            )?;
            execute!(
                stdout,
                SetForegroundColor(Color::Cyan),
                Print("-".repeat(65)),
                Print("\n"),
                ResetColor
            )?;
            for (i, entry) in self.high_scores.scores.iter().enumerate() {
                let rank_color = if i < 3 {
                    Color::Yellow
                } else {
                    Color::White
                };
                let tile_color = if entry.highest_tile >= 2048 {
                    Color::Green
                } else {
                    Color::Cyan
                };
                execute!(
                    stdout,
                    SetForegroundColor(rank_color),
                    Print(format!("{:<4}", i + 1)),
                    ResetColor,
                    Print(" "),
                    SetForegroundColor(Color::White),
                    Print(format!("{:<8}", entry.score)),
                    ResetColor,
                    Print(" "),
                    SetForegroundColor(tile_color),
                    Print(format!("{:<12}", entry.highest_tile)),
                    ResetColor,
                    Print(" "),
                    SetForegroundColor(Color::DarkGrey),
                    Print(format!("{:<19}", entry.date)),
                    ResetColor,
                    Print("\n")
                )?;
            }
        }
        execute!(
            stdout,
            SetForegroundColor(Color::Cyan),
            Print("=".repeat(65)),
            Print("\n"),
            ResetColor
        )?;
        execute!(
            stdout,
            SetForegroundColor(Color::DarkGrey),
            Print("\nPress any key to continue...\n"),
            ResetColor
        )?;

        self.wait_for_key_press()?;
        Ok(())
    }

    fn wait_for_key_press(&self) -> std::io::Result<()> {
        loop {
            if let Event::Key(_) = event::read()? {
                return Ok(());
            }
        }
    }
}
