# CPSC 481 m×n Tic-Tac-Toe Tutor

An AI tutor for m×n Tic-Tac-Toe with configurable board size and win condition. The tutor recommends moves using depth-limited minimax with alpha-beta pruning and a heuristic evaluation function.

## Team Members
- Steven Sanusi
- Kevin Fuentes
- Gilbert Cervantes

## Tech Stack
- **Language:** Python 3
- **GUI:** pygame
- **Testing:** pytest

## Setup & Run

```bash
pip install -r requirements.txt
python main.py
```

## Default Demo
- Board size: 5×5
- Win condition: 4 in a row

## Features & AI Approach

The tutor supports configurable m×n boards and win lengths, with legal move, win, and draw detection.

Move recommendations use **depth-limited minimax** with **alpha-beta pruning** to reduce the number of states searched. Search depth adapts to board size (depth = max(3, 7 − max(m, n))), so smaller boards receive deeper search. On larger boards where exhaustive search is too expensive, a heuristic evaluation function estimates position strength.

### Heuristic Evaluation & Weighting

The evaluation function scores a position by summing weighted factors for the current player minus the same factors for the opponent:

| Priority | Factor | Weight | Rationale |
|---|---|---|---|
| 1 | Immediate win/loss on board | ±10 000 | A finished game is the ultimate outcome — must dominate all other factors |
| 2 | Opponent has a winning move next turn | −1 000 per threat | Missing a block is nearly as catastrophic as losing outright |
| 3 | Own open sequences of length n | +10 × n² | Squaring rewards longer chains non-linearly — a 3-in-a-row is far more threatening than two 2-in-a-rows |
| 4 | Open line count (ends not blocked) | ±50 per open end | Positional control: lines with two open ends are twice as dangerous as one-sided threats |
| 5 | Raw sequence length | +n | Tiebreaker between otherwise equal positions |

**Why this ordering?** Winning is unconditionally the best outcome, so it gets the highest weight. Failing to block an opponent's winning move is the next-worst outcome — worth far more than any positional advantage. Sequence length is squared rather than linear because a 3-in-a-row with two open ends creates two simultaneous threats the opponent cannot both block, which is qualitatively different from isolated 2-in-a-rows. Open-end count captures this double-threat structure. Raw length is kept as a small tiebreaker so the AI still prefers longer chains when all else is equal.

## Planned Evaluation
We will compare the tutor's recommended moves against random legal moves on board sizes such as 4×4 and 5×5, measuring win rate and tracking how alpha-beta pruning affects the number of board states searched.

## Code Layout

cpsc481-tictactoe-tutor/
├── README.md
├── requirements.txt
├── main.py
└── src/
    ├── __init__.py
    ├── board.py
    ├── ai.py
    ├── evaluation.py
    ├── tutor.py
    ├── ui.py
    └── performance_eval.py

README.md
Explains the project, setup instructions, how to run the program, and the code layout.
requirements.txt
Lists the Python libraries needed to run the project. The main external library is Pygame.

main.py
Entry point of the program. It starts the Pygame application.

src/__init__.py
Marks the src folder as a Python package.

src/board.py
Contains the m×n Tic-Tac-Toe game logic. It stores the board state, legal moves, result function, terminal test, and win checking for k pieces in a row.

src/ai.py
Contains the AI move-selection logic. It uses depth-limited minimax search, alpha-beta pruning, and caching to choose moves.

src/evaluation.py
Contains the heuristic evaluation function used by the AI to score non-terminal board states. It considers wins/losses, opponent threats, open sequences, and open-ended lines.

src/tutor.py
Contains the tutor logic. It recommends moves, compares the user’s move against the AI’s best move, and returns feedback such as “Excellent,” “Good move,” “Mistake,” or “Blunder.”

src/ui.py
Contains the Pygame graphical interface. It handles the configuration screen, board rendering, mouse clicks, Hint button, New Game button, AI move display, and tutor feedback display.

src/performance_eval.py
Separate evaluation script used to compare the tutor’s recommended moves against randomly selected legal moves across different board sizes.