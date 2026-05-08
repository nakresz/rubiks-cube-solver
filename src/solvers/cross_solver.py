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
        "position": "DF",
        "colors": ["W", "G"],
    },
    "White-Red": {
        "position": "DR",
        "colors": ["W", "R"],
    },
    "White-Blue": {
        "position": "DB",
        "colors": ["W", "B"],
    },
    "White-Orange": {
        "position": "DL",
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

    # Bottom layer flipped cases
    ("DB", ("G", "W")): ["B2", "U2", "F2"],

    # Top layer flipped cases
    ("UR", ("G", "W")): ["R", "F"],
    
}

WHITE_GREEN_TO_DF_ALGORITHMS = {
    # Already solved in bottom cross position
    ("DF", ("W", "G")): [],

    # Top layer cases
    ("UF", ("W", "G")): ["F2"],
    ("UR", ("W", "G")): ["U", "F2"],
    ("UB", ("W", "G")): ["U2", "F2"],
    ("UL", ("W", "G")): ["U'", "F2"],

    # Bottom layer cases
    ("DR", ("W", "G")): ["D'"],
    ("DB", ("W", "G")): ["D2"],
    ("DL", ("W", "G")): ["D"],

    # Simple flipped cases we will expand later
    ("UF", ("G", "W")): ["F", "U'", "R", "U"],

    # Middle/back layer cases
    ("BL", ("W", "G")): ["L", "U2", "F2"],
}

WHITE_RED_TO_DR_ALGORITHMS = {
    # Already solved in bottom cross position
    ("DR", ("W", "R")): [],

    # Top layer cases
    ("UR", ("W", "R")): ["R2"],
    ("UF", ("W", "R")): ["U'", "R2"],
    ("UB", ("W", "R")): ["U", "R2"],
    ("UL", ("W", "R")): ["U2", "R2"],

    # Bottom layer cases
    ("DF", ("W", "R")): ["D"],
    ("DB", ("W", "R")): ["D'"],
    ("DL", ("W", "R")): ["D2"],

    # Simple flipped cases we will expand later
    ("UR", ("R", "W")): ["R", "U", "B'", "U'"],
}

WHITE_BLUE_TO_DB_ALGORITHMS = {
    # Already solved in bottom cross position
    ("DB", ("W", "B")): [],

    # Top layer cases
    ("UB", ("W", "B")): ["B2"],
    ("UF", ("W", "B")): ["U2", "B2"],
    ("UR", ("W", "B")): ["U'", "B2"],
    ("UL", ("W", "B")): ["U", "B2"],

    # Bottom layer cases
    ("DF", ("W", "B")): ["D2"],
    ("DR", ("W", "B")): ["D"],
    ("DL", ("W", "B")): ["D'"],

    # Simple flipped cases we will expand later
    ("UB", ("B", "W")): ["B", "U", "R'", "U'"],
}

WHITE_ORANGE_TO_DL_ALGORITHMS = {
    # Already solved in bottom cross position
    ("DL", ("W", "O")): [],

    # Top layer cases
    ("UL", ("W", "O")): ["L2"],
    ("UF", ("W", "O")): ["U", "L2"],
    ("UR", ("W", "O")): ["U2", "L2"],
    ("UB", ("W", "O")): ["U'", "L2"],

    # Bottom layer cases
    ("DF", ("W", "O")): ["D'"],
    ("DR", ("W", "O")): ["D2"],
    ("DB", ("W", "O")): ["D"],

    # Simple flipped cases we will expand later
    ("UL", ("O", "W")): ["L", "U'", "F", "U"],
}

WHITE_RED_TO_UR_ALGORITHMS = {
    # Already in the correct place and orientation
    ("UR", ("W", "R")): [],

    # Top layer cases
    ("UF", ("W", "R")): ["U'"],
    ("UB", ("W", "R")): ["U"],
    ("UL", ("W", "R")): ["U2"],

    # Bottom layer cases
    ("DR", ("W", "R")): ["R2"],
    ("DB", ("W", "R")): ["B2", "U"],
    ("DL", ("W", "R")): ["L2", "U2"],
    ("DF", ("W", "R")): ["F2", "U'"],

    # Middle layer flipped cases
    ("FL", ("R", "W")): ["F'", "R2"],
}

WHITE_BLUE_TO_UB_ALGORITHMS = {
    # Already in the correct place and orientation
    ("UB", ("W", "B")): [],

    # Top layer cases
    ("UF", ("W", "B")): ["U2"],
    ("UR", ("W", "B")): ["U'"],
    ("UL", ("W", "B")): ["U"],

    # Bottom layer cases
    ("DB", ("W", "B")): ["B2"],
    ("DR", ("W", "B")): ["R2", "U'"],
    ("DF", ("W", "B")): ["F2", "U2"],
    ("DL", ("W", "B")): ["L2", "U"],

    # Top layer flipped cases
    ("UL", ("B", "W")): ["U", "B2"],
}

WHITE_ORANGE_TO_UL_ALGORITHMS = {
    # Already in the correct place and orientation
    ("UL", ("W", "O")): [],

    # Top layer cases
    ("UF", ("W", "O")): ["U"],
    ("UR", ("W", "O")): ["U2"],
    ("UB", ("W", "O")): ["U'"],

    # Bottom layer cases
    ("DL", ("W", "O")): ["L2"],
    ("DF", ("W", "O")): ["F2", "U"],
    ("DR", ("W", "O")): ["R2", "U2"],
    ("DB", ("W", "O")): ["B2", "U'"],

    # Middle layer cases
    ("FL", ("W", "O")): ["L'"],

    # Back middle layer flipped cases
    ("BL", ("O", "W")): ["L2", "U"],

    # Bottom layer flipped cases
    ("DB", ("O", "W")): ["B2", "U'", "L2"],
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

def is_bottom_white_green_edge_solved(cube):
    """
    Return True if the White-Green edge is solved at DF.
    """
    status = get_white_cross_status(cube)

    return status["White-Green"]["solved"] is True


def get_bottom_white_green_edge_case(cube):
    """
    Get the current White-Green edge case for bottom-cross solving.

    Returns:
        A tuple:
            (current_position, current_colors_tuple)
    """
    status = get_white_cross_status(cube)
    white_green_status = status["White-Green"]

    current_position = white_green_status["current_position"]
    current_colors = white_green_status["current_colors"]

    if current_position is None or current_colors is None:
        return None

    return current_position, tuple(current_colors)


def solve_bottom_white_green_edge(cube):
    """
    Try to solve the White-Green edge into the bottom cross position DF.
    """
    edge_case = get_bottom_white_green_edge_case(cube)

    if edge_case is None:
        print("[Bottom Cross Solver] White-Green edge could not be found.")
        return []

    print(f"[Bottom Cross Solver] White-Green edge case: {edge_case}")

    if edge_case not in WHITE_GREEN_TO_DF_ALGORITHMS:
        print("[Bottom Cross Solver] No algorithm implemented for this White-Green bottom case yet.")
        return []

    moves = WHITE_GREEN_TO_DF_ALGORITHMS[edge_case]

    print(f"[Bottom Cross Solver] Moves for White-Green edge: {moves}")

    cube.apply_algorithm(moves)

    return moves

def is_bottom_white_red_edge_solved(cube):
    """
    Return True if the White-Red edge is solved at DR.
    """
    status = get_white_cross_status(cube)

    return status["White-Red"]["solved"] is True


def get_bottom_white_red_edge_case(cube):
    """
    Get the current White-Red edge case for bottom-cross solving.

    Returns:
        A tuple:
            (current_position, current_colors_tuple)
    """
    status = get_white_cross_status(cube)
    white_red_status = status["White-Red"]

    current_position = white_red_status["current_position"]
    current_colors = white_red_status["current_colors"]

    if current_position is None or current_colors is None:
        return None

    return current_position, tuple(current_colors)


def solve_bottom_white_red_edge(cube):
    """
    Try to solve the White-Red edge into the bottom cross position DR.
    """
    edge_case = get_bottom_white_red_edge_case(cube)

    if edge_case is None:
        print("[Bottom Cross Solver] White-Red edge could not be found.")
        return []

    print(f"[Bottom Cross Solver] White-Red edge case: {edge_case}")

    if edge_case not in WHITE_RED_TO_DR_ALGORITHMS:
        print("[Bottom Cross Solver] No algorithm implemented for this White-Red bottom case yet.")
        return []

    moves = WHITE_RED_TO_DR_ALGORITHMS[edge_case]

    print(f"[Bottom Cross Solver] Moves for White-Red edge: {moves}")

    cube.apply_algorithm(moves)

    return moves

def is_bottom_white_blue_edge_solved(cube):
    """
    Return True if the White-Blue edge is solved at DB.
    """
    status = get_white_cross_status(cube)

    return status["White-Blue"]["solved"] is True


def get_bottom_white_blue_edge_case(cube):
    """
    Get the current White-Blue edge case for bottom-cross solving.

    Returns:
        A tuple:
            (current_position, current_colors_tuple)
    """
    status = get_white_cross_status(cube)
    white_blue_status = status["White-Blue"]

    current_position = white_blue_status["current_position"]
    current_colors = white_blue_status["current_colors"]

    if current_position is None or current_colors is None:
        return None

    return current_position, tuple(current_colors)


def solve_bottom_white_blue_edge(cube):
    """
    Try to solve the White-Blue edge into the bottom cross position DB.
    """
    edge_case = get_bottom_white_blue_edge_case(cube)

    if edge_case is None:
        print("[Bottom Cross Solver] White-Blue edge could not be found.")
        return []

    print(f"[Bottom Cross Solver] White-Blue edge case: {edge_case}")

    if edge_case not in WHITE_BLUE_TO_DB_ALGORITHMS:
        print("[Bottom Cross Solver] No algorithm implemented for this White-Blue bottom case yet.")
        return []

    moves = WHITE_BLUE_TO_DB_ALGORITHMS[edge_case]

    print(f"[Bottom Cross Solver] Moves for White-Blue edge: {moves}")

    cube.apply_algorithm(moves)

    return moves

def is_bottom_white_orange_edge_solved(cube):
    """
    Return True if the White-Orange edge is solved at DL.
    """
    status = get_white_cross_status(cube)

    return status["White-Orange"]["solved"] is True


def get_bottom_white_orange_edge_case(cube):
    """
    Get the current White-Orange edge case for bottom-cross solving.

    Returns:
        A tuple:
            (current_position, current_colors_tuple)
    """
    status = get_white_cross_status(cube)
    white_orange_status = status["White-Orange"]

    current_position = white_orange_status["current_position"]
    current_colors = white_orange_status["current_colors"]

    if current_position is None or current_colors is None:
        return None

    return current_position, tuple(current_colors)


def solve_bottom_white_orange_edge(cube):
    """
    Try to solve the White-Orange edge into the bottom cross position DL.
    """
    edge_case = get_bottom_white_orange_edge_case(cube)

    if edge_case is None:
        print("[Bottom Cross Solver] White-Orange edge could not be found.")
        return []

    print(f"[Bottom Cross Solver] White-Orange edge case: {edge_case}")

    if edge_case not in WHITE_ORANGE_TO_DL_ALGORITHMS:
        print("[Bottom Cross Solver] No algorithm implemented for this White-Orange bottom case yet.")
        return []

    moves = WHITE_ORANGE_TO_DL_ALGORITHMS[edge_case]

    print(f"[Bottom Cross Solver] Moves for White-Orange edge: {moves}")

    cube.apply_algorithm(moves)

    return moves

def is_white_red_edge_solved(cube):
    """
    Return True if the White-Red edge is solved at UR.
    """
    status = get_white_cross_status(cube)

    return status["White-Red"]["solved"] is True


def get_white_red_edge_case(cube):
    """
    Get the current White-Red edge case.

    Returns:
        A tuple:
            (current_position, current_colors_tuple)

    Example:
        ("DR", ("W", "R"))
    """
    status = get_white_cross_status(cube)
    white_red_status = status["White-Red"]

    current_position = white_red_status["current_position"]
    current_colors = white_red_status["current_colors"]

    if current_position is None or current_colors is None:
        return None

    return current_position, tuple(current_colors)


def solve_white_red_edge(cube):
    """
    Try to solve only the White-Red cross edge.

    This is the second real move-generation step of the cross solver.

    Important:
        This is still a limited beginner version.
        It only knows some simple top-layer and bottom-layer cases.
    """
    edge_case = get_white_red_edge_case(cube)

    if edge_case is None:
        print("[Cross Solver] White-Red edge could not be found.")
        return []

    print(f"[Cross Solver] White-Red edge case: {edge_case}")

    if edge_case not in WHITE_RED_TO_UR_ALGORITHMS:
        print("[Cross Solver] No algorithm implemented for this White-Red case yet.")
        return []

    moves = WHITE_RED_TO_UR_ALGORITHMS[edge_case]

    print(f"[Cross Solver] Moves for White-Red edge: {moves}")

    cube.apply_algorithm(moves)

    return moves

def is_white_blue_edge_solved(cube):
    """
    Return True if the White-Blue edge is solved at UB.
    """
    status = get_white_cross_status(cube)

    return status["White-Blue"]["solved"] is True


def get_white_blue_edge_case(cube):
    """
    Get the current White-Blue edge case.

    Returns:
        A tuple:
            (current_position, current_colors_tuple)

    Example:
        ("DB", ("W", "B"))
    """
    status = get_white_cross_status(cube)
    white_blue_status = status["White-Blue"]

    current_position = white_blue_status["current_position"]
    current_colors = white_blue_status["current_colors"]

    if current_position is None or current_colors is None:
        return None

    return current_position, tuple(current_colors)


def solve_white_blue_edge(cube):
    """
    Try to solve only the White-Blue cross edge.

    This is the third move-generation step of the cross solver.
    """
    edge_case = get_white_blue_edge_case(cube)

    if edge_case is None:
        print("[Cross Solver] White-Blue edge could not be found.")
        return []

    print(f"[Cross Solver] White-Blue edge case: {edge_case}")

    if edge_case not in WHITE_BLUE_TO_UB_ALGORITHMS:
        print("[Cross Solver] No algorithm implemented for this White-Blue case yet.")
        return []

    moves = WHITE_BLUE_TO_UB_ALGORITHMS[edge_case]

    print(f"[Cross Solver] Moves for White-Blue edge: {moves}")

    cube.apply_algorithm(moves)

    return moves

def is_white_orange_edge_solved(cube):
    """
    Return True if the White-Orange edge is solved at UL.
    """
    status = get_white_cross_status(cube)

    return status["White-Orange"]["solved"] is True


def get_white_orange_edge_case(cube):
    """
    Get the current White-Orange edge case.

    Returns:
        A tuple:
            (current_position, current_colors_tuple)

    Example:
        ("DL", ("W", "O"))
    """
    status = get_white_cross_status(cube)
    white_orange_status = status["White-Orange"]

    current_position = white_orange_status["current_position"]
    current_colors = white_orange_status["current_colors"]

    if current_position is None or current_colors is None:
        return None

    return current_position, tuple(current_colors)


def solve_white_orange_edge(cube):
    """
    Try to solve only the White-Orange cross edge.

    This is the fourth move-generation step of the cross solver.
    """
    edge_case = get_white_orange_edge_case(cube)

    if edge_case is None:
        print("[Cross Solver] White-Orange edge could not be found.")
        return []

    print(f"[Cross Solver] White-Orange edge case: {edge_case}")

    if edge_case not in WHITE_ORANGE_TO_UL_ALGORITHMS:
        print("[Cross Solver] No algorithm implemented for this White-Orange case yet.")
        return []

    moves = WHITE_ORANGE_TO_UL_ALGORITHMS[edge_case]

    print(f"[Cross Solver] Moves for White-Orange edge: {moves}")

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
    Try to solve the full bottom white cross.

    Current strategy:
        1. Solve White-Green edge to DF
        2. Solve White-Red edge to DR
        3. Solve White-Blue edge to DB
        4. Solve White-Orange edge to DL

    Important:
        This is the first bottom-cross pipeline version.
        Individual edge solvers are tested, but the full sequence
        may still fail on some scrambles until protected strategy is improved.
    """
    full_moves = []

    print("[Bottom Cross Solver] Starting full bottom white cross attempt...")
    print()

    print("[Bottom Cross Solver] Initial white cross status:")
    print_white_cross_status(cube)

    print("[Bottom Cross Solver] Step 1: Solving White-Green edge to DF...")
    green_moves = solve_bottom_white_green_edge(cube)
    full_moves.extend(green_moves)

    print()
    print("[Bottom Cross Solver] Status after White-Green:")
    print_white_cross_status(cube)

    print("[Bottom Cross Solver] Step 2: Solving White-Red edge to DR...")
    red_moves = solve_bottom_white_red_edge(cube)
    full_moves.extend(red_moves)

    print()
    print("[Bottom Cross Solver] Status after White-Red:")
    print_white_cross_status(cube)

    print("[Bottom Cross Solver] Step 3: Solving White-Blue edge to DB...")
    blue_moves = solve_bottom_white_blue_edge(cube)
    full_moves.extend(blue_moves)

    print()
    print("[Bottom Cross Solver] Status after White-Blue:")
    print_white_cross_status(cube)

    print("[Bottom Cross Solver] Step 4: Solving White-Orange edge to DL...")
    orange_moves = solve_bottom_white_orange_edge(cube)
    full_moves.extend(orange_moves)

    print()
    print("[Bottom Cross Solver] Final white cross status:")
    print_white_cross_status(cube)

    if is_white_cross_solved(cube):
        print("[Bottom Cross Solver] Bottom white cross solved successfully.")
    else:
        print("[Bottom Cross Solver] Bottom white cross is not fully solved yet.")
        print("[Bottom Cross Solver] More protected strategy is needed.")

    return full_moves