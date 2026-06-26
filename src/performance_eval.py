import random
import time

from src.board import TicTacToe
from src.ai import best_move, clear_ai_cache
from src.evaluation import evaluate


def random_play_to_state(game, max_moves):
    """
    Creates a random non-terminal board state by playing random legal moves.
    """
    state = game.initial

    for _ in range(max_moves):
        if game.terminal_test(state) or not state.moves:
            break

        move = random.choice(state.moves)
        state = game.result(state, move)

    return state


def compare_tutor_vs_random(game, state):
    """
    Compares the tutor's recommended move against a random legal move.
    Returns performance data for one trial.
    """
    player = state.to_move

    if game.terminal_test(state) or not state.moves:
        return None

    # Tutor move
    clear_ai_cache()
    start_time = time.perf_counter()
    tutor_move = best_move(game, state)
    tutor_time = time.perf_counter() - start_time

    if tutor_move is None:
        return None

    tutor_state = game.result(state, tutor_move)
    tutor_score = evaluate(game, tutor_state, player)

    # Random move
    random_move = random.choice(state.moves)
    random_state = game.result(state, random_move)
    random_score = evaluate(game, random_state, player)

    return {
        "player": player,
        "tutor_move": tutor_move,
        "random_move": random_move,
        "tutor_score": tutor_score,
        "random_score": random_score,
        "tutor_time": tutor_time,
        "tutor_better": tutor_score > random_score,
        "same_score": tutor_score == random_score,
    }


def run_evaluation(board_width, board_height, win_length, trials=20, random_start_moves=6):
    """
    Runs several trials for one board configuration.
    """
    game = TicTacToe(h=board_width, v=board_height, k=win_length)

    tutor_scores = []
    random_scores = []
    tutor_times = []

    tutor_better_count = 0
    same_score_count = 0
    completed_trials = 0

    for _ in range(trials):
        state = random_play_to_state(game, random_start_moves)
        result = compare_tutor_vs_random(game, state)

        if result is None:
            continue

        completed_trials += 1
        tutor_scores.append(result["tutor_score"])
        random_scores.append(result["random_score"])
        tutor_times.append(result["tutor_time"])

        if result["tutor_better"]:
            tutor_better_count += 1

        if result["same_score"]:
            same_score_count += 1

    if completed_trials == 0:
        print(f"No valid trials for {board_width}x{board_height}, k={win_length}")
        return

    avg_tutor_score = sum(tutor_scores) / completed_trials
    avg_random_score = sum(random_scores) / completed_trials
    avg_tutor_time = sum(tutor_times) / completed_trials

    print("=" * 70)
    print(f"Board: {board_width}x{board_height}, win length: {win_length}")
    print(f"Trials completed: {completed_trials}")
    print(f"Tutor better than random: {tutor_better_count}/{completed_trials}")
    print(f"Same score: {same_score_count}/{completed_trials}")
    print(f"Average tutor score: {avg_tutor_score:.2f}")
    print(f"Average random score: {avg_random_score:.2f}")
    print(f"Average tutor decision time: {avg_tutor_time:.4f} seconds")


def main():
    random.seed(42)

    test_settings = [
        (4, 4, 3),
        (5, 5, 4),
        (6, 6, 4),
    ]

    for width, height, win_length in test_settings:
        run_evaluation(
            board_width=width,
            board_height=height,
            win_length=win_length,
            trials=20,
            random_start_moves=6,
        )


if __name__ == "__main__":
    main()