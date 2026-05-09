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
    get_f2l_pair_case,
)


# Change only this scramble when you want to investigate a new case.
TARGET_SCRAMBLE = [
    "F'", "R", "U'", "U'", "L'", "R'", "B", "R'", "U'", "F2",
    "U2", "U2", "D", "L2", "R", "B'", "D2", "L2", "D", "B'",
]

NEXT_CASE_NAME = "green_red_case_36"


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
    """
    Skip obviously redundant sequences:
        R R'
        R' R
        R2 R2
        U U'
        same face repeated consecutively
    """
    for first_move, second_move in zip(sequence, sequence[1:]):
        if (first_move, second_move) in INVERSE_PAIRS:
            return True

        if get_move_face(first_move) == get_move_face(second_move):
            return True

    return False


def build_current_case():
    cube = RubiksCube()
    cube.apply_algorithm(TARGET_SCRAMBLE)

    with redirect_stdout(io.StringIO()):
        solve_cross(cube)
        normalize_green_red_pair(cube)

    return cube


def print_case_table_entry(case_definition, algorithm):
    print()
    print("Case table entry:")
    print("-----------------")
    print("Copy this into GREEN_RED_F2L_CASES:")
    print()
    print("    {")
    print(f'        "name": "{NEXT_CASE_NAME}",')
    print(f'        "case_type": "{case_definition["case_type"]}",')
    print(f'        "corner_position": "{case_definition["corner_position"]}",')
    print(f'        "corner_stickers": {case_definition["corner_stickers"]},')
    print(f'        "edge_position": "{case_definition["edge_position"]}",')
    print(f'        "edge_stickers": {case_definition["edge_stickers"]},')
    print(f'        "algorithm": {algorithm},')
    print("    },")


def brute_force_current_green_red_case(max_depth=7):
    base_cube = build_current_case()
    base_case = get_f2l_pair_case(base_cube, "Green-Red")

    print("Green-Red Current Case Brute Force Finder")
    print("=========================================")
    print()

    print("Target scramble:")
    print("---------------")
    print(TARGET_SCRAMBLE)

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

                print_case_table_entry(base_case, sequence)

                return sequence

        print(f"Checked candidates at depth {depth}: {checked}")

    print()
    print("No working insertion found up to this depth.")
    return None


def main():
    brute_force_current_green_red_case(max_depth=7)


if __name__ == "__main__":
    main()