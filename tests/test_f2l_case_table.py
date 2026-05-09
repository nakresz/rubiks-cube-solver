from src.solvers.f2l_solver import GREEN_RED_F2L_CASES


VALID_MOVES = {
    "U", "U'", "U2",
    "D", "D'", "D2",
    "R", "R'", "R2",
    "L", "L'", "L2",
    "F", "F'", "F2",
    "B", "B'", "B2",
}


REQUIRED_CASE_KEYS = {
    "name",
    "case_type",
    "corner_position",
    "corner_stickers",
    "edge_position",
    "edge_stickers",
    "algorithm",
}


def get_case_signature(case_definition):
    """
    A case signature uniquely identifies a Green-Red F2L situation.

    We use:
        case_type
        corner_position
        corner_stickers
        edge_position
        edge_stickers

    If two case definitions have the same signature, they describe
    the same F2L case and should not both exist in the table.
    """
    return (
        case_definition["case_type"],
        case_definition["corner_position"],
        tuple(case_definition["corner_stickers"]),
        case_definition["edge_position"],
        tuple(case_definition["edge_stickers"]),
    )


def test_green_red_f2l_case_table_is_not_empty():
    assert len(GREEN_RED_F2L_CASES) > 0


def test_green_red_f2l_cases_have_required_keys():
    for case_definition in GREEN_RED_F2L_CASES:
        assert REQUIRED_CASE_KEYS.issubset(case_definition.keys())


def test_green_red_f2l_case_names_are_unique():
    case_names = [
        case_definition["name"]
        for case_definition in GREEN_RED_F2L_CASES
    ]

    assert len(case_names) == len(set(case_names))


def test_green_red_f2l_case_signatures_are_unique():
    case_signatures = [
        get_case_signature(case_definition)
        for case_definition in GREEN_RED_F2L_CASES
    ]

    assert len(case_signatures) == len(set(case_signatures))


def test_green_red_f2l_cases_have_valid_corner_stickers():
    for case_definition in GREEN_RED_F2L_CASES:
        corner_stickers = case_definition["corner_stickers"]

        assert len(corner_stickers) == 3
        assert sorted(corner_stickers) == sorted(["W", "G", "R"])


def test_green_red_f2l_cases_have_valid_edge_stickers():
    for case_definition in GREEN_RED_F2L_CASES:
        edge_stickers = case_definition["edge_stickers"]

        assert len(edge_stickers) == 2
        assert sorted(edge_stickers) == sorted(["G", "R"])


def test_green_red_f2l_cases_have_non_empty_algorithms():
    for case_definition in GREEN_RED_F2L_CASES:
        algorithm = case_definition["algorithm"]

        assert isinstance(algorithm, list)
        assert len(algorithm) > 0


def test_green_red_f2l_case_algorithms_use_valid_moves():
    for case_definition in GREEN_RED_F2L_CASES:
        algorithm = case_definition["algorithm"]

        for move in algorithm:
            assert move in VALID_MOVES