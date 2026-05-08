"""
Human-style Rubik's Cube solver.

This module coordinates the CFOP-style solving process:

1. Cross
2. F2L
3. OLL
4. PLL
"""

from src.solvers.cross_solver import solve_cross
from src.solvers.f2l_solver import solve_f2l
from src.solvers.oll_solver import solve_oll
from src.solvers.pll_solver import solve_pll


def solve_human_style(cube):
    """
    Solve the cube using a human-style CFOP pipeline.

    For now, each stage is only a placeholder.

    Parameters:
        cube: RubiksCube object

    Returns:
        A list of all moves produced by the human-style solver.
    """
    full_solution = []

    print("Starting human-style CFOP solver...")
    print("-----------------------------------")

    cross_moves = solve_cross(cube)
    full_solution.extend(cross_moves)

    f2l_moves = solve_f2l(cube)
    full_solution.extend(f2l_moves)

    oll_moves = solve_oll(cube)
    full_solution.extend(oll_moves)

    pll_moves = solve_pll(cube)
    full_solution.extend(pll_moves)

    print("-----------------------------------")
    print("Human-style solver finished.")

    return full_solution