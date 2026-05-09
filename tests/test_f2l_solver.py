from src.cube import RubiksCube
from src.solvers.f2l_solver import (
    find_f2l_pair,
    find_all_f2l_pairs,
    get_f2l_status,
    get_f2l_pair_case,
    normalize_green_red_pair,
    is_f2l_pair_solved,
    is_f2l_solved,
)

def test_find_green_red_f2l_pair_on_initial_cube():
    cube = RubiksCube()

    pair = find_f2l_pair(cube, "Green-Red")

    assert pair["corner_position"] == "DFR"
    assert pair["edge_position"] == "FR"
    assert pair["corner_stickers"] == ["W", "G", "R"]
    assert pair["edge_stickers"] == ["G", "R"]

def test_find_red_blue_f2l_pair_on_initial_cube():
    cube = RubiksCube()

    pair = find_f2l_pair(cube, "Red-Blue")

    assert pair["corner_position"] == "DRB"
    assert pair["edge_position"] == "BR"
    assert pair["corner_stickers"] == ["W", "R", "B"]
    assert pair["edge_stickers"] == ["B", "R"]

def test_find_blue_orange_f2l_pair_on_initial_cube():
    cube = RubiksCube()

    pair = find_f2l_pair(cube, "Blue-Orange")

    assert pair["corner_position"] == "DBL"
    assert pair["edge_position"] == "BL"
    assert pair["corner_stickers"] == ["W", "B", "O"]
    assert pair["edge_stickers"] == ["B", "O"]

def test_find_orange_green_f2l_pair_on_initial_cube():
    cube = RubiksCube()

    pair = find_f2l_pair(cube, "Orange-Green")

    assert pair["corner_position"] == "DLF"
    assert pair["edge_position"] == "FL"
    assert pair["corner_stickers"] == ["W", "O", "G"]
    assert pair["edge_stickers"] == ["G", "O"]

def test_find_all_f2l_pairs_returns_four_pairs():
    cube = RubiksCube()

    pairs = find_all_f2l_pairs(cube)

    assert set(pairs.keys()) == {
        "Green-Red",
        "Red-Blue",
        "Blue-Orange",
        "Orange-Green",
    }


def test_f2l_status_contains_all_pairs():
    cube = RubiksCube()

    status = get_f2l_status(cube)

    assert set(status.keys()) == {
        "Green-Red",
        "Red-Blue",
        "Blue-Orange",
        "Orange-Green",
    }


def test_initial_cube_is_f2l_solved_for_bottom_white_orientation():
    cube = RubiksCube()

    assert is_f2l_solved(cube) is True

def test_individual_pairs_solved_on_initial_cube_for_bottom_white_orientation():
    cube = RubiksCube()

    assert is_f2l_pair_solved(cube, "Green-Red") is True
    assert is_f2l_pair_solved(cube, "Red-Blue") is True
    assert is_f2l_pair_solved(cube, "Blue-Orange") is True
    assert is_f2l_pair_solved(cube, "Orange-Green") is True

def test_green_red_f2l_case_on_initial_cube():
    cube = RubiksCube()

    pair_case = get_f2l_pair_case(cube, "Green-Red")

    assert pair_case["corner_position"] == "DFR"
    assert pair_case["edge_position"] == "FR"

    assert pair_case["corner_in_top"] is False
    assert pair_case["corner_in_bottom"] is True

    assert pair_case["edge_in_top"] is False
    assert pair_case["edge_in_middle"] is True
    assert pair_case["edge_in_bottom"] is False

    assert pair_case["corner_in_target_slot"] is True
    assert pair_case["edge_in_target_slot"] is True

    assert pair_case["corner_orientation_correct"] is True
    assert pair_case["edge_orientation_correct"] is True

    assert pair_case["case_type"] == "solved"
    assert pair_case["solved"] is True

def test_all_f2l_pair_cases_have_case_type():
    cube = RubiksCube()

    for pair_name in [
        "Green-Red",
        "Red-Blue",
        "Blue-Orange",
        "Orange-Green",
    ]:
        pair_case = get_f2l_pair_case(cube, pair_name)

        assert "case_type" in pair_case
        assert pair_case["case_type"] in {
            "solved",
            "inserted_but_corner_twisted",
            "corner_top_edge_top",
            "corner_top_edge_middle",
            "corner_top_edge_bottom",
            "corner_bottom_edge_top",
            "corner_bottom_edge_middle",
            "corner_bottom_edge_bottom",
            "unknown",
        }


def test_normalize_green_red_pair_keeps_white_cross_solved():
    from src.scrambler import generate_scramble
    from src.solvers.cross_solver import solve_cross, is_white_cross_solved

    cube = RubiksCube()

    scramble = generate_scramble(length=20)
    cube.apply_algorithm(scramble)

    solve_cross(cube)

    assert is_white_cross_solved(cube) is True

    normalize_green_red_pair(cube)

    assert is_white_cross_solved(cube) is True
