import pytest
from src.board import TicTacToe
from src.evaluation import evaluate
from src.ai import best_move
from src.tutor import Tutor


@pytest.fixture
def game():
    return TicTacToe(h=3, v=3, k=3)


def apply_moves(game, moves):
    state = game.initial
    for move in moves:
        state = game.result(state, move)
    return state


# --- evaluation ---

def test_empty_board_not_extreme(game):
    score = evaluate(game, game.initial, "X")
    assert -10000 < score < 10000


def test_near_win_positive(game):
    # X has two in a row, O has nothing
    state = apply_moves(game, [(1,1), (3,3), (2,1)])  # X:(1,1),(2,1) O:(3,3)
    score = evaluate(game, state, "X")
    assert score > 0


def test_three_in_row_beats_two(game):
    # Compare evaluate score directly on isolated boards (no opponent threat)
    from src.board import GameState
    g4 = TicTacToe(h=5, v=5, k=4)
    board2 = {(1,1): "X", (2,1): "X"}
    board3 = {(1,1): "X", (2,1): "X", (3,1): "X"}
    moves_all = [(x,y) for x in range(1,6) for y in range(1,6)]
    state2 = GameState(to_move="O", utility=0, board=board2,
                       moves=[m for m in moves_all if m not in board2])
    state3 = GameState(to_move="O", utility=0, board=board3,
                       moves=[m for m in moves_all if m not in board3])
    assert evaluate(g4, state3, "X") > evaluate(g4, state2, "X")


# --- best_move / minimax ---

def test_takes_winning_move(game):
    # X: (1,1),(2,1) — playing (3,1) wins
    state = apply_moves(game, [(1,1), (1,3), (2,1), (2,3)])
    move = best_move(game, state)
    assert move == (3, 1)


def test_blocks_opponent_win(game):
    # O: (1,3),(2,3) — X must block (3,3)
    state = apply_moves(game, [(1,1), (1,3), (2,2), (2,3)])
    move = best_move(game, state)
    assert move == (3, 3)


def test_returns_valid_move_on_empty():
    g = TicTacToe(h=5, v=5, k=4)
    move = best_move(g, g.initial)
    assert move in g.initial.moves


# --- tutor ---

def test_recommend_returns_valid_move(game):
    tutor = Tutor(game)
    move, explanation = tutor.recommend(game.initial)
    assert move in game.initial.moves
    assert "AI suggests" in explanation


def test_result_message(game):
    tutor = Tutor(game)
    # X wins: (1,1),(1,2),(1,3)
    state = apply_moves(game, [(1,1), (2,1), (1,2), (2,2), (1,3)])
    assert tutor.result_message(state) == "X wins!"


def test_draw_message(game):
    # fill a 3x3 with no winner
    moves = [(1,1),(2,1),(3,1),(1,2),(3,2),(2,2),(1,3),(3,3),(2,3)]
    state = apply_moves(game, moves)
    tutor = Tutor(game)
    assert tutor.result_message(state) == "Draw!"
