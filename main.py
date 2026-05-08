from src.cube import RubiksCube
from src.scrambler import generate_scramble
from src.solvers.cross_solver import (
    solve_cross,
    is_white_cross_solved,
    print_white_cross_status,
)


def run_single_cross_test(test_number, scramble_length=8):
    """
    Run one random bottom white cross test.

    Returns:
        True if the bottom white cross is solved.
        False otherwise.
    """
    cube = RubiksCube()

    scramble = generate_scramble(length=scramble_length)

    print("=" * 70)
    print(f"Cross Test #{test_number}")
    print("=" * 70)

    print("Scramble:")
    print(" ".join(scramble))

    cube.apply_algorithm(scramble)

    print()
    print("White cross status before solving:")
    print("----------------------------------")
    print_white_cross_status(cube)

    print()
    print("Running bottom white cross solver...")
    print("------------------------------------")

    moves = solve_cross(cube)

    solved = is_white_cross_solved(cube)

    print()
    print("Moves used:")
    print(moves)

    print()
    print("White cross status after solving:")
    print("---------------------------------")
    print_white_cross_status(cube)

    print("Solved?")
    print(solved)

    return solved


def main():
    total_tests = 20
    scramble_length = 8

    passed = 0
    failed = 0

    print("Rubik's Cube Bottom White Cross Stress Test")
    print("===========================================")
    print()

    for test_number in range(1, total_tests + 1):
        solved = run_single_cross_test(
            test_number=test_number,
            scramble_length=scramble_length,
        )

        if solved:
            passed += 1
        else:
            failed += 1

    print()
    print("=" * 70)
    print("Final Stress Test Result")
    print("=" * 70)
    print(f"Total tests: {total_tests}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")
    print(f"Success rate: {(passed / total_tests) * 100:.1f}%")

    if failed == 0:
        print()
        print("Great! Bottom white cross solver solved all random tests.")
    else:
        print()
        print("Some tests failed. We will use those failed cases to improve the solver.")


if __name__ == "__main__":
    main()