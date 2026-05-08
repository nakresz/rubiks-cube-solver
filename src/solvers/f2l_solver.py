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

    if solved:
        case_type = "solved"
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
    print()
    print(f"Edge position:          {pair_case['edge_position']}")
    print(f"Edge target:            {pair_case['edge_target']}")
    print(f"Edge stickers:          {pair_case['edge_stickers']}")
    print(f"Edge target stickers:   {pair_case['edge_target_stickers']}")
    print(f"Edge in top?            {pair_case['edge_in_top']}")
    print(f"Edge in middle?         {pair_case['edge_in_middle']}")
    print(f"Edge in bottom?         {pair_case['edge_in_bottom']}")
    print(f"Edge in target slot?    {pair_case['edge_in_target_slot']}")
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