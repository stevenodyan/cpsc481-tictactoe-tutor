DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]


def evaluate(game, state, player):
    """
    Heuristic board evaluation for player.
    Weights (descending priority):
      ±10000  immediate win/loss on board
      ±1000   opponent has winning move next turn
      +10*n²  own open sequences of length n >= 2
      ±50     per open line available to each player
      +n      raw sequence length (tiebreaker)
    """
    opponent = "O" if player == "X" else "X"

    # Immediate terminal: already won/lost
    if state.utility != 0:
        return 10000 if (state.utility > 0 and player == "X") or \
                        (state.utility < 0 and player == "O") else -10000

    score = 0

    # Check if opponent can win on their next move (urgency to block).
    # Temporarily flip to_move to simulate opponent moving.
    from src.board import GameState
    opp_state = GameState(opponent, state.utility, state.board, state.moves)
    for move in state.moves:
        test = game.result(opp_state, move)
        if test.utility != 0:
            score -= 1000

    score += _score_lines(game, state.board, player, game.k)
    score -= _score_lines(game, state.board, opponent, game.k)

    return score


def _score_lines(game, board, player, k):
    """Sum heuristic score for all open lines belonging to player."""
    score = 0
    for x in range(1, game.h + 1):
        for y in range(1, game.v + 1):
            for dx, dy in DIRECTIONS:
                length, open_ends = _scan_line(game, board, player, x, y, dx, dy, k)
                if length >= 2 and open_ends > 0:
                    score += 10 * length * length  # sequence² bonus
                    score += 50 * open_ends         # open line bonus
                    score += length                  # tiebreaker
    return score


def _scan_line(game, board, player, x, y, dx, dy, k):
    """
    Starting at (x,y) in direction (dx,dy), count consecutive player marks
    and open ends. Returns (length, open_ends) or (0, 0) if not player's mark.
    """
    if board.get((x, y)) != player:
        return 0, 0

    length = 0
    cx, cy = x, y
    while 1 <= cx <= game.h and 1 <= cy <= game.v and board.get((cx, cy)) == player:
        length += 1
        cx += dx
        cy += dy

    if length >= k:
        return length, 0  # already a win, handled elsewhere

    open_ends = 0
    # check end of sequence
    if 1 <= cx <= game.h and 1 <= cy <= game.v and board.get((cx, cy)) is None:
        open_ends += 1
    # check before start
    bx, by = x - dx, y - dy
    if 1 <= bx <= game.h and 1 <= by <= game.v and board.get((bx, by)) is None:
        open_ends += 1

    return length, open_ends
