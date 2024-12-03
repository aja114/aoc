DIR = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


def is_symbol(c: str):
    return c != "." and not c.isalnum()


def is_gear(c: str):
    return c == "*"


def find_replace_num(mat: list[list[str]], pos: (int, int)) -> int | None:
    x, y = pos
    if x >= len(mat) or x < 0 or y >= len(mat[0]) or y < 0 or not mat[x][y].isdigit():
        return None
    s, e = y-1, y+1
    while s >= 0 and mat[x][s].isdigit():
        s -= 1
    while e < len(mat[0]) and mat[x][e].isdigit():
        e += 1
    s += 1
    num = int("".join(mat[x][s:e]))
    mat[x][s:e] = ["."]*(e-s)
    return num


def find_adj(mat: list[list[str]], pos: (int, int)):
    nums = []
    x, y = pos
    for dir_x, dir_y in DIR:
        num = find_replace_num(mat, (x+dir_x, y+dir_y))
        if num:
            nums.append(num)
    return nums


def part1(mat: list[list[str]]) -> int:
    s = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if is_symbol(mat[i][j]):
                s += sum(find_adj(mat, (i, j)))
    return s


def part2(mat: list[list[str]]) -> int:
    s = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if is_gear(mat[i][j]):
                nums = find_adj(mat, (i, j))
                if len(nums) == 2:
                    s += nums[0] * nums[1]
    return s


def get_input(file: str) -> list[list[str]]:
    matrix = []
    with open(file, "r") as f:
        for line in f.readlines():
            matrix.append(list(line.strip()))
    return matrix


if __name__ == "__main__":
    print(part1(get_input("day3-input.txt")))
    print(part2(get_input("day3-input.txt")))
