"""
Cross solver module.

This module handles the first step of the CFOP method:
solving the white cross.
"""

from src.piece_detector import find_edge_by_colors, get_edge_pieces


WHITE_CROSS_EDGES = [
    ("White-Green", ["W", "G"]),
    ("White-Red", ["W", "R"]),
    ("White-Blue", ["W", "B"]),
    ("White-Orange", ["W", "O"]),
]


WHITE_CROSS_TARGETS = {
    "White-Green": {
        "position": "UF",
        "colors": ["W", "G"],
    },
    "White-Red": {
        "position": "UR",
        "colors": ["W", "R"],
    },
    "White-Blue": {
        "position": "UB",
        "colors": ["W", "B"],
    },
    "White-Orange": {
        "position": "UL",
        "colors": ["W", "O"],
    },
}


WHITE_GREEN_TO_UF_ALGORITHMS = {
    # Already in the correct place and orientation
    ("UF", ("W", "G")): [],

    # Correct position but flipped
    # This is a simple beginner-style flip setup.
    ("UF", ("G", "W")): ["F", "U'", "R", "U"],

    # Top layer cases
    ("UR", ("W", "G")): ["U"],
    ("UB", ("W", "G")): ["U2"],
    ("UL", ("W", "G")): ["U'"],

    # Bottom layer cases
    ("DF", ("W", "G")): ["F2"],
    ("DR", ("W", "G")): ["R2", "U"],
    ("DB", ("W", "G")): ["B2", "U2"],
    ("DL", ("W", "G")): ["L2", "U'"],

    # Middle layer simple cases
    ("FR", ("W", "G")): ["R", "U"],
    ("FL", ("W", "G")): ["L'", "U'"],
    ("BR", ("W", "G")): ["R'", "U"],
    ("BL", ("W", "G")): ["L", "U'"],

    # Middle layer flipped cases
    ("FR", ("G", "W")): ["F", "F2"],
    ("FL", ("G", "W")): ["F'", "F2"],

    # Back middle layer flipped cases
    ("BL", ("G", "W")): ["L2", "F"],
    ("BR", ("G", "W")): ["R2", "F'"],
    
}


def find_white_cross_edges(cube):
    """
    Find the four white edge pieces needed for the white cross.

    Returns:
        A dictionary where:
            key   = human-readable edge name
            value = current edge position
    """
    cross_edges = {}

    for edge_name, colors in WHITE_CROSS_EDGES:
        position = find_edge_by_colors(cube, colors)
        cross_edges[edge_name] = position

    return cross_edges


def get_white_cross_status(cube):
    """
    Check the status of each white cross edge.
    """
    edges = get_edge_pieces(cube)
    current_positions = find_white_cross_edges(cube)

    status = {}

    for edge_name, target_data in WHITE_CROSS_TARGETS.items():
        current_position = current_positions[edge_name]
        target_position = target_data["position"]
        target_colors = target_data["colors"]

        current_colors = None
        position_correct = False
        orientation_correct = False

        if current_position is not None:
            current_colors = edges[current_position]
            position_correct = current_position == target_position
            orientation_correct = current_colors == target_colors

        status[edge_name] = {
            "current_position": current_position,
            "target_position": target_position,
            "current_colors": current_colors,
            "target_colors": target_colors,
            "position_correct": position_correct,
            "orientation_correct": orientation_correct,
            "solved": position_correct and orientation_correct,
        }

    return status


def is_white_cross_solved(cube):
    """
    Return True if all four white cross edges are solved.
    """
    status = get_white_cross_status(cube)

    for edge_status in status.values():
        if edge_status["solved"] is not True:
            return False

    return True


def is_white_green_edge_solved(cube):
    """
    Return True if the White-Green edge is solved at UF.
    """
    status = get_white_cross_status(cube)

    return status["White-Green"]["solved"] is True


def get_white_green_edge_case(cube):
    """
    Get the current White-Green edge case.

    Returns:
        A tuple:
            (current_position, current_colors_tuple)

    Example:
        ("DF", ("W", "G"))
    """
    status = get_white_cross_status(cube)
    white_green_status = status["White-Green"]

    current_position = white_green_status["current_position"]
    current_colors = white_green_status["current_colors"]

    if current_position is None or current_colors is None:
        return None

    return current_position, tuple(current_colors)


def solve_white_green_edge(cube):
    """
    Try to solve only the White-Green cross edge.

    This is the first real move-generation step of the cross solver.

    Important:
        This is still a limited beginner version.
        It only knows some simple cases.
    """
    edge_case = get_white_green_edge_case(cube)

    if edge_case is None:
        print("[Cross Solver] White-Green edge could not be found.")
        return []

    print(f"[Cross Solver] White-Green edge case: {edge_case}")

    if edge_case not in WHITE_GREEN_TO_UF_ALGORITHMS:
        print("[Cross Solver] No algorithm implemented for this case yet.")
        return []

    moves = WHITE_GREEN_TO_UF_ALGORITHMS[edge_case]

    print(f"[Cross Solver] Moves for White-Green edge: {moves}")

    cube.apply_algorithm(moves)

    return moves


def print_white_cross_report(cube):
    """
    Print a readable report showing where each white cross edge is located.
    """
    cross_edges = find_white_cross_edges(cube)

    print("White Cross Edge Report")
    print("-----------------------")

    for edge_name, position in cross_edges.items():
        print(f"{edge_name} edge is currently at: {position}")


def print_white_cross_status(cube):
    """
    Print a detailed status report for the white cross.
    """
    status = get_white_cross_status(cube)

    print("White Cross Status")
    print("------------------")

    for edge_name, edge_status in status.items():
        print(f"{edge_name}:")
        print(f"  Current position:     {edge_status['current_position']}")
        print(f"  Target position:      {edge_status['target_position']}")
        print(f"  Current colors:       {edge_status['current_colors']}")
        print(f"  Target colors:        {edge_status['target_colors']}")
        print(f"  Position correct?     {edge_status['position_correct']}")
        print(f"  Orientation correct?  {edge_status['orientation_correct']}")
        print(f"  Solved?               {edge_status['solved']}")
        print()


def solve_cross(cube):
    """
    Solve the white cross step of the cube.

    For now, this function only tries to solve the White-Green edge.
    """
    full_moves = []

    print("[Cross Solver] Checking white cross status before solving...")
    print_white_cross_status(cube)

    white_green_moves = solve_white_green_edge(cube)
    full_moves.extend(white_green_moves)

    print()
    print("[Cross Solver] Checking white cross status after White-Green attempt...")
    print_white_cross_status(cube)

    return full_moves