from src.ai import best_move


class Tutor:
    def __init__(self, game):
        self.game = game

    def recommend(self, state):
        """Return (move, explanation) for the current player."""
        move = best_move(self.game, state)
        explanation = f"AI suggests: {move}"
        return move, explanation

    def apply_move(self, state, move):
        return self.game.result(state, move)

    def is_terminal(self, state):
        return self.game.terminal_test(state)

    def result_message(self, state):
        if state.utility > 0:
            return "X wins!"
        if state.utility < 0:
            return "O wins!"
        return "Draw!"
