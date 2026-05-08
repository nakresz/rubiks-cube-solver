from src.cube import RubiksCube
from src.scrambler import generate_scramble, inverse_algorithm
from src.piece_detector import (
    find_edge_by_colors,
    find_corner_by_colors,
    validate_pieces,
)


def main():
    cube = RubiksCube()

    print("Rubik's Cube Solver Demo")
    print("========================")
    print()

    print("Initial cube:")
    print("-------------")
    cube.display()

    print("Solved?")
    print(cube.is_solved())

    print()
    print("Finding pieces on solved cube:")
    print("------------------------------")
    print("White-Green edge:", find_edge_by_colors(cube, ["W", "G"]))
    print("White-Green-Red corner:", find_corner_by_colors(cube, ["W", "G", "R"]))
    print("Pieces valid?", validate_pieces(cube))

    print()
    print("Generating random scramble...")
    print("-----------------------------")

    scramble = generate_scramble(length=20)

    print("Scramble:")
    print(" ".join(scramble))

    print()
    print("Applying scramble...")
    print("--------------------")

    cube.apply_algorithm(scramble)
    cube.display()

    print("Solved after scramble?")
    print(cube.is_solved())
    print("Pieces valid after scramble?")
    print(validate_pieces(cube))

    print()
    print("Generating inverse solution...")
    print("------------------------------")

    solution = inverse_algorithm(scramble)

    print("Solution:")
    print(" ".join(solution))

    print()
    print("Applying solution...")
    print("--------------------")

    cube.apply_algorithm(solution)
    cube.display()

    print("Solved after solution?")
    print(cube.is_solved())
    print("Pieces valid after solution?")
    print(validate_pieces(cube))


if __name__ == "__main__":
    main()