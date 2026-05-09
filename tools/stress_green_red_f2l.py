import io
from contextlib import redirect_stdout

from src.cube import RubiksCube
from src.scrambler import generate_scramble
from src.solvers.cross_solver import solve_cross, is_white_cross_solved
from src.solvers.f2l_solver import (
    normalize_green_red_pair,
    insert_green_red_pair,
    is_f2l_pair_solved,
    get_f2l_pair_case,
)


def run_single_trial(trial_number, scramble_length=20):
    cube = RubiksCube()

    scramble = generate_scramble(length=scramble_length)
    cube.apply_algorithm(scramble)

    with redirect_stdout(io.StringIO()):
        solve_cross(cube)

    cross_solved_after_cross = is_white_cross_solved(cube)

    with redirect_stdout(io.StringIO()):
        normalize_moves = normalize_green_red_pair(cube)

    case_after_normalization = get_f2l_pair_case(cube, "Green-Red")

    with redirect_stdout(io.StringIO()):
        insertion_moves = insert_green_red_pair(cube)

    cross_solved_after_f2l = is_white_cross_solved(cube)
    green_red_solved = is_f2l_pair_solved(cube, "Green-Red")

    final_case = get_f2l_pair_case(cube, "Green-Red")

    return {
        "trial_number": trial_number,
        "scramble": scramble,
        "cross_solved_after_cross": cross_solved_after_cross,
        "cross_solved_after_f2l": cross_solved_after_f2l,
        "green_red_solved": green_red_solved,
        "normalize_moves": normalize_moves,
        "insertion_moves": insertion_moves,
        "case_after_normalization": case_after_normalization,
        "final_case": final_case,
    }


def main():
    total_trials = 100
    scramble_length = 20

    solved_count = 0
    unsupported_count = 0
    cross_broken_count = 0
    cross_failed_count = 0

    unsupported_cases = {}
    unsupported_examples = {}

    print("Green-Red F2L Stress Test")
    print("=========================")
    print()
    print(f"Total trials: {total_trials}")
    print(f"Scramble length: {scramble_length}")
    print()

    for trial_number in range(1, total_trials + 1):
        result = run_single_trial(
            trial_number=trial_number,
            scramble_length=scramble_length,
        )

        if not result["cross_solved_after_cross"]:
            cross_failed_count += 1
            print(f"[Trial {trial_number}] Cross failed after cross solver.")
            print("Scramble:")
            print(result["scramble"])
            continue

        if not result["cross_solved_after_f2l"]:
            cross_broken_count += 1
            print(f"[Trial {trial_number}] Cross was broken during F2L operation.")
            print("Scramble:")
            print(result["scramble"])
            continue

        if result["green_red_solved"]:
            solved_count += 1
        else:
            unsupported_count += 1

            case = result["final_case"]

            case_signature = (
                case["case_type"],
                case["corner_position"],
                tuple(case["corner_stickers"]),
                case["edge_position"],
                tuple(case["edge_stickers"]),
            )

            unsupported_cases[case_signature] = (
                unsupported_cases.get(case_signature, 0) + 1
            )

            if case_signature not in unsupported_examples:
                unsupported_examples[case_signature] = result["scramble"]

    print()
    print("Stress Test Summary")
    print("-------------------")
    print(f"Total trials:              {total_trials}")
    print(f"Green-Red solved:          {solved_count}")
    print(f"Green-Red unsupported:     {unsupported_count}")
    print(f"Cross failed after solver: {cross_failed_count}")
    print(f"Cross broken by F2L:       {cross_broken_count}")

    print()
    print("Success rate:")
    print(f"{solved_count}/{total_trials} = {solved_count / total_trials:.2%}")

    print()
    print("Most common unsupported cases:")
    print("------------------------------")

    sorted_cases = sorted(
        unsupported_cases.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    for index, (case_signature, count) in enumerate(sorted_cases[:10], start=1):
        (
            case_type,
            corner_position,
            corner_stickers,
            edge_position,
            edge_stickers,
        ) = case_signature

        example_scramble = unsupported_examples[case_signature]

        print()
        print(f"#{index} | Count: {count}")
        print(f"Case type:       {case_type}")
        print(f"Corner position: {corner_position}")
        print(f"Corner stickers: {list(corner_stickers)}")
        print(f"Edge position:   {edge_position}")
        print(f"Edge stickers:   {list(edge_stickers)}")
        print("Example scramble:")
        print(example_scramble)


if __name__ == "__main__":
    main()