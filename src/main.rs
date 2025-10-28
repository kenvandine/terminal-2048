use terminal_2048::game::ui::GameUI;
use std::io::{stdout, IsTerminal};

/// The main entry point for the Terminal 2048 application.
///
/// This function initializes and runs the game. It checks if the application is
/// running in an interactive terminal before starting the game loop. If not,
/// it prints an error message and exits.
fn main() -> std::io::Result<()> {
    if !stdout().is_terminal() {
        eprintln!("Not running in an interactive terminal.");
        eprintln!("This game requires an interactive terminal to run.");
        return Ok(());
    }
    let mut game = GameUI::new();
    game.run()
}
