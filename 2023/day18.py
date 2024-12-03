import dataclasses
import enum
import itertools

Inst = tuple["Dir", int, str]


@dataclasses.dataclass
class Interval:
    """The interval is a close one: [min, max]."""
    min: int
    max: int

    def range(self):
        return self.max - self.min + 1

    def contains(self, val):
        return self.min <= val <= self.max

    def __lt__(self, other):
        return self.min < other.min

    @classmethod
    def from_consec(cls, intervals: list["Interval"]) -> "Interval":
        return cls(
            min=intervals[0].min,
            max=intervals[-1].max
        )


@dataclasses.dataclass
class Row:
    """Represent a row in the matrix."""
    path_intervals: list[Interval]
    min: int = dataclasses.field(repr=False)
    max: int = dataclasses.field(repr=False)
    filled_intervals: list[Interval] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.path_intervals = list(sorted(self.path_intervals))

    def get_intervals_not_path(self):
        intervals_not_cov = []
        start = self.min
        for interval in self.path_intervals:
            if interval.contains(start):
                start = interval.max + 1
                continue
            else:
                intervals_not_cov.append(
                    Interval(min=start, max=interval.min-1)
                )
                start = interval.max + 1
        if start < self.max:
            intervals_not_cov.append(
                Interval(min=start, max=self.max)
            )
        return intervals_not_cov


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
    # Create the row representations
    paths = [start_point]
    for instruction in instructions:
        v = instruction[1]
        d_r = instruction[0].value[0] * v
        d_c = instruction[0].value[1] * v
        next_point = paths[-1][0]+d_r, paths[-1][1]+d_c
        paths.append(next_point)
    print(paths)
    covered_rows = {}
    for r, _ in paths:
        intervals = []
        for i in range(len(paths)-1):
            if paths[i][0] == r and paths[i+1][0] == r:
                intervals.append(
                    Interval(
                        min=min(paths[i][1], paths[i+1][1]),
                        max=max(paths[i][1], paths[i+1][1])
                    )
                )
        covered_rows[r] = Row(
            min=0,
            max=dimension[1]-1,
            path_intervals=intervals,
        )

    # fill the rows
    covered_rows_indexes = list(sorted(covered_rows.keys()))
    for idx, i in enumerate(covered_rows_indexes):
        row = covered_rows[i]
        print(i, row)
        print(row.get_intervals_not_path())
        if i == min(covered_rows_indexes) or i == max(covered_rows_indexes):
            continue
        inside = False
        filled_intervals = []
        all_intervals = list(sorted(row.path_intervals + row.get_intervals_not_path()))
        print(all_intervals)
        for interv in all_intervals:
            if interv in row.path_intervals:
                if check_horizontal(
                    interv,
                    covered_rows[covered_rows_indexes[idx-1]],
                    covered_rows[covered_rows_indexes[idx+1]],
                ):
                    inside = not inside
            elif inside:
                filled_intervals.append(interv)
        print(filled_intervals)
        row = Row(
            path_intervals=row.path_intervals,
            filled_intervals=filled_intervals,
            min=row.min,
            max=row.max
        )
        covered_rows[i] = row
    
    print("-"*150)
    # Calculate the results
    res = 0
    for idx, i in enumerate(covered_rows_indexes):
        row = covered_rows[i]
        res += sum(x.range() for x in row.path_intervals)
        if idx == len(covered_rows_indexes)-2:
            continue
        next_row_index = covered_rows_indexes[idx+1]
        row_diff = next_row_index - i
        next_row = get_next_row(row, covered_rows[covered_rows_indexes[idx+1]])
        res += row_diff * get_overlapp(row, next_row)
    print(res)


def check_horizontal(interval: Interval, previous_row: Row, next_row: Row) -> bool:
    if any(pi.contains(interval.min) for pi in previous_row.path_intervals) and \
       any(ni.contains(interval.max) for ni in next_row.path_intervals):
        return True
    if any(pi.contains(interval.max) for pi in previous_row.path_intervals) and \
       any(ni.contains(interval.min) for ni in next_row.path_intervals):
        return True
    return False


def get_overlapp(row1: Row, row2: Row):
    intervals_1 = sorted(row1.path_intervals+row1.filled_intervals)
    intervals_2 = sorted(row2.path_intervals+row2.filled_intervals)
    overlapp = []
    j = 0
    i = 0
    while j < len(intervals_1):
        if intervals_1[j].max < intervals_2[i].min:
            j += 1
        while i < len(intervals_2) and intervals_1[j].min > intervals_2[i].max:
            i += 1
        overlapp.append(Interval(
            min=max(intervals_1[j].min, intervals_2[i].min),
            max=min(intervals_1[j].max, intervals_2[i].max),
        ))
        if min(intervals_1[j].max, intervals_2[i].max) == intervals_1[j].max:
            j += 1
        else:
            i += 1

    print("*"*150)
    print(row1)
    print(row2)
    print(overlapp)
    return sum(x.range() for x in overlapp)

def get_in_between_row(row: Row, next_row: Row) -> Row:
    ...


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
    dim, start = get_dim(inp)
    fill_huge_mat(start, dim, inp)


if __name__ == "__main__":
    part2("day18-input.txt.test")
