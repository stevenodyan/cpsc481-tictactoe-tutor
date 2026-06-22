from src.ai import best_move, _minimax


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

    def evaluate_player_move(self, state, chosen_move):
        """
        Acts as the AI Tutor. Compares the user's chosen move against the optimal
        Minimax evaluation and returns text feedback.
        """
        if chosen_move not in state.moves:
            return "Invalid move."
        player = state.to_move
        depth = max(3, 7 - max(self.game.h, self.game.v))
        
        # 1. Calculate the absolute best possible score
        best_score, optimal_move = _minimax(self.game, state, depth, float('-inf'), float('inf'), True, player)
        
        if chosen_move == optimal_move:
            return "Excellent! That is the optimal move."
            
        # 2. Calculate the score of the user's move
        child_state = self.game.result(state, chosen_move)
        actual_score, _ = _minimax(self.game, child_state, depth - 1, float('-inf'), float('inf'), False, player)
        
        # 3. Analyze the difference
        score_diff = best_score - actual_score
        
        if score_diff == 0:
            return "Good move! It maintains your advantage."
        elif score_diff <= 10:
            return "Slight inaccuracy. There was a slightly stronger move available."
        elif actual_score < 0 and best_score >= 0:
            return "Blunder! You just gave away a winning or drawing position."
        else:
            return "Mistake. You lost significant ground with that move."
