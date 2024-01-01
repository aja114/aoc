import enum
import itertools

Inst = tuple["Dir", int, str]


class Dir(enum.Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)


DIR_MAP = {
    "U": Dir.UP,
    "D": Dir.DOWN,
    "R": Dir.RIGHT,
    "L": Dir.LEFT,
}


def get_input(file: str) -> list[Inst]:
    def parse_line(x):
        return DIR_MAP[x[0]], int(x[1]), x[2][1:-1]
    with open(file, "r") as f:
        inp = [
            parse_line(line.strip().split(" "))
            for line in f.readlines()
        ]
    return inp


def get_corrected_input(file: str) -> list[Inst]:
    def parse_line(x):
        hex_num = x[2][2:-1]
        directions = {
            "0": Dir.RIGHT,
            "1": Dir.DOWN,
            "2": Dir.LEFT,
            "3": Dir.UP,
        }
        d = directions[hex_num[-1]]
        num = int(hex_num[:-1], 16)
        return d, num, ""
    with open(file, "r") as f:
        inp = [
            parse_line(line.strip().split(" "))
            for line in f.readlines()
        ]
    return inp


def get_dim(instructions: list[Inst]):
    min_row = 0
    max_row = 0
    current_row = 0
    min_col = 0
    max_col = 0
    current_col = 0
    for inst in instructions:
        if inst[0] is Dir.UP:
            current_row -= inst[1]
        if inst[0] is Dir.DOWN:
            current_row += inst[1]
        if inst[0] is Dir.LEFT:
            current_col -= inst[1]
        if inst[0] is Dir.RIGHT:
            current_col += inst[1]
        min_row = min(min_row, current_row)
        max_row = max(max_row, current_row)
        min_col = min(min_col, current_col)
        max_col = max(max_col, current_col)
    dim = (max_row-min_row+1), (max_col-min_col+1)
    start_point = (-min_row, -min_col)
    return dim, start_point


def fill_mat(mat: list[list[str]], start_point: tuple[int, int], instructions: list[Inst]) -> None:
    pos = start_point
    mat[pos[0]][pos[0]] = "#"
    for inst in instructions:
        d_r, d_c = inst[0].value
        for j in range(inst[1]):
            pos = (pos[0]+d_r, pos[1]+d_c)
            mat[pos[0]][pos[1]] = "#"
    
    for i in range(1, len(mat)-1):
        inside = False
        j = 0
        while j < len(mat[0])-1:
            if mat[i][j] == "#":
                if mat[i-1][j] == "#" and mat[i+1][j] == "#":
                    inside = not inside
                elif mat[i-1][j] == "#":
                    while j+1 < len(mat[0]) and mat[i][j+1] == "#":
                        j += 1
                    if mat[i+1][j] == "#":
                        inside = not inside
                elif mat[i+1][j] == "#":
                    while j+1 < len(mat[0]) and mat[i][j+1] == "#":
                        j += 1
                    if mat[i-1][j] == "#":
                        inside = not inside
            elif mat[i][j] == "." and inside:
                mat[i][j] = "#"
            j += 1


def fill_huge_mat(start_point: tuple[int, int], dimension: tuple[int, int], instructions: list[Inst]) -> None:
    paths = [start_point]
    for instruction in instructions:
        v = instruction[1]
        d_r = instruction[0].value[0] * v
        d_c = instruction[0].value[1] * v
        next_point = paths[-1][0]+d_r, paths[-1][1]+d_c
        paths.append(next_point)
    print(paths)
    covered_rows = {x[0]: [] for x in paths}
    for r in covered_rows:
        for i in range(len(paths)-1):
            if paths[i][0] == r and paths[i+1][0] == r:
                covered_rows[r].append((paths[i][1], paths[i+1][1]))
    
    for i in range(dimension[0]):
        if i in covered_rows:
            print(i, covered_rows[i])
    
    
    # filled = sum((x[1]-x[0]) for x in covered_rows[0])
    # for i in range(len):
    #     while j < len(mat[0])-1:
    #         if mat[i][j] == "#":
    #             if mat[i-1][j] == "#" and mat[i+1][j] == "#":
    #                 inside = not inside
    #             elif mat[i-1][j] == "#":
    #                 while j+1 < len(mat[0]) and mat[i][j+1] == "#":
    #                     j += 1
    #                 if mat[i+1][j] == "#":
    #                     inside = not inside
    #             elif mat[i+1][j] == "#":
    #                 while j+1 < len(mat[0]) and mat[i][j+1] == "#":
    #                     j += 1
    #                 if mat[i-1][j] == "#":
    #                     inside = not inside
    #         elif mat[i][j] == "." and inside:
    #             mat[i][j] = "#"
    #         j += 1


def pprint_mat(mat: list[list[str]]) -> None:
    for row in mat:
        print("".join(x for x in row))
    print()


def part1(file: str) -> int:
    inp = get_input(file)
    dim, start = get_dim(inp)
    mat = [["."]*dim[1] for _ in range(dim[0])]
    fill_mat(mat, start, inp)
    return sum(x == "#" for x in itertools.chain.from_iterable(mat))


def part2(file: str) -> int:
    # inp = get_corrected_input(file)
    inp = get_input(file)
    print(inp)
    dim, start = get_dim(inp)
    fill_huge_mat(start, dim, inp)



if __name__ == "__main__":
    part2("day18-input.txt.test")
