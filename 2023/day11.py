import dataclasses


@dataclasses.dataclass()
class Point:
    value: str
    d_r: int
    d_c: int
    gal_num: int | None = dataclasses.field(default=None)
    
    def is_gal(self):
        return self.value == "#"


def get_input(file: str) -> list[list[str]]:
    with open(file, "r") as f:
        galmap = [list(l.strip()) for l in f.readlines()]
    return galmap


def expand(galmap: list[list[str]], expansion_dist: int = 2) -> list[list[Point]]:
    rows_to_expand = []
    for i, galrow in enumerate(galmap):
        if all(x == "." for x in galrow):
            rows_to_expand.append(i)
    cols_to_expand = []
    for i, galcol in enumerate(zip(*galmap)):
        if all(x == "." for x in galcol):
            cols_to_expand.append(i)
    expanded_map = [
        [Point(value=".", d_r=1, d_c=1) for _ in range(len(galmap[0]))]
        for _ in range(len(galmap))
    ]
    for r in range(len(galmap)):
        for c in range(len(galmap[0])):
            expanded_map[r][c] = Point(
                value=galmap[r][c],
                d_r=expansion_dist if r in rows_to_expand else 1,
                d_c=expansion_dist if c in cols_to_expand else 1
            )
    return expanded_map


def pprint_map(galmap: list[list[Point]]) -> None:
    for galrow in galmap:
        print("".join(x.value for x in galrow))


def name_gal_inplace(galmap: list[list[Point]]) -> int:
    n = 0
    for i in range(len(galmap)):
        for j in range(len(galmap[0])):
            if galmap[i][j].is_gal():
                galmap[i][j].gal_num = n
                n += 1
    return n


def gal_dist(start_gal: int, target_gals: set[int], galmap: list[list[Point]]):
    start_point = (-1, -1)
    target_gals = set(target_gals)
    gals_dist: dict[int, int] = {}
    for i in range(len(galmap)):
        for j in range(len(galmap[0])):
            if galmap[i][j].gal_num == start_gal:
                start_point = (i, j)
                break
                
    current_points = {
        start_point: 0
    }
    visited_points = set()
    while current_points:
        next_points = {}
        for current_point, dist in current_points.items():
            for d_r, d_c in [(0, -1), (0, 1), (1, 0)]:
                r, c = current_point
                n = (r+d_r, c+d_c)
                if 0 <= n[0] < len(galmap) and 0 <= n[1] < len(galmap[0]):
                    new_dist = dist + galmap[n[0]][n[1]].d_c if d_r == 0 else dist + galmap[n[0]][n[1]].d_r
                    if galmap[n[0]][n[1]].gal_num in (target_gals - set(gals_dist.keys())):
                        gals_dist[galmap[n[0]][n[1]].gal_num] = new_dist
                    if n not in visited_points:
                        next_points[n] = new_dist
                        visited_points.add(n)
        current_points = next_points
    return gals_dist


def sum_gal_dist(galmap: list[list[Point]], num_gal: int) -> int:
    s = 0
    for n in range(num_gal):
        dists = gal_dist(n, set(range(n+1, num_gal)), galmap)
        s += sum(dists.values())
    return s
    

def part1(file: str) -> int:
    input_map = get_input(file)
    input_map = expand(input_map, expansion_dist=2)
    num_gal = name_gal_inplace(input_map)
    return sum_gal_dist(galmap=input_map, num_gal=num_gal)


def part2(file: str) -> int:
    input_map = get_input(file)
    input_map = expand(input_map, expansion_dist=1_000_000)
    num_gal = name_gal_inplace(input_map)
    return sum_gal_dist(galmap=input_map, num_gal=num_gal)


if __name__ == "__main__":
    print(part1("inputs/day11-input.txt"))
    print(part2("inputs/day11-input.txt"))
