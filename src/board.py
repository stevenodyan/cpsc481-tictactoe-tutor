# Board/game structure adapted from the provided Python TicTacToe implementation.
# - Kept only the m x n TicTacToe functionality needed for our tutor.
# - Removed unrelated textbook game classes.
# - Changed default settings to a larger board.
# - Our project-specific heuristic evaluation is implemented in evaluation.py.
# - Our tutor move recommendation logic is implemented in tutor.py.
from collections import namedtuple

GameState = namedtuple("GameState", "to_move, utility, board, moves")


class TicTacToe:
    """
    m x n Tic-Tac-Toe based on the AIMA textbook code.
    h = board width
    v = board height
    k = number in a row needed to win
    """

    def __init__(self, h=5, v=5, k=4):
        self.h = h
        self.v = v
        self.k = k

        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]

        self.initial = GameState(
            to_move="X",
            utility=0,
            board={},
            moves=moves
        )

    def actions(self, state):
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state

        board = state.board.copy()
        board[move] = state.to_move

        moves = list(state.moves)
        moves.remove(move)

        next_player = "O" if state.to_move == "X" else "X"

        return GameState(
            to_move=next_player,
            utility=self.compute_utility(board, move, state.to_move),
            board=board,
            moves=moves
        )

    def utility(self, state, player):
        return state.utility if player == "X" else -state.utility

    def terminal_test(self, state):
        return state.utility != 0 or len(state.moves) == 0

    def to_move(self, state):
        return state.to_move

    def display(self, state):
        board = state.board

        for y in range(1, self.v + 1):
            row = []
            for x in range(1, self.h + 1):
                row.append(board.get((x, y), "."))
            print(" ".join(row))

    def compute_utility(self, board, move, player):
        if (
            self.k_in_row(board, move, player, (0, 1)) or
            self.k_in_row(board, move, player, (1, 0)) or
            self.k_in_row(board, move, player, (1, -1)) or
            self.k_in_row(board, move, player, (1, 1))
        ):
            return 1 if player == "X" else -1

        return 0

    def k_in_row(self, board, move, player, delta_x_y):
        delta_x, delta_y = delta_x_y
        x, y = move
        count = 0

        while board.get((x, y)) == player:
            count += 1
            x += delta_x
            y += delta_y

        x, y = move

        while board.get((x, y)) == player:
            count += 1
            x -= delta_x
            y -= delta_y

        count -= 1
        return count >= self.k