from src.cube import RubiksCube
from src.solvers.cross_solver import (
    solve_bottom_white_green_edge,
    is_bottom_white_green_edge_solved,
    get_bottom_white_green_edge_case,
)


def run_bottom_white_green_case(setup_moves):
    cube = RubiksCube()

    cube.apply_algorithm(setup_moves)

    solve_bottom_white_green_edge(cube)

    assert is_bottom_white_green_edge_solved(cube) is True


def test_bottom_white_green_already_solved_at_df():
    cube = RubiksCube()

    cube.apply_algorithm(["F2"])

    assert get_bottom_white_green_edge_case(cube) == ("DF", ("W", "G"))

    solve_bottom_white_green_edge(cube)

    assert is_bottom_white_green_edge_solved(cube) is True


def test_bottom_white_green_top_layer_uf():
    run_bottom_white_green_case([])


def test_bottom_white_green_top_layer_ur():
    run_bottom_white_green_case(["U'"])


def test_bottom_white_green_top_layer_ub():
    run_bottom_white_green_case(["U2"])


def test_bottom_white_green_top_layer_ul():
    run_bottom_white_green_case(["U"])


def test_bottom_white_green_bottom_layer_dr():
    run_bottom_white_green_case(["F2", "D"])


def test_bottom_white_green_bottom_layer_db():
    run_bottom_white_green_case(["F2", "D2"])


def test_bottom_white_green_bottom_layer_dl():
    run_bottom_white_green_case(["F2", "D'"])

from src.solvers.cross_solver import (
    solve_bottom_white_red_edge,
    is_bottom_white_red_edge_solved,
    get_bottom_white_red_edge_case,
)


def run_bottom_white_red_case(setup_moves):
    cube = RubiksCube()

    cube.apply_algorithm(setup_moves)

    solve_bottom_white_red_edge(cube)

    assert is_bottom_white_red_edge_solved(cube) is True


def test_bottom_white_red_already_solved_at_dr():
    cube = RubiksCube()

    cube.apply_algorithm(["R2"])

    assert get_bottom_white_red_edge_case(cube) == ("DR", ("W", "R"))

    solve_bottom_white_red_edge(cube)

    assert is_bottom_white_red_edge_solved(cube) is True


def test_bottom_white_red_top_layer_ur():
    run_bottom_white_red_case([])


def test_bottom_white_red_top_layer_uf():
    run_bottom_white_red_case(["U"])


def test_bottom_white_red_top_layer_ub():
    run_bottom_white_red_case(["U'"])


def test_bottom_white_red_top_layer_ul():
    run_bottom_white_red_case(["U2"])


def test_bottom_white_red_bottom_layer_df():
    run_bottom_white_red_case(["R2", "D'"])


def test_bottom_white_red_bottom_layer_db():
    run_bottom_white_red_case(["R2", "D"])


def test_bottom_white_red_bottom_layer_dl():
    run_bottom_white_red_case(["R2", "D2"])

from src.solvers.cross_solver import (
    solve_bottom_white_blue_edge,
    is_bottom_white_blue_edge_solved,
    get_bottom_white_blue_edge_case,
)


def run_bottom_white_blue_case(setup_moves):
    cube = RubiksCube()

    cube.apply_algorithm(setup_moves)

    solve_bottom_white_blue_edge(cube)

    assert is_bottom_white_blue_edge_solved(cube) is True


def test_bottom_white_blue_already_solved_at_db():
    cube = RubiksCube()

    cube.apply_algorithm(["B2"])

    assert get_bottom_white_blue_edge_case(cube) == ("DB", ("W", "B"))

    solve_bottom_white_blue_edge(cube)

    assert is_bottom_white_blue_edge_solved(cube) is True


def test_bottom_white_blue_top_layer_ub():
    run_bottom_white_blue_case([])


def test_bottom_white_blue_top_layer_uf():
    run_bottom_white_blue_case(["U2"])


def test_bottom_white_blue_top_layer_ur():
    run_bottom_white_blue_case(["U"])


def test_bottom_white_blue_top_layer_ul():
    run_bottom_white_blue_case(["U'"])


def test_bottom_white_blue_bottom_layer_df():
    run_bottom_white_blue_case(["B2", "D2"])


def test_bottom_white_blue_bottom_layer_dr():
    run_bottom_white_blue_case(["B2", "D'"])


def test_bottom_white_blue_bottom_layer_dl():
    run_bottom_white_blue_case(["B2", "D"])

from src.solvers.cross_solver import (
    solve_bottom_white_orange_edge,
    is_bottom_white_orange_edge_solved,
    get_bottom_white_orange_edge_case,
)


def run_bottom_white_orange_case(setup_moves):
    cube = RubiksCube()

    cube.apply_algorithm(setup_moves)

    solve_bottom_white_orange_edge(cube)

    assert is_bottom_white_orange_edge_solved(cube) is True


def test_bottom_white_orange_already_solved_at_dl():
    cube = RubiksCube()

    cube.apply_algorithm(["L2"])

    assert get_bottom_white_orange_edge_case(cube) == ("DL", ("W", "O"))

    solve_bottom_white_orange_edge(cube)

    assert is_bottom_white_orange_edge_solved(cube) is True


def test_bottom_white_orange_top_layer_ul():
    run_bottom_white_orange_case([])


def test_bottom_white_orange_top_layer_uf():
    run_bottom_white_orange_case(["U'"])


def test_bottom_white_orange_top_layer_ur():
    run_bottom_white_orange_case(["U2"])


def test_bottom_white_orange_top_layer_ub():
    run_bottom_white_orange_case(["U"])


def test_bottom_white_orange_bottom_layer_df():
    run_bottom_white_orange_case(["L2", "D"])


def test_bottom_white_orange_bottom_layer_dr():
    run_bottom_white_orange_case(["L2", "D2"])


def test_bottom_white_orange_bottom_layer_db():
    run_bottom_white_orange_case(["L2", "D'"])

from src.solvers.cross_solver import solve_cross, is_white_cross_solved


FAILED_SCRAMBLE_REGRESSION_CASES = [
    ["L", "F", "F2", "D2", "B", "F'", "B", "F2"],
    ["L2", "L", "D'", "F2", "B'", "U", "F2", "L"],
    ["L'", "F", "B'", "L", "R", "F'", "D", "D2"],
    ["B", "B'", "B'", "L'", "F2", "D2", "F'", "D2"],
    ["R", "L'", "B", "D2", "B", "D'", "U2", "R2"],
    ["R2", "D", "B", "L'", "D", "D", "F", "B2"],
    ["D'", "F2", "L'", "R'", "B'", "U", "U2", "F'"],
    ["B2", "F", "U'", "D'", "L2", "D", "R2", "F2"],
]


def test_solve_cross_regression_failed_scrambles():
    for scramble in FAILED_SCRAMBLE_REGRESSION_CASES:
        cube = RubiksCube()

        cube.apply_algorithm(scramble)

        solve_cross(cube)

        assert is_white_cross_solved(cube) is True