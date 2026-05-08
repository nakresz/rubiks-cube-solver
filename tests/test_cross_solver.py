from src.cube import RubiksCube
from src.solvers.cross_solver import (
    solve_white_green_edge,
    is_white_green_edge_solved,
    get_white_green_edge_case,
)


def run_white_green_case(setup_moves):
    cube = RubiksCube()

    cube.apply_algorithm(setup_moves)

    assert is_white_green_edge_solved(cube) is False or setup_moves == []

    solve_white_green_edge(cube)

    assert is_white_green_edge_solved(cube) is True


def test_white_green_already_solved():
    cube = RubiksCube()

    assert get_white_green_edge_case(cube) == ("UF", ("W", "G"))

    solve_white_green_edge(cube)

    assert is_white_green_edge_solved(cube) is True


def test_white_green_top_layer_ur():
    run_white_green_case(["U'"])


def test_white_green_top_layer_ub():
    run_white_green_case(["U2"])


def test_white_green_top_layer_ul():
    run_white_green_case(["U"])


def test_white_green_bottom_layer_df():
    run_white_green_case(["F2"])


def test_white_green_bottom_layer_dl():
    run_white_green_case(["F2", "D'"])


def test_white_green_bottom_layer_db():
    run_white_green_case(["F2", "D2"])


def test_white_green_bottom_layer_dr():
    run_white_green_case(["F2", "D"])


def test_white_green_middle_layer_fl_flipped():
    run_white_green_case(["F'", "U"])


def test_white_green_middle_layer_fr_flipped():
    run_white_green_case(["F", "U'"])


def test_white_green_middle_layer_bl_flipped():
    run_white_green_case(["U2", "B"])
    

def test_white_green_middle_layer_br_flipped():
    run_white_green_case(["U2", "B'"])