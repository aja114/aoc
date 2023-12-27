import enum

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
        print(len(path) // 2)
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


def part1(file: str):
    mat = get_input(file)
    start = get_start(mat)
    for x in MAP_DIR.keys():
        p = get_path(
            mat,
            [start, (start[0]+MAP_DIR[x][0], start[1]+MAP_DIR[x][1])],
            from_dir=rever_dir[x]
        )
        if p:
            return p


def part2(file: str):
    from colorama import Fore
    mat = get_input(file)
    path = part1(file)
    
    vertical_signs = {"|", "L", "J", "F", "7"} 
    
    for i in range(len(mat)):
        inside = False
        for j in range(len(mat[0])):
            if (i, j) in path and mat[i][j] in vertical_signs:
                inside = not inside
            elif (i, j) not in path:
                if inside:
                    mat[i][j] = "I"
                else:
                    mat[i][j] = "O"

    for i, j in path:
        if mat[i][j] == "S":
            mat[i][j] = Fore.GREEN + mat[i][j] + Fore.RESET
        else:
            mat[i][j] = Fore.RED + mat[i][j] + Fore.RESET

    store_output("day10-output.txt", mat)


if __name__ == "__main__":
    import sys
    sys. setrecursionlimit(100_000)
    part2("day10-input.txt.test")
