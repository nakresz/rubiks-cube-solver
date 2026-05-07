import random

from src.moves import ALL_MOVES, INVERSE_MOVES


def generate_scramble(length=20):
    """
    Generate a random scramble.

    Parameters:
        length: Number of moves in the scramble.

    Returns:
        A list of moves.

    Example:
        ["U", "R", "F2", "D'"]
    """
    scramble = []

    for _ in range(length):
        move = random.choice(ALL_MOVES)
        scramble.append(move)

    return scramble


def inverse_move(move):
    """
    Return the inverse of a single move.

    Example:
        U  -> U'
        R' -> R
        F2 -> F2
    """
    if move not in INVERSE_MOVES:
        raise ValueError(f"Unsupported move: {move}")

    return INVERSE_MOVES[move]


def inverse_algorithm(moves):
    """
    Return the inverse of a move sequence.

    Important idea:
        To undo an algorithm, we reverse the order
        and invert each move.

    Example:
        ["U", "R", "F2"]
        reverse order -> ["F2", "R", "U"]
        invert each   -> ["F2", "R'", "U'"]
    """
    inverse_moves = []

    for move in reversed(moves):
        inverse_moves.append(inverse_move(move))

    return inverse_moves