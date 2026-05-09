"""
F2L solver module.

This module will handle the second step of the CFOP method:
solving the first two layers.

For now, we only detect F2L pairs.
Actual solving algorithms will be added later.
"""

from src.piece_detector import find_edge_by_colors, find_corner_by_colors
from src.piece_detector import get_edge_pieces, get_corner_pieces


F2L_PAIRS = {
    "Green-Red": {
        "corner_colors": ["W", "G", "R"],
        "edge_colors": ["G", "R"],
        "corner_target": "DFR",
        "edge_target": "FR",
        "corner_target_stickers": ["W", "G", "R"],
        "edge_target_stickers": ["G", "R"],
    },
    "Red-Blue": {
        "corner_colors": ["W", "R", "B"],
        "edge_colors": ["R", "B"],
        "corner_target": "DRB",
        "edge_target": "BR",
        "corner_target_stickers": ["W", "R", "B"],
        "edge_target_stickers": ["B", "R"],
    },
    "Blue-Orange": {
        "corner_colors": ["W", "B", "O"],
        "edge_colors": ["B", "O"],
        "corner_target": "DBL",
        "edge_target": "BL",
        "corner_target_stickers": ["W", "B", "O"],
        "edge_target_stickers": ["B", "O"],
    },
    "Orange-Green": {
        "corner_colors": ["W", "O", "G"],
        "edge_colors": ["O", "G"],
        "corner_target": "DLF",
        "edge_target": "FL",
        "corner_target_stickers": ["W", "O", "G"],
        "edge_target_stickers": ["G", "O"],
    },
}

TOP_CORNER_POSITIONS = {"UFR", "URB", "UBL", "ULF"}
BOTTOM_CORNER_POSITIONS = {"DFR", "DRB", "DBL", "DLF"}

TOP_EDGE_POSITIONS = {"UF", "UR", "UB", "UL"}
MIDDLE_EDGE_POSITIONS = {"FR", "BR", "BL", "FL"}
BOTTOM_EDGE_POSITIONS = {"DF", "DR", "DB", "DL"}


def find_f2l_pair(cube, pair_name):
    """
    Find one F2L pair on the cube.

    Args:
        cube:
            RubiksCube object.

        pair_name:
            One of:
                - Green-Red
                - Red-Blue
                - Blue-Orange
                - Orange-Green

    Returns:
        A dictionary containing:
            - pair name
            - corner colors
            - edge colors
            - current corner position
            - current edge position
            - target corner position
            - target edge position
            - current corner stickers
            - current edge stickers
    """
    pair_data = F2L_PAIRS[pair_name]

    edges = get_edge_pieces(cube)
    corners = get_corner_pieces(cube)

    corner_position = find_corner_by_colors(
        cube,
        pair_data["corner_colors"],
    )

    edge_position = find_edge_by_colors(
        cube,
        pair_data["edge_colors"],
    )

    corner_stickers = None
    edge_stickers = None

    if corner_position is not None:
        corner_stickers = corners[corner_position]

    if edge_position is not None:
        edge_stickers = edges[edge_position]

    return {
        "pair_name": pair_name,
        "corner_colors": pair_data["corner_colors"],
        "edge_colors": pair_data["edge_colors"],
        "corner_position": corner_position,
        "edge_position": edge_position,
        "corner_target": pair_data["corner_target"],
        "edge_target": pair_data["edge_target"],
        "corner_stickers": corner_stickers,
        "edge_stickers": edge_stickers,
        "corner_target_stickers": pair_data["corner_target_stickers"],
        "edge_target_stickers": pair_data["edge_target_stickers"],
    }


def find_all_f2l_pairs(cube):
    """
    Find all four F2L pairs.

    Returns:
        Dictionary containing the status of all F2L pairs.
    """
    all_pairs = {}

    for pair_name in F2L_PAIRS:
        all_pairs[pair_name] = find_f2l_pair(cube, pair_name)

    return all_pairs


def is_f2l_pair_solved(cube, pair_name):
    """
    Check whether one F2L pair is solved in its correct slot.

    Important:
        For now this checks only position and exact sticker order.
        We may refine this later if orientation details need adjustment.
    """
    pair = find_f2l_pair(cube, pair_name)

    corner_position_correct = pair["corner_position"] == pair["corner_target"]
    edge_position_correct = pair["edge_position"] == pair["edge_target"]

    if pair["corner_stickers"] is None or pair["edge_stickers"] is None:
        return False

    corner_orientation_correct = pair["corner_stickers"] == pair["corner_target_stickers"]
    edge_orientation_correct = pair["edge_stickers"] == pair["edge_target_stickers"]

    return (
        corner_position_correct
        and edge_position_correct   
        and corner_orientation_correct
        and edge_orientation_correct
    )


def get_f2l_status(cube):
    """
    Return detailed solved/unsolved status for all F2L pairs.
    """
    status = {}

    for pair_name in F2L_PAIRS:
        pair = find_f2l_pair(cube, pair_name)

        status[pair_name] = {
            **pair,
            "corner_position_correct": pair["corner_position"] == pair["corner_target"],
            "edge_position_correct": pair["edge_position"] == pair["edge_target"],
            "solved": is_f2l_pair_solved(cube, pair_name),
        }

    return status

def get_f2l_pair_case(cube, pair_name):
    """
    Classify the current case of one F2L pair.

    This function does not solve anything yet.
    It only describes where the corner and edge are located.

    Args:
        cube:
            RubiksCube object.

        pair_name:
            One of:
                - Green-Red
                - Red-Blue
                - Blue-Orange
                - Orange-Green

    Returns:
        Dictionary describing the pair case.
    """
    pair = find_f2l_pair(cube, pair_name)

    corner_position = pair["corner_position"]
    edge_position = pair["edge_position"]

    corner_in_top = corner_position in TOP_CORNER_POSITIONS
    corner_in_bottom = corner_position in BOTTOM_CORNER_POSITIONS

    edge_in_top = edge_position in TOP_EDGE_POSITIONS
    edge_in_middle = edge_position in MIDDLE_EDGE_POSITIONS
    edge_in_bottom = edge_position in BOTTOM_EDGE_POSITIONS

    corner_in_target_slot = corner_position == pair["corner_target"]
    edge_in_target_slot = edge_position == pair["edge_target"]

    solved = is_f2l_pair_solved(cube, pair_name)

    corner_orientation_correct = (
        pair["corner_stickers"] == pair["corner_target_stickers"]
    )

    edge_orientation_correct = (
        pair["edge_stickers"] == pair["edge_target_stickers"]
    )

    if solved:
        case_type = "solved"
    elif (
        corner_in_target_slot
        and edge_in_target_slot
        and edge_orientation_correct
        and not corner_orientation_correct
    ):
        case_type = "inserted_but_corner_twisted"
    elif corner_in_top and edge_in_top:
        case_type = "corner_top_edge_top"
    elif corner_in_top and edge_in_middle:
        case_type = "corner_top_edge_middle"
    elif corner_in_top and edge_in_bottom:
        case_type = "corner_top_edge_bottom"
    elif corner_in_bottom and edge_in_top:
        case_type = "corner_bottom_edge_top"
    elif corner_in_bottom and edge_in_middle:
        case_type = "corner_bottom_edge_middle"
    elif corner_in_bottom and edge_in_bottom:
        case_type = "corner_bottom_edge_bottom"
    else:
        case_type = "unknown"

    return {
        **pair,
        "corner_in_top": corner_in_top,
        "corner_in_bottom": corner_in_bottom,
        "edge_in_top": edge_in_top,
        "edge_in_middle": edge_in_middle,
        "edge_in_bottom": edge_in_bottom,
        "corner_in_target_slot": corner_in_target_slot,
        "edge_in_target_slot": edge_in_target_slot,
        "corner_orientation_correct": corner_orientation_correct,
        "edge_orientation_correct": edge_orientation_correct,
        "solved": solved,
        "case_type": case_type,
        
    }

def print_f2l_pair_case(cube, pair_name):
    """
    Print the classified case of one F2L pair.
    """
    pair_case = get_f2l_pair_case(cube, pair_name)

    print(f"F2L Pair Case: {pair_name}")
    print("-------------------------")
    print(f"Case type:              {pair_case['case_type']}")
    print(f"Corner position:        {pair_case['corner_position']}")
    print(f"Corner target:          {pair_case['corner_target']}")
    print(f"Corner stickers:        {pair_case['corner_stickers']}")
    print(f"Corner target stickers: {pair_case['corner_target_stickers']}")
    print(f"Corner in top?          {pair_case['corner_in_top']}")
    print(f"Corner in bottom?       {pair_case['corner_in_bottom']}")
    print(f"Corner in target slot?  {pair_case['corner_in_target_slot']}")
    print(f"Corner orientation ok?  {pair_case['corner_orientation_correct']}")
    print()
    print(f"Edge position:          {pair_case['edge_position']}")
    print(f"Edge target:            {pair_case['edge_target']}")
    print(f"Edge stickers:          {pair_case['edge_stickers']}")
    print(f"Edge target stickers:   {pair_case['edge_target_stickers']}")
    print(f"Edge in top?            {pair_case['edge_in_top']}")
    print(f"Edge in middle?         {pair_case['edge_in_middle']}")
    print(f"Edge in bottom?         {pair_case['edge_in_bottom']}")
    print(f"Edge in target slot?    {pair_case['edge_in_target_slot']}")
    print(f"Edge orientation ok?    {pair_case['edge_orientation_correct']}")
    print()
    print(f"Solved?                 {pair_case['solved']}")


def print_f2l_status(cube):
    """
    Print readable F2L pair status.
    """
    status = get_f2l_status(cube)

    print("F2L Status")
    print("----------")

    for pair_name, pair_status in status.items():
        print(f"{pair_name} pair:")
        print(f"  Corner colors:           {pair_status['corner_colors']}")
        print(f"  Edge colors:             {pair_status['edge_colors']}")
        print(f"  Current corner position: {pair_status['corner_position']}")
        print(f"  Target corner position:  {pair_status['corner_target']}")
        print(f"  Current corner stickers: {pair_status['corner_stickers']}")
        print(f"  Current edge position:   {pair_status['edge_position']}")
        print(f"  Target edge position:    {pair_status['edge_target']}")
        print(f"  Current edge stickers:   {pair_status['edge_stickers']}")
        print(f"  Corner position correct? {pair_status['corner_position_correct']}")
        print(f"  Edge position correct?   {pair_status['edge_position_correct']}")
        print(f"  Solved?                  {pair_status['solved']}")
        print(f"  Target corner stickers:  {pair_status['corner_target_stickers']}")
        print(f"  Target edge stickers:    {pair_status['edge_target_stickers']}")
        print()


def is_f2l_solved(cube):
    """
    Return True if all four F2L pairs are solved.
    """
    for pair_name in F2L_PAIRS:
        if is_f2l_pair_solved(cube, pair_name) is not True:
            return False

    return True

GREEN_RED_CORNER_BOTTOM_EXTRACTION_MOVES = {
    "DFR": ["R", "U", "R'"],
    "DRB": ["R'", "U'", "R"],
    "DBL": ["L", "U", "L'"],
    "DLF": ["L'", "U'", "L"],
}

GREEN_RED_EDGE_MIDDLE_EXTRACTION_MOVES = {
    "FR": ["R", "U", "R'"],
    "BR": ["R'", "U", "R"],
    "BL": ["L", "U'", "L'"],
    "FL": ["L'", "U'", "L"],
}


def prepare_green_red_pair(cube):
    """
    Normalize the Green-Red F2L pair.

    Current goal:
        Not to fully solve F2L yet.

    Strategy:
        1. If Green-Red pair is already solved, do nothing.
        2. If Green-Red corner is in bottom layer, extract it to top.
        3. If Green-Red edge is in middle layer, extract it to top.
        4. If both corner and edge are in top layer, stop and report.

    Later:
        Once both pieces are in the top layer, we will add insertion logic.
    """
    pair_case = get_f2l_pair_case(cube, "Green-Red")

    print("[F2L Solver] Preparing Green-Red pair...")
    print(f"[F2L Solver] Case type: {pair_case['case_type']}")
    print(f"[F2L Solver] Corner position: {pair_case['corner_position']}")
    print(f"[F2L Solver] Corner stickers: {pair_case['corner_stickers']}")
    print(f"[F2L Solver] Edge position: {pair_case['edge_position']}")
    print(f"[F2L Solver] Edge stickers: {pair_case['edge_stickers']}")

    if pair_case["solved"] is True:
        print("[F2L Solver] Green-Red pair is already solved.")
        return []

    # 1) If the corner is in the bottom layer, extract it to top.
    if (
        pair_case["corner_in_bottom"] is True
        and pair_case["corner_position"] in GREEN_RED_CORNER_BOTTOM_EXTRACTION_MOVES
    ):
        moves = GREEN_RED_CORNER_BOTTOM_EXTRACTION_MOVES[pair_case["corner_position"]]

        print("[F2L Solver] Green-Red corner is in bottom layer.")
        print("[F2L Solver] Extracting corner to top layer.")
        print(f"[F2L Solver] Applying moves: {moves}")

        cube.apply_algorithm(moves)

        return moves

    # 2) If the edge is in the middle layer, extract it to top.
    if (
        pair_case["edge_in_middle"] is True
        and pair_case["edge_position"] in GREEN_RED_EDGE_MIDDLE_EXTRACTION_MOVES
    ):
        moves = GREEN_RED_EDGE_MIDDLE_EXTRACTION_MOVES[pair_case["edge_position"]]

        print("[F2L Solver] Green-Red edge is in middle layer.")
        print("[F2L Solver] Extracting edge to top layer.")
        print(f"[F2L Solver] Applying moves: {moves}")

        cube.apply_algorithm(moves)

        return moves

    # 3) If both are already in top layer, we are ready for insertion logic.
    if (
        pair_case["corner_in_top"] is True
        and pair_case["edge_in_top"] is True
    ):
        print("[F2L Solver] Green-Red corner and edge are both in top layer.")
        print("[F2L Solver] Insertion logic is not implemented yet.")
        return []

    print("[F2L Solver] No normalization algorithm implemented for this Green-Red case yet.")
    return []


def normalize_green_red_pair(cube, max_attempts=4):
    """
    Normalize the Green-Red F2L pair.

    Goal:
        Move the Green-Red corner and edge into the top layer if possible.

    Safety:
        If the same case appears again, stop early.
        This prevents repeated loops such as:
            corner_top_edge_middle -> corner_bottom_edge_top -> corner_top_edge_middle
    """
    full_moves = []
    seen_cases = set()

    for attempt in range(max_attempts):
        pair_case = get_f2l_pair_case(cube, "Green-Red")

        case_signature = (
            pair_case["case_type"],
            pair_case["corner_position"],
            tuple(pair_case["corner_stickers"]),
            pair_case["edge_position"],
            tuple(pair_case["edge_stickers"]),
        )

        print(f"[F2L Solver] Normalize attempt {attempt + 1}")
        print(f"[F2L Solver] Current case type: {pair_case['case_type']}")
        print(f"[F2L Solver] Corner position: {pair_case['corner_position']}")
        print(f"[F2L Solver] Edge position: {pair_case['edge_position']}")

        if pair_case["solved"] is True:
            print("[F2L Solver] Green-Red pair is already solved.")
            return full_moves

        if (
            pair_case["corner_in_top"] is True
            and pair_case["edge_in_top"] is True
        ):
            print("[F2L Solver] Green-Red pair is normalized: both pieces are in top layer.")
            return full_moves

        if case_signature in seen_cases:
            print("[F2L Solver] Repeated Green-Red normalization case detected.")
            print("[F2L Solver] Stopping normalization to avoid an infinite loop.")
            return full_moves

        seen_cases.add(case_signature)

        moves = prepare_green_red_pair(cube)

        if moves == []:
            print("[F2L Solver] No more normalization progress.")
            return full_moves

        full_moves.extend(moves)

    print("[F2L Solver] Max normalization attempts reached.")
    return full_moves

GREEN_RED_F2L_CASES = [
    {
        "name": "green_red_case_01",
        "case_type": "corner_top_edge_top",
        "corner_position": "UFR",
        "corner_stickers": ["W", "R", "G"],
        "edge_position": "UR",
        "edge_stickers": ["G", "R"],
        "algorithm": ["R", "U'", "R", "U", "R'", "U'", "R2"],
    },
    {
        "name": "green_red_case_02",
        "case_type": "corner_top_edge_top",
        "corner_position": "ULF",
        "corner_stickers": ["R", "G", "W"],
        "edge_position": "UL",
        "edge_stickers": ["R", "G"],
        "algorithm": ["U", "F'", "U2", "F"],
    },
    {
        "name": "green_red_case_03",
        "case_type": "corner_top_edge_top",
        "corner_position": "UBL",
        "corner_stickers": ["W", "R", "G"],
        "edge_position": "UF",
        "edge_stickers": ["R", "G"],
        "algorithm": ["F'", "L", "F'", "L'", "F2"],
    },
    {
        "name": "green_red_case_04",
        "case_type": "corner_top_edge_top",
        "corner_position": "ULF",
        "corner_stickers": ["G", "W", "R"],
        "edge_position": "UR",
        "edge_stickers": ["G", "R"],
        "algorithm": ["R", "F", "R'", "F'", "R'"],
    },
    {
        "name": "green_red_case_05",
        "case_type": "corner_top_edge_top",
        "corner_position": "UFR",
        "corner_stickers": ["R", "G", "W"],
        "edge_position": "UF",
        "edge_stickers": ["G", "R"],
        "algorithm": ["R'", "U2", "R2", "U", "R'"],
    },
    {
        "name": "green_red_case_06",
        "case_type": "corner_top_edge_top",
        "corner_position": "UBL",
        "corner_stickers": ["W", "R", "G"],
        "edge_position": "UF",
        "edge_stickers": ["G", "R"],
        "algorithm": ["R", "F", "U2", "F'", "U'", "R'"],
    },
    {
        "name": "green_red_case_07",
        "case_type": "corner_top_edge_top",
        "corner_position": "URB",
        "corner_stickers": ["W", "R", "G"],
        "edge_position": "UB",
        "edge_stickers": ["R", "G"],
        "algorithm": ["R2", "F2", "U2", "F'", "U2", "R2", "F2"],
    },
    {
        "name": "green_red_case_08",
        "case_type": "corner_top_edge_top",
        "corner_position": "URB",
        "corner_stickers": ["G", "W", "R"],
        "edge_position": "UB",
        "edge_stickers": ["G", "R"],
        "algorithm": ["U'", "R", "U2", "R'"],
    },
    {
        "name": "green_red_case_09",
        "case_type": "corner_top_edge_top",
        "corner_position": "UBL",
        "corner_stickers": ["R", "G", "W"],
        "edge_position": "UF",
        "edge_stickers": ["G", "R"],
        "algorithm": ["U2", "R", "U", "R'"],
    },
    {
        "name": "green_red_case_10",
        "case_type": "corner_top_edge_top",
        "corner_position": "UBL",
        "corner_stickers": ["R", "G", "W"],
        "edge_position": "UF",
        "edge_stickers": ["R", "G"],
        "algorithm": ["F", "R2", "U2", "F'", "U2", "R2"],
    },
    {
        "name": "green_red_case_11",
        "case_type": "corner_top_edge_top",
        "corner_position": "URB",
        "corner_stickers": ["W", "R", "G"],
        "edge_position": "UF",
        "edge_stickers": ["G", "R"],
        "algorithm": ["F", "U", "F'", "R", "U'", "R'"],
    },
    {
        "name": "green_red_case_12",
        "case_type": "corner_top_edge_top",
        "corner_position": "ULF",
        "corner_stickers": ["R", "G", "W"],
        "edge_position": "UF",
        "edge_stickers": ["R", "G"],
        "algorithm": ["U", "L", "U'", "L'", "F'", "U'", "F"],
    },
    {
        "name": "green_red_case_13",
        "case_type": "corner_top_edge_top",
        "corner_position": "ULF",
        "corner_stickers": ["G", "W", "R"],
        "edge_position": "UF",
        "edge_stickers": ["G", "R"],
        "algorithm": ["R", "U'", "R'"],
    },

    {
        "name": "green_red_case_14",
        "case_type": "corner_top_edge_top",
        "corner_position": "UFR",
        "corner_stickers": ["G", "W", "R"],
        "edge_position": "UF",
        "edge_stickers": ["G", "R"],
        "algorithm": ["R", "F", "U", "F'", "U'", "R'"],
    },

    {
        "name": "green_red_case_15",
        "case_type": "corner_top_edge_top",
        "corner_position": "URB",
        "corner_stickers": ["W", "R", "G"],
        "edge_position": "UF",
        "edge_stickers": ["R", "G"],
        "algorithm": ["F'", "U'", "L", "F'", "L'", "F2"],
    },

    {
        "name": "green_red_case_16",
        "case_type": "corner_top_edge_top",
        "corner_position": "ULF",
        "corner_stickers": ["R", "G", "W"],
        "edge_position": "UF",
        "edge_stickers": ["G", "R"],
        "algorithm": ["U2", "R2", "U", "R", "U'", "R2"],
    },

    {
        "name": "green_red_case_17",
        "case_type": "corner_top_edge_top",
        "corner_position": "URB",
        "corner_stickers": ["G", "W", "R"],
        "edge_position": "UF",
        "edge_stickers": ["G", "R"],
        "algorithm": ["U", "L2", "F2", "L'", "F2", "L'"],
    },

    {
        "name": "green_red_case_18",
        "case_type": "corner_top_edge_top",
        "corner_position": "UBL",
        "corner_stickers": ["G", "W", "R"],
        "edge_position": "UF",
        "edge_stickers": ["G", "R"],
        "algorithm": ["U'", "R", "F", "R'", "F'", "R'"],
    },

    {
        "name": "green_red_case_19",
        "case_type": "corner_top_edge_top",
        "corner_position": "UFR",
        "corner_stickers": ['R', 'G', 'W'],
        "edge_position": "UF",
        "edge_stickers": ['R', 'G'],
        "algorithm": ["U'", "F'", 'U', 'F'],
    },

    {
        "name": "green_red_case_20",
        "case_type": "corner_top_edge_top",
        "corner_position": "URB",
        "corner_stickers": ["R", "G", "W"],
        "edge_position": "UF",
        "edge_stickers": ["R", "G"],
        "algorithm": ["R", "F", "R", "F'", "R'"],
    },

    {
        "name": "green_red_case_21",
        "case_type": "corner_top_edge_top",
        "corner_position": "URB",
        "corner_stickers": ["G", "W", "R"],
        "edge_position": "UF",
        "edge_stickers": ["R", "G"],
        "algorithm": ["U", "F'", "U'", "F"],
    },

    {
        "name": "green_red_case_22",
        "case_type": "corner_top_edge_top",
        "corner_position": "ULF",
        "corner_stickers": ["G", "W", "R"],
        "edge_position": "UF",
        "edge_stickers": ["R", "G"],
        "algorithm": ["U'", "F", "U2", "F2", "U'", "F"],
    },

    {
        "name": "green_red_case_23",
        "case_type": "corner_top_edge_top",
        "corner_position": "UFR",
        "corner_stickers": ["W", "R", "G"],
        "edge_position": "UF",
        "edge_stickers": ["R", "G"],
        "algorithm": ["U", "L'", "U2", "L", "F'", "U'", "F"],
    },

    {
        "name": "green_red_case_24",
        "case_type": "corner_top_edge_top",
        "corner_position": "UFR",
        "corner_stickers": ["G", "W", "R"],
        "edge_position": "UR",
        "edge_stickers": ["G", "R"],
        "algorithm": ["U", "R", "U'", "R'"],
    },   

    {
        "name": "green_red_case_25",
        "case_type": "corner_top_edge_top",
        "corner_position": "ULF",
        "corner_stickers": ["R", "G", "W"],
        "edge_position": "UL",
        "edge_stickers": ["G", "R"],
        "algorithm": ["U'", "R'", "U2", "R2", "U", "R'"],
    },

    {
        "name": "green_red_case_26",
        "case_type": "corner_top_edge_top",
        "corner_position": "UFR",
        "corner_stickers": ["W", "R", "G"],
        "edge_position": "UF",
        "edge_stickers": ["G", "R"],
        "algorithm": ["R", "U'", "L", "F'", "L'", "F", "R'"],
    },

    {
        "name": "green_red_case_27",
        "case_type": "corner_top_edge_top",
        "corner_position": "UBL",
        "corner_stickers": ["G", "W", "R"],
        "edge_position": "UB",
        "edge_stickers": ["G", "R"],
        "algorithm": ["U'", "R", "F", "R'", "U2", "F'", "R'"],
    },

    {
        "name": "green_red_case_28",
        "case_type": "corner_top_edge_top",
        "corner_position": "ULF",
        "corner_stickers": ["W", "R", "G"],
        "edge_position": "UB",
        "edge_stickers": ["R", "G"],
        "algorithm": ["F'", "L2", "U2", "F", "U2", "L2"],
    },

    {
        "name": "green_red_case_29",
        "case_type": "corner_top_edge_top",
        "corner_position": "UBL",
        "corner_stickers": ["G", "W", "R"],
        "edge_position": "UF",
        "edge_stickers": ["R", "G"],
        "algorithm": ["F2", "U'", "F", "U", "F2"],
    },

]


def does_green_red_case_match(pair_case, case_definition):
    """
    Check whether the current Green-Red F2L case matches
    a known CFOP-style F2L case definition.
    """
    return (
        pair_case["case_type"] == case_definition["case_type"]
        and pair_case["corner_position"] == case_definition["corner_position"]
        and pair_case["corner_stickers"] == case_definition["corner_stickers"]
        and pair_case["edge_position"] == case_definition["edge_position"]
        and pair_case["edge_stickers"] == case_definition["edge_stickers"]
    )


def find_known_green_red_f2l_case(pair_case):
    """
    Return the matching known Green-Red F2L case if one exists.
    Otherwise return None.
    """
    for case_definition in GREEN_RED_F2L_CASES:
        if does_green_red_case_match(pair_case, case_definition):
            return case_definition

    return None


def apply_known_green_red_f2l_case(cube, pair_case):
    """
    Apply a known Green-Red F2L case algorithm if the current case
    exists in the Green-Red F2L case table.
    """
    case_definition = find_known_green_red_f2l_case(pair_case)

    if case_definition is None:
        return []

    moves = case_definition["algorithm"]

    print("[F2L Solver] Supported Green-Red F2L case found.")
    print(f"[F2L Solver] Case name: {case_definition['name']}")
    print(f"[F2L Solver] Applying moves: {moves}")

    cube.apply_algorithm(moves)

    return moves


def insert_green_red_pair(cube):
    """
    Try to insert the normalized Green-Red F2L pair into the FR slot.

    Target:
        Corner -> DFR
        Edge   -> FR

    CFOP approach:
        1. Detect the current Green-Red F2L case.
        2. Check the known F2L case table.
        3. If found, apply the algorithm.
        4. If not found, try U-layer alignment once.
        5. If still not found, stop safely.

    This prevents applying the wrong algorithm to the wrong orientation.
    """
    pair_case = get_f2l_pair_case(cube, "Green-Red")

    print("[F2L Solver] Trying to insert Green-Red pair...")
    print(f"[F2L Solver] Case type: {pair_case['case_type']}")
    print(f"[F2L Solver] Corner position: {pair_case['corner_position']}")
    print(f"[F2L Solver] Corner stickers: {pair_case['corner_stickers']}")
    print(f"[F2L Solver] Edge position: {pair_case['edge_position']}")
    print(f"[F2L Solver] Edge stickers: {pair_case['edge_stickers']}")

    if pair_case["solved"] is True:
        print("[F2L Solver] Green-Red pair is already solved.")
        return []

    if pair_case["case_type"] == "inserted_but_corner_twisted":
        return extract_inserted_green_red_pair(cube)

    total_moves = []

    known_case_moves = apply_known_green_red_f2l_case(cube, pair_case)

    if known_case_moves:
        total_moves.extend(known_case_moves)
        return total_moves

    if (
        pair_case["corner_in_top"] is True
        and pair_case["edge_in_top"] is True
    ):
        align_moves = align_green_red_top_pair_for_insertion(cube)

        if align_moves:
            total_moves.extend(align_moves)

            aligned_pair_case = get_f2l_pair_case(cube, "Green-Red")
            known_case_moves = apply_known_green_red_f2l_case(
                cube,
                aligned_pair_case,
            )

            if known_case_moves:
                total_moves.extend(known_case_moves)
                return total_moves

        print("[F2L Solver] Could not align Green-Red pair for insertion.")
        return total_moves

    print("[F2L Solver] No insertion algorithm implemented for this Green-Red case yet.")
    return total_moves

def align_green_red_top_pair_for_insertion(cube):
    """
    Try to align the Green-Red pair on the U layer before insertion.

    Important:
        We do not only check positions.
        We also check sticker orientation.

    Supported target insertion case:
        corner_position == UFR
        corner_stickers == ["W", "R", "G"]
        edge_position == UR
        edge_stickers == ["G", "R"]
    """
    candidate_u_moves = [
        [],
        ["U"],
        ["U2"],
        ["U'"],
    ]

    inverse_moves = {
        (): [],
        ("U",): ["U'"],
        ("U2",): ["U2"],
        ("U'",): ["U"],
    }

    for moves in candidate_u_moves:
        if moves:
            cube.apply_algorithm(moves)

        pair_case = get_f2l_pair_case(cube, "Green-Red")

        if (
            pair_case["case_type"] == "corner_top_edge_top"
            and pair_case["corner_position"] == "UFR"
            and pair_case["corner_stickers"] == ["W", "R", "G"]
            and pair_case["edge_position"] == "UR"
            and pair_case["edge_stickers"] == ["G", "R"]
        ):
            print("[F2L Solver] Found U-layer alignment for Green-Red pair.")
            print(f"[F2L Solver] Alignment moves: {moves}")

            return moves

        undo = inverse_moves[tuple(moves)]

        if undo:
            cube.apply_algorithm(undo)

    print("[F2L Solver] No U-layer alignment found for current Green-Red pair.")
    return []

def extract_inserted_green_red_pair(cube):
    """
    Extract the Green-Red F2L pair when it is inserted but the corner is twisted.

    Supported case:
        - case_type: inserted_but_corner_twisted
        - corner_position: DFR
        - edge_position: FR

    Goal:
        Move the Green-Red pair out of the FR slot so it can be normalized again.
    """
    pair_case = get_f2l_pair_case(cube, "Green-Red")

    print("[F2L Solver] Checking inserted Green-Red pair extraction...")
    print(f"[F2L Solver] Case type: {pair_case['case_type']}")
    print(f"[F2L Solver] Corner position: {pair_case['corner_position']}")
    print(f"[F2L Solver] Corner stickers: {pair_case['corner_stickers']}")
    print(f"[F2L Solver] Edge position: {pair_case['edge_position']}")
    print(f"[F2L Solver] Edge stickers: {pair_case['edge_stickers']}")

    if pair_case["case_type"] == "inserted_but_corner_twisted":
        moves = ["R", "U", "R'"]

        print("[F2L Solver] Inserted but twisted Green-Red pair found.")
        print("[F2L Solver] Extracting pair from FR slot.")
        print(f"[F2L Solver] Applying moves: {moves}")

        cube.apply_algorithm(moves)

        return moves

    print("[F2L Solver] No inserted twisted Green-Red pair found.")
    return []