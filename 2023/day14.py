import copy
from collections import Counter


def get_input(file: str) -> list[list[str]]:
    with open(file, "r") as f:
        inp = [list(x.strip()) for x in f.readlines()]
    return inp


def roll_rocks(subrow: list[str]) -> list[str]:
    c = Counter(subrow)
    r = ["O"] * c["O"] + ["."] * c["."]
    return r
    
    
def roll_all_rocks(platform: list[list[str]]) -> None:
    for row in platform:
        i = 0
        top = 0
        while i < len(row):
            if row[i] != "#":
                i += 1
                continue
            row[top:i] = roll_rocks(row[top:i])
            i += 1
            top = i
        if top < i:
            row[top:i] = roll_rocks(row[top:i])


def tilt_north(platform: list[list[str]]) -> list[list[str]]:
    platform = [list(x) for x in zip(*platform)]
    roll_all_rocks(platform)
    return list(zip(*platform))


def tilt_cycle(platform: list[list[str]]) -> list[list[str]]:
    platform = copy.deepcopy(platform)
    # north
    platform = [list(x) for x in zip(*platform)]
    roll_all_rocks(platform)
    
    # west
    platform = [list(x) for x in zip(*platform)]
    roll_all_rocks(platform)

    # south
    platform = [list(row)[::-1] for row in zip(*platform)]
    roll_all_rocks(platform)
    platform = [list(row) for row in zip(*[x[::-1] for x in platform])]
    
    # east
    platform = [row[::-1] for row in platform]
    roll_all_rocks(platform)
    platform = [row[::-1] for row in platform]
    return platform


def tilt_west(platform: list[list[str]]) -> list[list[str]]:
    platform = copy.deepcopy(platform)
    roll_all_rocks(platform)
    return platform


def count_load(platform: list[list[str]]) -> int:
    s = 0
    for i, row in enumerate(platform):
        c = Counter(row)
        s += c["O"] * (len(platform)-i)
    return s


def pprint_plat(platform: list[list[str]]) -> None:
    for row in platform:
        print("".join(x for x in row))
    print()


def part1(file: str) -> int:
    platform = get_input(file)
    tilted_platform = tilt_north(platform)
    return count_load(tilted_platform)


def hash_plat(platform: list[list[str]]) -> str:
    import hashlib
    platform_str = "".join("".join(r) for r in platform)
    hash_object = hashlib.md5(platform_str.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig
    

def part2(file: str) -> int:
    platform = get_input(file)
    hash_list = []
    while True:
        platform = tilt_cycle(platform)
        hashed_plat = hash_plat(platform)
        if hashed_plat in hash_list:
            cycle_start = hash_list.index(hashed_plat)
            cycle_len = len(hash_list) - cycle_start
            cycle_pos = (1_000_000_000 - cycle_start) % cycle_len
            break
        hash_list.append(hashed_plat)
    
    platform = get_input(file)
    for _ in range(cycle_start+cycle_pos):
        platform = tilt_cycle(platform)
    return count_load(platform)


if __name__ == "__main__":
    print(part1("inputs/day14-input.txt"))
    print(part2("inputs/day14-input.txt"))
