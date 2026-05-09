import io
import copy
from itertools import product
from contextlib import redirect_stdout

from src.cube import RubiksCube
from src.solvers.cross_solver import solve_cross, is_white_cross_solved
from src.solvers.f2l_solver import (
    normalize_green_red_pair,
    print_f2l_pair_case,
    is_f2l_pair_solved,
)


SCRAMBLE = [
    "R2", "B'", "B2", "B", "F2", "D", "B'", "R2", "R2", "F'",
    "L'", "F'", "U2", "R'", "F2", "U", "F2", "U2", "R'", "U2",
]


MOVES = [
    "U", "U'", "U2",
    "R", "R'", "R2",
    "F", "F'", "F2",
    "L", "L'", "L2",
]


INVERSE_PAIRS = {
    ("U", "U'"), ("U'", "U"), ("U2", "U2"),
    ("R", "R'"), ("R'", "R"), ("R2", "R2"),
    ("F", "F'"), ("F'", "F"), ("F2", "F2"),
    ("L", "L'"), ("L'", "L"), ("L2", "L2"),
}


def get_move_face(move):
    return move[0]


def has_bad_repetition(sequence):
    for first_move, second_move in zip(sequence, sequence[1:]):
        if (first_move, second_move) in INVERSE_PAIRS:
            return True

        if get_move_face(first_move) == get_move_face(second_move):
            return True

    return False


def build_current_case():
    cube = RubiksCube()
    cube.apply_algorithm(SCRAMBLE)

    with redirect_stdout(io.StringIO()):
        solve_cross(cube)
        normalize_green_red_pair(cube)

    return cube


def brute_force_current_green_red_case(max_depth=7):
    base_cube = build_current_case()

    print("Green-Red Current Case Brute Force Finder")
    print("=========================================")
    print()

    print("Base case:")
    print("----------")
    print_f2l_pair_case(base_cube, "Green-Red")

    print()
    print("White cross solved before search?")
    print(is_white_cross_solved(base_cube))

    print()
    print("Searching...")
    print()

    for depth in range(1, max_depth + 1):
        print(f"Searching depth {depth}...")

        checked = 0

        for sequence in product(MOVES, repeat=depth):
            sequence = list(sequence)

            if has_bad_repetition(sequence):
                continue

            checked += 1

            cube = copy.deepcopy(base_cube)
            cube.apply_algorithm(sequence)

            if (
                is_f2l_pair_solved(cube, "Green-Red")
                and is_white_cross_solved(cube)
            ):
                print()
                print("FOUND WORKING GREEN-RED INSERTION!")
                print("Algorithm:")
                print(sequence)

                print()
                print("Green-Red case after algorithm:")
                print("-------------------------------")
                print_f2l_pair_case(cube, "Green-Red")

                return sequence

        print(f"Checked candidates at depth {depth}: {checked}")

    print()
    print("No working insertion found up to this depth.")
    return None


def main():
    brute_force_current_green_red_case(max_depth=7)


if __name__ == "__main__":
    main()