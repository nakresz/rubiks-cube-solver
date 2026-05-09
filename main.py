from src.cube import RubiksCube
from src.scrambler import generate_scramble
from src.solvers.cross_solver import (
    solve_cross,
    is_white_cross_solved,
)
from src.solvers.f2l_solver import (
    normalize_green_red_pair,
    insert_green_red_pair,
    print_f2l_pair_case,
    is_f2l_pair_solved,
)


def main():
    cube = RubiksCube()

    print("Rubik's Cube Green-Red F2L Demo")
    print("===============================")
    print()

    scramble = generate_scramble(length=20)

    print("Scramble:")
    print(" ".join(scramble))

    cube.apply_algorithm(scramble)

    print()
    print("Solving bottom white cross...")
    cross_moves = solve_cross(cube)

    print()
    print("Cross moves:")
    print(cross_moves)

    print()
    print("Is white cross solved?")
    print(is_white_cross_solved(cube))

    print()
    print("Green-Red case before normalization:")
    print("------------------------------------")
    print_f2l_pair_case(cube, "Green-Red")

    print()
    print("Normalizing Green-Red pair...")
    print("-----------------------------")
    normalize_moves = normalize_green_red_pair(cube)

    print()
    print("Normalize moves:")
    print(normalize_moves)

    print()
    print("Green-Red case after normalization:")
    print("-----------------------------------")
    print_f2l_pair_case(cube, "Green-Red")

    print()
    print("Trying Green-Red insertion/extraction...")
    print("-----------------------------------------")
    f2l_moves = insert_green_red_pair(cube)

    print()
    print("F2L moves:")
    print(f2l_moves)

    print()
    print("Green-Red case after F2L operation:")
    print("-----------------------------------")
    print_f2l_pair_case(cube, "Green-Red")

    print()
    print("Is Green-Red solved?")
    print(is_f2l_pair_solved(cube, "Green-Red"))

    print()
    print("Is white cross still solved?")
    print(is_white_cross_solved(cube))


if __name__ == "__main__":
    main()  