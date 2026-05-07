from src.cube import RubiksCube
from src.moves import ALL_MOVES
from src.scrambler import inverse_move, generate_scramble, inverse_algorithm


def test_solved_cube_is_solved():
    cube = RubiksCube()

    assert cube.is_solved() is True


def test_each_move_followed_by_inverse_returns_to_solved_state():
    for move in ALL_MOVES:
        cube = RubiksCube()

        cube.apply_move(move)
        cube.apply_move(inverse_move(move))

        assert cube.is_solved() is True


def test_each_move_applied_four_times_returns_to_solved_state():
    for move in ["U", "D", "R", "L", "F", "B"]:
        cube = RubiksCube()

        cube.apply_algorithm([move, move, move, move])

        assert cube.is_solved() is True


def test_scramble_followed_by_inverse_solution_returns_to_solved_state():
    cube = RubiksCube()

    scramble = generate_scramble(length=30)
    solution = inverse_algorithm(scramble)

    cube.apply_algorithm(scramble)
    cube.apply_algorithm(solution)

    assert cube.is_solved() is True