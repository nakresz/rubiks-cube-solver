"""
Move definitions for the Rubik's Cube project.

This file keeps all supported moves in one place.
"""

BASIC_MOVES = ["U", "D", "R", "L", "F", "B"]

ALL_MOVES = [
    "U", "U'", "U2",
    "D", "D'", "D2",
    "R", "R'", "R2",
    "L", "L'", "L2",
    "F", "F'", "F2",
    "B", "B'", "B2",
]

INVERSE_MOVES = {
    "U": "U'",
    "U'": "U",
    "U2": "U2",

    "D": "D'",
    "D'": "D",
    "D2": "D2",

    "R": "R'",
    "R'": "R",
    "R2": "R2",

    "L": "L'",
    "L'": "L",
    "L2": "L2",

    "F": "F'",
    "F'": "F",
    "F2": "F2",

    "B": "B'",
    "B'": "B",
    "B2": "B2",
}