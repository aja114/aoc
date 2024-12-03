def extrapolate_end(l: list[int]) -> int:
    if all(x == 0 for x in l):
        return 0
    diff = [l[i+1] - l[i] for i in range(len(l)-1)]
    target = extrapolate_end(diff)
    return target + l[-1]


def extrapolate_start(l: list[int]) -> int:
    if all(x == 0 for x in l):
        return 0
    diff = [l[i+1] - l[i] for i in range(len(l)-1)]
    target = extrapolate_start(diff)
    return l[0] - target


def part1(file: str) -> int:
    with open(file, "r") as f:
        lines = [
            [int(n) for n in l.split(" ")]
            for l in f.readlines()
        ]
    s = 0
    for l in lines:
        s += extrapolate_end(l)
    return s


def part2(file: str) -> int:
    with open(file, "r") as f:
        lines = [
            [int(n) for n in l.split(" ")]
            for l in f.readlines()
        ]
    s = 0
    for l in lines:
        s += extrapolate_start(l)
    return s


if __name__ == "__main__":
    print(part1("day9-input.txt"))
    print(part2("day9-input.txt"))
