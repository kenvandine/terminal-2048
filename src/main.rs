use terminal_2048::game::ui::GameUI;
use std::io::{stdout, IsTerminal};

fn main() -> std::io::Result<()> {
    if !stdout().is_terminal() {
        eprintln!("Not running in an interactive terminal.");
        eprintln!("This game requires an interactive terminal to run.");
        return Ok(());
    }
    let mut game = GameUI::new();
    game.run()
}
