from src.ai import _minimax

class Tutor:
    def __init__(self, *args, **kwargs):
        # Accepts any arguments ui.py might be trying to pass to it
        pass

    def evaluate_player_move(self, game, state, chosen_move):
        """
        Acts as the AI Tutor. Compares the user's chosen move against the optimal
        Minimax evaluation and returns text feedback.
        """
        player = state.to_move
        depth = max(3, 7 - max(game.h, game.v))
        
        # 1. Calculate the absolute best possible score
        best_score, optimal_move = _minimax(game, state, depth, float('-inf'), float('inf'), True, player)
        
        if chosen_move == optimal_move:
            return "Excellent! That is the optimal move."
            
        # 2. Calculate the score of the user's move
        child_state = game.result(state, chosen_move)
        actual_score, _ = _minimax(game, child_state, depth - 1, float('-inf'), float('inf'), False, player)
        
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
