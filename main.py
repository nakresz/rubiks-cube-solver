from src.cube import RubiksCube
from src.scrambler import generate_scramble
from src.solvers.cross_solver import (
    solve_cross,
    is_white_cross_solved,
    print_white_cross_status,
)

from src.solvers.f2l_solver import (
    print_f2l_status,
    print_f2l_pair_case,
    normalize_green_red_pair,
)


def main():
    cube = RubiksCube()

    print("Rubik's Cube Green-Red F2L Preparation Demo")
    print("===========================================")
    print()

    print("Generating random scramble...")
    print("-----------------------------")

    scramble = generate_scramble(length=20)

    print("Scramble:")
    print(" ".join(scramble))

    cube.apply_algorithm(scramble)

    print()
    print("Solving bottom white cross first...")
    print("-----------------------------------")

    cross_moves = solve_cross(cube)

    print()
    print("Cross moves:")
    print(cross_moves)

    print()
    print("White cross status after cross solver:")
    print("--------------------------------------")
    print_white_cross_status(cube)

    print("Is white cross solved?")
    print(is_white_cross_solved(cube))

    print()
    print("Green-Red F2L case before preparation:")
    print("--------------------------------------")
    print_f2l_pair_case(cube, "Green-Red")

    print()
    print("Preparing Green-Red F2L pair...")
    print("--------------------------------")

    f2l_moves = normalize_green_red_pair(cube)

    print()
    print("F2L preparation moves:")
    print(f2l_moves)

    print()
    print("Green-Red F2L case after preparation:")
    print("-------------------------------------")
    print_f2l_pair_case(cube, "Green-Red")

    print()
    print("Full F2L status after preparation:")
    print("----------------------------------")
    print_f2l_status(cube)

    print()
    print("White cross status after F2L preparation:")
    print("-----------------------------------------")
    print_white_cross_status(cube)

    print("Is white cross still solved?")
    print(is_white_cross_solved(cube))


if __name__ == "__main__":
    main()