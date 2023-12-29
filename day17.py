import dataclasses
import enum
import heapq
from typing import Callable

matrix = list[list[int]]


class Dir(enum.Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)


OPPOSITE_DIRS = {
    Dir.UP: Dir.DOWN,
    Dir.DOWN: Dir.UP,
    Dir.RIGHT: Dir.LEFT,
    Dir.LEFT: Dir.RIGHT,
}

ORTHOGONAL_DIRS = {
    Dir.UP: (Dir.LEFT, Dir.RIGHT),
    Dir.DOWN:  (Dir.LEFT, Dir.RIGHT),
    Dir.RIGHT:  (Dir.UP, Dir.DOWN),
    Dir.LEFT:  (Dir.UP, Dir.DOWN),
}


@dataclasses.dataclass(slots=True, frozen=True)
class Path:
    last_dirs: list[Dir | None] = dataclasses.field(hash=False)
    position: tuple[int, int]
    loss: int = dataclasses.field(hash=False)

    def key(self) -> tuple:
        return (*self.position, *tuple(self.last_dirs))
    
    def __lt__(self, other: "Path") -> bool:
        return self.loss < other.loss
        

def get_input(file: str) -> matrix:
    with open(file, "r") as f:
        inp = [
            [int(y) for y in x.strip()]
            for x in f.readlines()
        ]
    return inp


def get_allowed_directions_cubicle(path: Path) -> tuple[Dir, ...]:
    last_dir = path.last_dirs[-1]
    if len(set(path.last_dirs)) == 1:
        return ORTHOGONAL_DIRS[last_dir]
    return tuple(d for d in OPPOSITE_DIRS.keys() if d != OPPOSITE_DIRS[last_dir])


def get_allowed_directions_ultra_cubicle(path: Path) -> tuple[Dir, ...]:
    last_dir = path.last_dirs[-1]
    if len(set(path.last_dirs[-4:])) != 1:
        return (last_dir,)
    if len(set(path.last_dirs[-10:])) == 1:
        return ORTHOGONAL_DIRS[last_dir]
    return tuple(d for d in OPPOSITE_DIRS.keys() if d != OPPOSITE_DIRS[last_dir])
    

def best_path(
    mat: matrix,
    start_path: Path,
    stop_distance: int,
    new_direction_fn: Callable[[Path], tuple[Dir, ...]],
) -> int:
    paths = [start_path]
    end_pos = (len(mat)-1, len(mat[0])-1)
    heapq.heapify(paths)
    seen_pos = {start_path.key()}
    i = 0
    while True:
        path = heapq.heappop(paths)
        i += 1
        if path.position == end_pos:            
            if len(set(path.last_dirs[-stop_distance:])) > 1:
                continue
            return path.loss
        allowed_dirs = new_direction_fn(path)
        for allowed_dir in allowed_dirs:
            r, c = path.position
            d_r, d_c = allowed_dir.value
            if not (0 <= r+d_r < len(mat) and 0 <= c+d_c < len(mat[0])):
                continue
            new_path = Path(
                last_dirs=[*path.last_dirs[1:], allowed_dir],
                position=(r+d_r, c+d_c),
                loss=path.loss+mat[r+d_r][c+d_c],
            )
            if new_path.key() in seen_pos:
                continue
            seen_pos.add(new_path.key())
            heapq.heappush(paths, new_path)


def part1(file: str) -> int:
    mat = get_input(file)
    start_path = Path(
        last_dirs=[None, None, Dir.RIGHT],
        position=(0, 0),
        loss=0
    )
    return best_path(
        mat=mat,
        start_path=start_path,
        stop_distance=1,
        new_direction_fn=get_allowed_directions_cubicle,
    )


def part2(file: str) -> int:
    mat = get_input(file)
    start_path = Path(
        last_dirs=[None] * 9 + [Dir.RIGHT],
        position=(0, 0),
        loss=0
    )
    return best_path(
        mat=mat,
        start_path=start_path,
        stop_distance=4,
        new_direction_fn=get_allowed_directions_ultra_cubicle,
    )


if __name__ == "__main__":
    print(part1("day17-input.txt.test"))
