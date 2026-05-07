from src.cube import RubiksCube
from src.scrambler import generate_scramble, inverse_algorithm


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


if __name__ == "__main__":
    main()