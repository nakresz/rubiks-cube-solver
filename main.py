from src.cube import RubiksCube
from src.solvers.cross_solver import (
    solve_cross,
    is_white_cross_solved,
    print_white_cross_status,
)
from src.solvers.f2l_solver import (
    normalize_green_red_pair,
    print_f2l_pair_case,
    is_f2l_pair_solved,
)


CANDIDATE_INSERTION_ALGORITHMS = [
    ["U", "R", "U'", "R'", "U'", "F'", "U", "F"],
    ["R", "U", "R'", "U'", "R", "U", "R'"],
    ["R", "U'", "R'", "U", "F'", "U", "F"],
    ["F'", "U'", "F", "U", "R", "U'", "R'"],
    ["U'", "F'", "U", "F", "U", "R", "U'", "R'"],
    ["U", "R", "U'", "R'", "U", "R", "U'", "R'"],
    ["R", "U", "R'", "U2", "R", "U'", "R'"],
    ["F'", "U", "F", "U2", "R", "U", "R'"],
]


def build_current_test_case():
    """
    Rebuild the exact case from the last run:

    After scramble + cross + normalize, we reached:
        Green-Red corner: UFR
        Green-Red edge: UF
    """
    cube = RubiksCube()

    scramble = [
        "U2", "L'", "R", "R2", "U", "F", "D'", "D", "B2", "B",
        "B2", "F'", "D", "D2", "B2", "D'", "L", "U", "L'", "L'",
    ]

    cube.apply_algorithm(scramble)

    solve_cross(cube)

    normalize_green_red_pair(cube)

    return cube


def main():
    print("Green-Red F2L Insertion Algorithm Tester")
    print("========================================")
    print()

    base_cube = build_current_test_case()

    print("Base case after cross + normalization:")
    print("--------------------------------------")
    print_f2l_pair_case(base_cube, "Green-Red")

    print()
    print("Is white cross solved before testing?")
    print(is_white_cross_solved(base_cube))

    print()
    print("Testing candidate insertion algorithms...")
    print("-----------------------------------------")

    for index, algorithm in enumerate(CANDIDATE_INSERTION_ALGORITHMS, start=1):
        cube = build_current_test_case()

        print()
        print("=" * 70)
        print(f"Candidate #{index}")
        print("Algorithm:")
        print(algorithm)

        cube.apply_algorithm(algorithm)

        print()
        print("Green-Red case after algorithm:")
        print("-------------------------------")
        print_f2l_pair_case(cube, "Green-Red")

        green_red_solved = is_f2l_pair_solved(cube, "Green-Red")
        cross_solved = is_white_cross_solved(cube)

        print("Green-Red solved?")
        print(green_red_solved)

        print("White cross still solved?")
        print(cross_solved)

        if green_red_solved and cross_solved:
            print()
            print("FOUND WORKING INSERTION ALGORITHM!")
            print(algorithm)
            return

    print()
    print("No candidate solved this case yet.")


if __name__ == "__main__":
    main()