# Spades Score Tracker

A desktop application for tracking scores in the classic card game Spades, with automatic score calculation and PDF report generation.

## Overview

Spades Score Tracker is a Python-based desktop application that simplifies score tracking for Spades card games. The application automatically calculates scores based on bids and tricks, tracks bags, and generates comprehensive PDF reports of game progress.

## Key Features

- **Player Management**: Support for multiple players
- **Automatic Scoring**: Calculates points based on bids and tricks won
- **Bags Tracking**: Tracks and counts bag penalties
- **Round Management**: Supports the standard 13 rounds of Spades
- **PDF Reports**: Generates detailed game reports in PDF format
- **User-Friendly Interface**: Simple, intuitive Tkinter-based UI

## Game Rules Implemented

- Players earn 10 points for each bid trick won
- Players earn 1 point for each trick won beyond their bid (bags)
- Players lose 10 points for each bid trick not won
- Players with 5 or more bags are marked as eliminated
- Game progresses through 13 rounds

## Requirements

- Python 3.6+
- Tkinter (included with most Python installations)
- ReportLab (for PDF generation)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/spades-score-tracker.git
   cd spades-score-tracker
   ```

2. Install required packages:
   ```
   pip install reportlab
   ```

3. Run the application:
   ```
   python game.py
   ```

## Usage

1. **Start a New Game**:
   - Enter the number of players (2+)
   - Click "Setup Players"
   - Enter player names and click "Save Player Names"

2. **During Each Round**:
   - Enter each player's bid (how many tricks they think they'll win)
   - After play, enter the actual tricks won by each player
   - Click "Calculate Scores" to update scores and generate round report
   - Click "Next Round" to proceed to the next round

3. **End of Game**:
   - After 13 rounds, a final score report is generated
   - The PDF file "spades_scores.pdf" contains the complete game history

## Score Calculation

- **Met or Exceeded Bid**: (Bid × 10) + (Tricks - Bid)
- **Failed to Meet Bid**: -(Bid × 10) + Tricks
- **Bags**: Accumulate when players win more tricks than bid

## Project Structure

- `game.py`: Main application file with UI and game logic
- `spades_scores.pdf`: Generated score report

## Features in Detail

### Score Tracking
The application tracks round scores, total scores, and bags for each player, updating the display after each round.

### PDF Reports
The application generates a comprehensive PDF report with:
- Round-by-round scores for each player
- Total scores and bags count
- Final results after all rounds

### Validation
The application includes validation to ensure:
- Player names are not empty
- Bids and tricks are valid numbers
- Total tricks won in a round don't exceed the round number

## Future Enhancements

- Support for team play (partnerships)
- Customizable scoring rules
- Game history and statistics
- Dark mode UI option
- Undo/redo functionality
