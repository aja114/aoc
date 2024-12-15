from collections import defaultdict
from functools import reduce


def get_input(file: str) -> list[tuple[int, list[dict[str, int]]]]:
    inp = []
    with open(file, "r") as f:
        for line in f.readlines():
            id_, s = line.split(":")
            counters = []
            for colors in s.split(";"):
                counter = defaultdict(int)
                for color in colors.split(","):
                    num, c = color.strip().split(" ")
                    counter[c] = int(num)
                counters.append(counter)
            inp.append((int(id_[5:]), counters))
    return inp


def part1(file: str) -> int:
    limit = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    inp_list = get_input(file)
    possible_games = {}
    for id_, colors in inp_list:
        possible_games[id_] = True
        for color in colors:
            for k, v in limit.items():
                if color[k] > v:
                    possible_games[id_] = False
                    break
            else:
                continue
            break
    return sum(x for x in possible_games if possible_games[x])


def part2(file: str):
    inp_list = get_input(file)
    s = 0
    for id_, colors in inp_list:
        limits = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        for color in colors:
            for k, v in limits.items():
                if color[k] > v:
                    limits[k] = color[k]
        s += reduce((lambda x, y: x * y), limits.values())
    return s


if __name__ == '__main__':
    print(part1("inputs/day2-input.txt"))
    print(part2("inputs/day2-input.txt"))
