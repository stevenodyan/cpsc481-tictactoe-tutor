from src.evaluation import evaluate

# --- AI CACHING (TRANSPOSITION TABLE) ---
_ai_cache = {}

def clear_ai_cache():
    """Clears the AI memory. Call this when resetting the game."""
    _ai_cache.clear()

def best_move(game, state):
    """Return the best move for the current player using alpha-beta minimax."""
    depth = max(3, 7 - max(game.h, game.v))
    player = state.to_move
    _, move = _minimax(game, state, depth, float('-inf'), float('inf'), True, player)
    
    # Fallback guard: ensure move is legal
    if move not in state.moves:
        if state.moves:
            move = state.moves[0]
        else:
            move = None
    return move


def _minimax(game, state, depth, alpha, beta, maximizing, player):
    # Create a unique key for the current search state
    # We use str(state) to guarantee it can be safely saved in the dictionary
    cache_key = (str(state), depth, alpha, beta, maximizing)
    
    if cache_key in _ai_cache:
        return _ai_cache[cache_key]

    if depth == 0 or game.terminal_test(state):
        return evaluate(game, state, player), None

    best = None
    if maximizing:
        value = float('-inf')
        for move in game.actions(state):
            child = game.result(state, move)
            score, _ = _minimax(game, child, depth - 1, alpha, beta, False, player)
            if score > value:
                value, best = score, move
            alpha = max(alpha, value)
            if alpha >= beta:
                break
                
        # Save to cache before returning
        _ai_cache[cache_key] = (value, best)
        return value, best
        
    else:
        value = float('inf')
        for move in game.actions(state):
            child = game.result(state, move)
            score, _ = _minimax(game, child, depth - 1, alpha, beta, True, player)
            if score < value:
                value, best = score, move
            beta = min(beta, value)
            if alpha >= beta:
                break
                
        # Save to cache before returning
        _ai_cache[cache_key] = (value, best)
        return value, best
