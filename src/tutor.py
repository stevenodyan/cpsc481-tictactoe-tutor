from src.ai import _minimax

def evaluate_player_move(game, state, chosen_move):
    """
    Acts as the AI Tutor. Compares the user's chosen move against the optimal
    Minimax evaluation and returns text feedback.
    """
    player = state.to_move
    depth = max(3, 7 - max(game.h, game.v))
    
    # 1. Calculate the absolute best possible score from the current board
    best_score, optimal_move = _minimax(game, state, depth, float('-inf'), float('inf'), True, player)
    
    # If the user literally picked the AI's top choice
    if chosen_move == optimal_move:
        return "Excellent! That is the optimal move."
        
    # 2. Calculate the score of the board AFTER the user's chosen move
    child_state = game.result(state, chosen_move)
    
    # Evaluate the new state (the 'False' means the opponent is now minimizing our score)
    actual_score, _ = _minimax(game, child_state, depth - 1, float('-inf'), float('inf'), False, player)
    
    # 3. Analyze the difference (Delta)
    score_diff = best_score - actual_score
    
    # Provide feedback based on how much value was lost
    if score_diff == 0:
        return "Good move! It maintains your advantage, even if it wasn't my first choice."
    elif score_diff <= 10:  # Assuming small integer heuristic differences
        return "Slight inaccuracy. There was a slightly stronger move available."
    elif actual_score < 0 and best_score >= 0:
        return "Blunder! You just gave away a winning or drawing position."
    else:
        return "Mistake. You lost significant ground with that move."
