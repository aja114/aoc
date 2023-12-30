import enum
import itertools
import sys
sys. setrecursionlimit(100_000)

matrix = list[list[str]]
position = tuple[int, int]


class Dir(enum.Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


MAP_DIR = {
    Dir.LEFT: (0, -1),
    Dir.UP: (-1, 0),
    Dir.RIGHT: (0, 1),
    Dir.DOWN: (1, 0),
}


PIPES = {
    "|": {Dir.DOWN, Dir.UP},
    "-": {Dir.LEFT, Dir.RIGHT},
    "L": {Dir.UP, Dir.RIGHT},
    "J": {Dir.UP, Dir.LEFT},
    "7": {Dir.LEFT, Dir.DOWN},
    "F": {Dir.DOWN, Dir.RIGHT},
}

rever_dir = {
    Dir.UP: Dir.DOWN,
    Dir.DOWN: Dir.UP,
    Dir.RIGHT: Dir.LEFT,
    Dir.LEFT: Dir.RIGHT,
}


def get_path(mat: matrix, path: list[position], from_dir: Dir) -> list[position] | None:
    pos = path[-1]
    if pos[0] < 0 or pos[0] >= len(mat) or pos[1] < 0 or pos[1] >= len(mat[0]):
        return None
    pipe = mat[pos[0]][pos[1]]
    if pipe == "S":
        return path
    pipe_dir = PIPES.get(pipe, {})
    if from_dir not in pipe_dir:
        return None
    next_dir = list(pipe_dir - {from_dir})[0]
    next_pos = (pos[0]+MAP_DIR[next_dir][0], pos[1]+MAP_DIR[next_dir][1])
    return get_path(
        mat=mat,
        path=path+[next_pos],
        from_dir=rever_dir[next_dir]
    )


def get_input(file: str) -> matrix:
    with open(file, "r") as f:
        mat = [
            list(x.strip()) for x in f.readlines()  
        ]
    return mat


def get_start(mat: matrix) -> position:
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == "S":
                return i, j


def store_output(file: str, mat: matrix):
    with open(file, "w") as f:
        f.write(
            "\n".join("".join(x) for x in mat)
        )


def part1(file: str) -> int:
    mat = get_input(file)
    start = get_start(mat)
    for x in MAP_DIR.keys():
        p = get_path(
            mat,
            [start, (start[0]+MAP_DIR[x][0], start[1]+MAP_DIR[x][1])],
            from_dir=rever_dir[x]
        )
        if p:
            return len(p) // 2
    return -1

def part2(file: str):
    mat = get_input(file)
    start = get_start(mat)
    for x in MAP_DIR.keys():
        path = get_path(
            mat,
            [start, (start[0]+MAP_DIR[x][0], start[1]+MAP_DIR[x][1])],
            from_dir=rever_dir[x]
        )
        if path:
            break

    # Replace S with pipe
    d_r1, d_c1 = path[1][0]-path[0][0], path[1][1]-path[0][1]
    d_r2, d_c2 = path[-2][0]-path[0][0], path[-2][1]-path[0][1]
    print(d_r1, d_c1)
    print(d_r2, d_c2)

    for pipe, pipe_val in PIPES.items():
        dirs = set(MAP_DIR[d] for d in pipe_val)
        print(dirs)
        if {(d_r1, d_c1), (d_r2, d_c2)} == set(dirs):
            mat[start[0]][start[1]] = pipe
            print(pipe)
            break

    for i in range(1, len(mat)-1):
        inside = False
        j = 0
        while j < len(mat[0])-1:
            if (i, j) not in path:
                if inside:
                    mat[i][j] = "I"
            else:
                if mat[i][j] == "|":
                    inside = not inside
                elif mat[i][j] == "L":
                    while j+1 < len(mat[0]) and mat[i][j+1] == "-":
                        j += 1
                    if mat[i][j+1] == "7":
                        inside = not inside
                elif mat[i][j] == "F":
                    while j+1 < len(mat[0]) and mat[i][j+1] == "-":
                        j += 1
                    if mat[i][j+1] == "J":
                        inside = not inside
            j += 1

    print("\n".join("".join(x) for x in mat))

    return sum(x == "I" for x in itertools.chain.from_iterable(mat))


if __name__ == "__main__":
    print(part1("day10-input.txt"))
