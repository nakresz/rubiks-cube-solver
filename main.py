from src.cube import RubiksCube
from src.scrambler import generate_scramble
from src.solvers.cross_solver import (
    solve_cross,
    is_white_cross_solved,
    print_white_cross_status,
)
from src.solvers.f2l_solver import (
    print_f2l_status,
    is_f2l_solved,
)


def main():
    cube = RubiksCube()

    print("Rubik's Cube F2L Detection Demo")
    print("===============================")
    print()

    print("Initial solved cube:")
    print("--------------------")
    cube.display()

    print()
    print("F2L status on solved cube:")
    print("--------------------------")
    print_f2l_status(cube)

    print("Is F2L solved on initial cube?")
    print(is_f2l_solved(cube))

    print()
    print("Generating random scramble...")
    print("-----------------------------")

    scramble = generate_scramble(length=20)

    print("Scramble:")
    print(" ".join(scramble))

    cube.apply_algorithm(scramble)

    print()
    print("Cube after scramble:")
    print("--------------------")
    cube.display()

    print()
    print("White cross status after scramble:")
    print("----------------------------------")
    print_white_cross_status(cube)

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
    print("F2L status after cross solver:")
    print("------------------------------")
    print_f2l_status(cube)

    print("Is F2L solved?")
    print(is_f2l_solved(cube))


if __name__ == "__main__":
    main()