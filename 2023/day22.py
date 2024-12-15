import dataclasses
import typing
from collections import defaultdict

Grid3D: typing.TypeAlias = list[list[list[str]]]
Grid2D: typing.TypeAlias = list[list[str]]
Coord3D: typing.TypeAlias = tuple[int, int, int]
Coord2D: typing.TypeAlias = tuple[int, int]


class Tower:
    bricks: list["Brick"]
    z_levels: dict[int, list["Brick"]]

    def __init__(self, bricks: list["Brick"]):
        # Add ground
        self.lx, self.ly, self.lz = get_tower_dimensions(bricks)
        ground = Brick(
            start=(0, 0, 0),
            end=(self.lx - 1, self.ly - 1, 0),
            id_="_"
        )
        self.bricks = [ground]
        self.bricks.extend(bricks)

    @property
    def z_levels(self):
        z_levels = defaultdict(list)
        for b in self.bricks:
            for z in range(b.start[2], b.end[2] + 1):
                z_levels[z].append(b)
        return z_levels

    def let_brick_fall(self):
        for brick in sorted(self.bricks, key=lambda x: x.start[2]):
            z_start = brick.start[2]
            shift = 0
            z_levels = self.z_levels
            while True:
                if z_start - (shift + 1) < 0:
                    break
                for other_brick in z_levels[z_start - (shift + 1)]:
                    if brick != other_brick and collide(brick, other_brick):
                        break
                else:
                    shift += 1
                    continue
                break
            brick.start = (brick.start[0], brick.start[1], brick.start[2] - shift)
            brick.end = (brick.end[0], brick.end[1], brick.end[2] - shift)

    def get_brick_support(self):
        support = {}
        supported_by = {}
        z_levels = self.z_levels
        for brick in sorted(self.bricks, key=lambda x: x.start[2]):
            support[brick] = [
                other_brick for other_brick in z_levels[brick.end[2] + 1]
                if collide(brick, other_brick)
            ]
            supported_by[brick] = [
                other_brick for other_brick in z_levels[brick.start[2] - 1]
                if collide(brick, other_brick)
            ]
        return support, supported_by

    def get_empty_grid(self) -> Grid3D:
        grid = [
            [
                [
                    "." if z > 0 else "_"
                    for _ in range(0, self.lx)
                ]
                for _ in range(0, self.ly)
            ]
            for z in range(0, self.lz)
        ]
        return grid

    @property
    def grid(self):
        grid = self.get_empty_grid()
        for z, bricks in self.z_levels.items():
            for brick in bricks:
                for x, y in brick.horizontal_pos:
                    grid[z][y][x] = brick.id_
        return grid

    def print_side_view(self, left_out_ax: int | str) -> None:
        axis = {"x", "y"}
        if left_out_ax not in axis:
            raise ValueError("Need axis to be x or y")
        if left_out_ax == "y":
            prind_grid_2d([get_unblocked_elements(cut) for cut in self.grid[::-1]])
        if left_out_ax == "x":
            rotated_grid = [[list(m) for m in zip(*z)] for z in self.grid[::-1]]
            prind_grid_2d([get_unblocked_elements(cut) for cut in rotated_grid])


@dataclasses.dataclass(unsafe_hash=True)
class Brick:
    start: Coord3D
    end: Coord3D
    id_: str

    @property
    def horizontal_pos(self) -> set[Coord2D]:
        pos = {
            (x, y)
            for x in range(self.start[0], self.end[0] + 1)
            for y in range(self.start[1], self.end[1] + 1)
        }
        return pos


def collide(brick1: Brick, brick2: Brick) -> bool:
    return len(
        set.intersection(brick1.horizontal_pos, brick2.horizontal_pos)
    ) > 0


def get_tower_dimensions(bricks: list[Brick]) -> tuple[int, int, int]:
    lx = max(b.end[0] for b in bricks) + 1
    ly = max(b.end[1] for b in bricks) + 1
    lz = max(b.end[2] for b in bricks) + 1
    return lx, ly, lz


def get_input(file: str) -> list[Brick]:
    def line_to_brick(l: str, id_: int) -> Brick:
        start_str, end_str = l.strip().split("~")
        start = tuple(int(x) for x in start_str.split(",")[:3])
        end = tuple(int(x) for x in end_str.split(",")[:3])
        return Brick(start=start, end=end, id_=str(id_))

    bricks = []
    with open(file, "r") as f:
        for i, l in enumerate(f.readlines()):
            bricks.append(line_to_brick(l, i))
    return bricks


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


def part1_2(file: str) -> tuple[int, int]:
    bricks = get_input(file)
    tower = Tower(bricks)
    tower.let_brick_fall()
    support, supported_by = tower.get_brick_support()

    part1_res = 0
    safe_bricks = set()
    for brick, support_bricks in support.items():
        for support_brick in support_bricks:
            if supported_by[support_brick] == [brick]:
                break
        else:
            safe_bricks.add(brick)
            part1_res += 1
    
    part2_res = 0
    for brick in tower.bricks:
        if brick in safe_bricks or brick.id_ == "_":
            continue
        fallen = {brick}
        falling_bricks = set(
            b for b in support[brick]
            if not (set(supported_by[b]) - fallen)
        )
        while falling_bricks:
            fallen.update(falling_bricks)
            falling_bricks = set(
                b for fb in falling_bricks for b in support[fb]
                if not (set(supported_by[b]) - fallen)
            )
        part2_res += len(fallen)-1
    return part1_res, part2_res


if __name__ == "__main__":
    print(part1_2("inputs/day22-input.txt"))
