"""
Piece detection utilities for the Rubik's Cube.

This module reads the current sticker state of the cube and extracts
edge and corner pieces.

Important:
    The cube itself is stored as stickers.
    But CFOP needs pieces.

    Cross needs edge pieces.
    F2L needs edge + corner pairs.
    OLL/PLL need last-layer orientation and permutation.
"""


EDGE_POSITIONS = [
    ("UF", [("U", 7), ("F", 1)]),
    ("UR", [("U", 5), ("R", 1)]),
    ("UB", [("U", 1), ("B", 1)]),
    ("UL", [("U", 3), ("L", 1)]),

    ("FR", [("F", 5), ("R", 3)]),
    ("FL", [("F", 3), ("L", 5)]),
    ("BR", [("B", 3), ("R", 5)]),
    ("BL", [("B", 5), ("L", 3)]),

    ("DF", [("D", 1), ("F", 7)]),
    ("DR", [("D", 5), ("R", 7)]),
    ("DB", [("D", 7), ("B", 7)]),
    ("DL", [("D", 3), ("L", 7)]),
]


CORNER_POSITIONS = [
    ("UFR", [("U", 8), ("F", 2), ("R", 0)]),
    ("URB", [("U", 2), ("R", 2), ("B", 0)]),
    ("UBL", [("U", 0), ("B", 2), ("L", 0)]),
    ("ULF", [("U", 6), ("L", 2), ("F", 0)]),

    ("DFR", [("D", 2), ("F", 8), ("R", 6)]),
    ("DRB", [("D", 8), ("R", 8), ("B", 6)]),
    ("DBL", [("D", 6), ("B", 8), ("L", 6)]),
    ("DLF", [("D", 0), ("L", 8), ("F", 6)]),
]


def get_sticker(cube, face_name, sticker_index):
    """
    Return one sticker from the cube.

    Example:
        get_sticker(cube, "U", 0)
    """
    return cube.faces[face_name][sticker_index]


def get_edge_pieces(cube):
    """
    Return all edge pieces of the cube.

    Returns:
        A dictionary where:
            key   = edge position name
            value = list of colors at that position

    Example:
        {
            "UF": ["W", "G"],
            "UR": ["W", "R"],
            ...
        }
    """
    edges = {}

    for position_name, stickers in EDGE_POSITIONS:
        colors = []

        for face_name, sticker_index in stickers:
            color = get_sticker(cube, face_name, sticker_index)
            colors.append(color)

        edges[position_name] = colors

    return edges


def get_corner_pieces(cube):
    """
    Return all corner pieces of the cube.

    Returns:
        A dictionary where:
            key   = corner position name
            value = list of colors at that position

    Example:
        {
            "UFR": ["W", "G", "R"],
            "URB": ["W", "R", "B"],
            ...
        }
    """
    corners = {}

    for position_name, stickers in CORNER_POSITIONS:
        colors = []

        for face_name, sticker_index in stickers:
            color = get_sticker(cube, face_name, sticker_index)
            colors.append(color)

        corners[position_name] = colors

    return corners


def find_edge_by_colors(cube, target_colors):
    """
    Find an edge piece by its two colors.

    Parameters:
        cube: RubiksCube object
        target_colors: list or tuple of two colors

    Returns:
        The position name where the edge is found.

    Example:
        find_edge_by_colors(cube, ["W", "G"]) -> "UF"

    Important:
        Order does not matter.
        ["W", "G"] and ["G", "W"] represent the same edge piece.
    """
    target_set = set(target_colors)
    edges = get_edge_pieces(cube)

    for position_name, colors in edges.items():
        if set(colors) == target_set:
            return position_name

    return None


def find_corner_by_colors(cube, target_colors):
    """
    Find a corner piece by its three colors.

    Parameters:
        cube: RubiksCube object
        target_colors: list or tuple of three colors

    Returns:
        The position name where the corner is found.

    Example:
        find_corner_by_colors(cube, ["W", "G", "R"]) -> "UFR"

    Important:
        Order does not matter.
    """
    target_set = set(target_colors)
    corners = get_corner_pieces(cube)

    for position_name, colors in corners.items():
        if set(colors) == target_set:
            return position_name

    return None

VALID_EDGES = [
    {"W", "G"},
    {"W", "R"},
    {"W", "B"},
    {"W", "O"},
    {"Y", "G"},
    {"Y", "R"},
    {"Y", "B"},
    {"Y", "O"},
    {"G", "R"},
    {"G", "O"},
    {"B", "R"},
    {"B", "O"},
]


VALID_CORNERS = [
    {"W", "G", "R"},
    {"W", "R", "B"},
    {"W", "B", "O"},
    {"W", "O", "G"},
    {"Y", "G", "R"},
    {"Y", "R", "B"},
    {"Y", "B", "O"},
    {"Y", "O", "G"},
]


def validate_edges(cube):
    """
    Check whether all detected edge pieces are valid Rubik's Cube edges.
    """
    edges = get_edge_pieces(cube)

    detected_edges = []

    for colors in edges.values():
        detected_edges.append(set(colors))

    for valid_edge in VALID_EDGES:
        if valid_edge not in detected_edges:
            return False

    return True


def validate_corners(cube):
    """
    Check whether all detected corner pieces are valid Rubik's Cube corners.
    """
    corners = get_corner_pieces(cube)

    detected_corners = []

    for colors in corners.values():
        detected_corners.append(set(colors))

    for valid_corner in VALID_CORNERS:
        if valid_corner not in detected_corners:
            return False

    return True


def validate_pieces(cube):
    """
    Check both edges and corners.
    """
    return validate_edges(cube) and validate_corners(cube)