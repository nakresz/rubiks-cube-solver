from src.cube import RubiksCube
from src.scrambler import generate_scramble
from src.solvers.cross_solver import (
    solve_white_green_edge,
    print_white_cross_status,
    is_white_green_edge_solved,
)


def main():
    cube = RubiksCube()

    print("Rubik's Cube CFOP Cross Demo")
    print("============================")
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
    print("White cross status before solving White-Green edge:")
    print("---------------------------------------------------")
    print_white_cross_status(cube)

    print("Is White-Green edge solved?")
    print(is_white_green_edge_solved(cube))

    print()
    print("Trying to solve White-Green edge...")
    print("-----------------------------------")

    moves = solve_white_green_edge(cube)

    print()
    print("Moves used:")
    print(moves)

    print()
    print("Cube after White-Green attempt:")
    print("-------------------------------")
    cube.display()

    print()
    print("White cross status after solving White-Green edge:")
    print("--------------------------------------------------")
    print_white_cross_status(cube)

    print("Is White-Green edge solved?")
    print(is_white_green_edge_solved(cube))


if __name__ == "__main__":
    main()