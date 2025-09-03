//! # Game Module
//!
//! This module encapsulates all the game-related functionality for Terminal 2048.
//! It is divided into two sub-modules: `logic` and `ui`.
//!
//! - The `logic` module implements the core game mechanics, such as moving tiles,
//!   merging them, and tracking the score.
//! - The `ui` module is responsible for rendering the game board and handling
//!   user input in the terminal.

pub mod logic;
pub mod ui;
