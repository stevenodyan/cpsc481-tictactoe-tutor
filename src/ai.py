from src.evaluation import evaluate


def best_move(game, state):
    """Return the best move for the current player using alpha-beta minimax."""
    depth = max(3, 7 - max(game.h, game.v))
    player = state.to_move
    _, move = _minimax(game, state, depth, float('-inf'), float('inf'), True, player)
    # Fallback guard: ensure move is legal
    if move not in state.moves:
        move = state.moves[0]
    return move


def _minimax(game, state, depth, alpha, beta, maximizing, player):
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
        return value, best
