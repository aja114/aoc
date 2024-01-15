import dataclasses
import typing

Grid3D: typing.TypeAlias = list[list[list[str]]]
Grid2D: typing.TypeAlias = list[list[str]]
Coord3D: typing.TypeAlias = tuple[int, int, int]
        
# TODO:
#  - make a tower class
#  - Keep track of the bricks on each level
#  - Make a colide function for two bricks
#  - remove the grid references and instead display using the tower


@dataclasses.dataclass
class Brick:
    start: Coord3D
    end: Coord3D
    id_: str


def get_input(file: str) -> list[Brick]:
    def line_to_brick(l: str, id_: int) -> Brick:
        start_str, end_str = l.strip().split("~")
        start = tuple(int(x) for x in start_str.split(",")[:3])
        end = tuple(int(x) for x in end_str.split(",")[:3])
        return Brick(start=start, end=end, id_=chr(65+id_))
    bricks = []
    with open(file, "r") as f:
        for i, l in enumerate(f.readlines()):
            bricks.append(line_to_brick(l, i))
    return bricks


def add_bricks_in_grid(grid: Grid3D, bricks: list[Brick]):
    for brick in bricks:
        add_brick_in_grid(grid, brick)
    

def add_brick_in_grid(grid: Grid3D, brick: Brick):
    dir = [s != e for s, e in zip(brick.start, brick.end)].index(True)
    s, e = brick.start[dir], brick.end[dir]
    p = brick.start
    for i in range(s, e+1):
        x, y, z = p
        grid[z][y][x] = brick.id_
        p = tuple(x if i != dir else x+1 for i, x in enumerate(p))


def prind_grid_2d(grid: Grid2D):
    for row in grid:
        print("".join(x for x in row))
    print()


def get_unblocked_elements(grid: Grid2D):
    row_l = len(grid[0])
    unblocked_elements = ["."] * row_l
    for i in range(row_l):
        j = 0
        while grid[j][i] == ".":
            j += 1
            if j >= len(grid):
                break
        else:
            unblocked_elements[i] = grid[j][i]
    return unblocked_elements


def print_side_view(grid: list[list[list[str]]], left_out_ax: int | str) -> None:
    axis = {"x", "y"}
    if left_out_ax not in axis:
        raise ValueError("Need axis to be x or y")
    if left_out_ax == "y":
        prind_grid_2d([get_unblocked_elements(cut) for cut in grid[::-1]])
    if left_out_ax == "x":
        rotated_grid = [[list(m) for m in zip(*z)] for z in grid[::-1]]
        prind_grid_2d([get_unblocked_elements(cut) for cut in rotated_grid])


def make_brick_fall(grid: Grid3D, bricks: list[Brick]) -> list[Brick]:
    sorted_bricks = list(sorted(bricks, key=lambda x: x.start[2]))
    new_bricks = []
    grid = get_empty_grid(len(grid[0][0]), len(grid[0]), len(grid))
    for brick in sorted_bricks:
        z_start = brick.start[2]
        shift = 0
        pos = [
            (x, y)
            for x in range(brick.start[0], brick.end[0] + 1)
            for y in range(brick.start[1], brick.end[1] + 1)
        ]
        while all([grid[z_start-shift-1][y][x] == "." for x, y in pos]):
            shift += 1
        new_brick = (
            Brick(
                start=(brick.start[0], brick.start[1], brick.start[2]-shift),
                end=(brick.end[0], brick.end[1], brick.end[2]-shift),
                id_=brick.id_
            )
        )
        new_bricks.append(new_brick)
        add_brick_in_grid(grid, new_brick)
    return grid, new_bricks


def desint_bricks(bricks: list[Brick]) -> int:
    ...
    return 0


def get_empty_grid(len_x, len_y, len_z) -> Grid3D:
    grid: Grid3D = (
        [
            [
                [
                    "." if z > 0 else "_"
                    for _ in range(0, len_x)
                ]
                for _ in range(0, len_y)
            ]
            for z in range(0, len_z)
        ]
    )
    return grid


def part1(file: str) -> int:
    bricks = get_input(file)    

    len_x = max(b.end[0] for b in bricks) + 1
    len_y = max(b.end[1] for b in bricks) + 1
    len_z = max(b.end[2] for b in bricks) + 1
    grid = get_empty_grid(len_x, len_y, len_z)
    add_bricks_in_grid(grid, bricks)

    print("x", "z")
    print_side_view(grid, "y")
    print("y", "z")
    print_side_view(grid, "x")

    new_grid, fallen_bricks = make_brick_fall(grid, bricks)
    print("x", "z")
    print_side_view(new_grid, "y")
    print("y", "z")
    print_side_view(new_grid, "x")
    
    # return desint_bricks(new_grid, fallen_bricks)


if __name__ == "__main__":
    print(part1("day22-input.txt.test"))
