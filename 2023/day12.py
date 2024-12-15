def get_input(file: str) -> list[tuple[list[str]], tuple[int, ...]]:
    springs = []
    conditions = []
    with open(file, "r") as f:
        for line in f.readlines():
            spring, condition, *_ = line.strip().split(" ")
            springs.append(list(spring))
            conditions.append(tuple([int(x) for x in condition.split(",")]))
    return list(zip(springs, conditions))


def find_spring_comb(
    springs: list[str], target_condition: tuple[int, ...], memo: dict
) -> int:
    current_condition = calc_condition(springs)
    current_condition_len = len(current_condition)
    if "?" not in springs:
        return int(target_condition == current_condition)

    if current_condition_len > 0:
        if current_condition_len > len(target_condition):
            return 0
        if current_condition[:current_condition_len-1] != target_condition[:current_condition_len-1]:
            return 0
        if current_condition[current_condition_len-1] > target_condition[current_condition_len-1]:
            return 0

    match_unknown = springs.index("?")
    matched = springs[:match_unknown]
    to_match = springs[match_unknown+1:]
    key = tuple(springs[match_unknown-1:]), current_condition

    if key in memo:
        return memo[key]

    r = find_spring_comb(
        matched + ["."] + to_match,
        target_condition,
        memo
    ) + find_spring_comb(
        matched + ["#"] + to_match,
        target_condition,
        memo
    )
    memo[key] = r
    return r


def calc_condition(springs: list[str]):
    condition = []
    func = False
    curr_count = 0
    for s in springs:
        if s == "?":
            break
        if s == "." and func is True:
            condition.append(curr_count)
            curr_count = 0
            func = False
        if s == "#":
            func = True
            curr_count += 1
    if func is True:
        condition.append(curr_count)
    return tuple(condition)


def part1(spring_inp: list[tuple[list[str]], tuple[int, ...]]) -> int:
    s = 0
    for i, (springs, target_condition) in enumerate(spring_inp):
        s += find_spring_comb(springs, target_condition, {})
    return s


def part2(spring_inp: list[tuple[list[str]], tuple[int, ...]]) -> int:
    s = 0
    for i, (springs, target_condition) in enumerate(spring_inp):
        unfolded_springs = ((springs + ["?"]) * 5)[:-1]
        unfolded_target_condition = target_condition * 5
        s += find_spring_comb(unfolded_springs, unfolded_target_condition, {})
    return s


if __name__ == "__main__":
    inp = get_input("inputs/day12-input.txt")
    print(part1(inp))
    print(part2(inp))
