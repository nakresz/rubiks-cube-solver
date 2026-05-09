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

    assert edges["UF"] == ["Y", "G"]
    assert edges["UR"] == ["Y", "R"]
    assert edges["UB"] == ["Y", "B"]
    assert edges["UL"] == ["Y", "O"]

    assert edges["DF"] == ["W", "G"]
    assert edges["DR"] == ["W", "R"]
    assert edges["DB"] == ["W", "B"]
    assert edges["DL"] == ["W", "O"]

def test_solved_cube_corners_are_detected_correctly():
    cube = RubiksCube()

    corners = get_corner_pieces(cube)

    assert corners["UFR"] == ["Y", "G", "R"]
    assert corners["URB"] == ["Y", "R", "B"]
    assert corners["UBL"] == ["Y", "B", "O"]
    assert corners["ULF"] == ["Y", "O", "G"]

    assert corners["DFR"] == ["W", "G", "R"]
    assert corners["DRB"] == ["W", "R", "B"]
    assert corners["DBL"] == ["W", "B", "O"]
    assert corners["DLF"] == ["W", "O", "G"]

def test_find_specific_edge_on_solved_cube():
    cube = RubiksCube()

    assert find_edge_by_colors(cube, ["W", "G"]) == "DF"
    assert find_edge_by_colors(cube, ["W", "R"]) == "DR"
    assert find_edge_by_colors(cube, ["W", "B"]) == "DB"
    assert find_edge_by_colors(cube, ["W", "O"]) == "DL"

def test_find_specific_corner_on_solved_cube():
    cube = RubiksCube()

    assert find_corner_by_colors(cube, ["W", "G", "R"]) == "DFR"
    assert find_corner_by_colors(cube, ["W", "R", "B"]) == "DRB"
    assert find_corner_by_colors(cube, ["W", "B", "O"]) == "DBL"
    assert find_corner_by_colors(cube, ["W", "O", "G"]) == "DLF"

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
