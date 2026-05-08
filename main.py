from src.cube import RubiksCube
from src.scrambler import generate_scramble
from src.solvers.cross_solver import (
    solve_cross,
    print_white_cross_status,
    is_white_cross_solved,
)


def main():
    cube = RubiksCube()

    print("Rubik's Cube Full Bottom White Cross Demo")
    print("=========================================")
    print()

    print("Generating random scramble...")
    print("-----------------------------")

    scramble = generate_scramble(length=8)

    print("Scramble:")
    print(" ".join(scramble))

    cube.apply_algorithm(scramble)

    print()
    print("Cube after scramble:")
    print("--------------------")
    cube.display()

    print()
    print("Bottom white cross status before solving:")
    print("-----------------------------------------")
    print_white_cross_status(cube)

    print("Is bottom white cross solved before?")
    print(is_white_cross_solved(cube))

    print()
    print("Trying to solve full bottom white cross...")
    print("------------------------------------------")

    moves = solve_cross(cube)

    print()
    print("Moves used by bottom cross solver:")
    print(moves)

    print()
    print("Cube after bottom cross attempt:")
    print("--------------------------------")
    cube.display()

    print()
    print("Bottom white cross status after solving:")
    print("----------------------------------------")
    print_white_cross_status(cube)

    print("Is bottom white cross solved after?")
    print(is_white_cross_solved(cube))


if __name__ == "__main__":
    main()