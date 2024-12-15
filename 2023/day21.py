import enum

Matrix = list[list[str]]
Position = tuple[int, int]


class Dir(enum.Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)


def get_input(file: str) -> Matrix:
    with open(file, "r") as f:
        inp = [list(x.strip()) for x in f.readlines()]
    return inp


def get_start(mat: Matrix) -> Position:
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == "S":
                return i, j
            

def get_next_position(p: Position, mat: Matrix) -> list[Position]:
    r, c = p
    return [
        (r+d.value[0], c+d.value[1])
        for d in Dir
        if (0 <= r+d.value[0] < len(mat)
            and 0 <= c+d.value[1] < len(mat[0])
            and mat[r+d.value[0]][c+d.value[1]] != "#"
        )
    ]


def part1(file: str) -> int:
    mat = get_input(file)
    start = get_start(mat)
    current_pos = {start}
    n = 64
    print(start)
    for _ in range(n):
        next_pos = set()
        for p in current_pos:
            next_pos.update(
                {
                    np for np in get_next_position(p, mat)
                }
            )
        current_pos = next_pos
        print(next_pos)
    return len(current_pos)


if __name__ == '__main__':
    print(part1("inputs/day21-input.txt"))
