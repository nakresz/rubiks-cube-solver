from src.cube import RubiksCube
from src.moves import ALL_MOVES
from src.scrambler import generate_scramble
from src.piece_detector import (
    get_edge_pieces,
    get_corner_pieces,
    find_edge_by_colors,
    find_corner_by_colors,
    validate_edges,
    validate_corners,
    validate_pieces,
)


def test_solved_cube_edges_are_detected_correctly():
    cube = RubiksCube()

    edges = get_edge_pieces(cube)

    assert edges["UF"] == ["W", "G"]
    assert edges["UR"] == ["W", "R"]
    assert edges["UB"] == ["W", "B"]
    assert edges["UL"] == ["W", "O"]

    assert edges["DF"] == ["Y", "G"]
    assert edges["DR"] == ["Y", "R"]
    assert edges["DB"] == ["Y", "B"]
    assert edges["DL"] == ["Y", "O"]


def test_solved_cube_corners_are_detected_correctly():
    cube = RubiksCube()

    corners = get_corner_pieces(cube)

    assert corners["UFR"] == ["W", "G", "R"]
    assert corners["URB"] == ["W", "R", "B"]
    assert corners["UBL"] == ["W", "B", "O"]
    assert corners["ULF"] == ["W", "O", "G"]

    assert corners["DFR"] == ["Y", "G", "R"]
    assert corners["DRB"] == ["Y", "R", "B"]
    assert corners["DBL"] == ["Y", "B", "O"]
    assert corners["DLF"] == ["Y", "O", "G"]


def test_find_specific_edge_on_solved_cube():
    cube = RubiksCube()

    assert find_edge_by_colors(cube, ["W", "G"]) == "UF"
    assert find_edge_by_colors(cube, ["G", "W"]) == "UF"


def test_find_specific_corner_on_solved_cube():
    cube = RubiksCube()

    assert find_corner_by_colors(cube, ["W", "G", "R"]) == "UFR"
    assert find_corner_by_colors(cube, ["R", "W", "G"]) == "UFR"


def test_each_single_move_keeps_pieces_valid():
    for move in ALL_MOVES:
        cube = RubiksCube()

        cube.apply_move(move)

        assert validate_edges(cube) is True
        assert validate_corners(cube) is True
        assert validate_pieces(cube) is True


def test_random_scramble_keeps_pieces_valid_after_each_move():
    cube = RubiksCube()
    scramble = generate_scramble(length=50)

    for move in scramble:
        cube.apply_move(move)

        assert validate_edges(cube) is True
        assert validate_corners(cube) is True
        assert validate_pieces(cube) is True