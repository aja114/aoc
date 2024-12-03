import dataclasses
import enum

matrix = list[list[str]]


class Dir(enum.Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)


MIRRORS = ("/", "\\")
SPLITTERS = ("|", "-")


@dataclasses.dataclass(frozen=True)
class Beam:
    direction: Dir
    position: tuple[int, int]


def reflect_beam(beam: Beam, mirror: str) -> Beam:
    if mirror == "\\":
        reflection = {
            Dir.UP: Dir.LEFT,
            Dir.DOWN: Dir.RIGHT,
            Dir.RIGHT: Dir.DOWN,
            Dir.LEFT: Dir.UP,
        }
    elif mirror == "/":
        reflection = {
            Dir.UP: Dir.RIGHT,
            Dir.DOWN: Dir.LEFT,
            Dir.RIGHT: Dir.UP,
            Dir.LEFT: Dir.DOWN,
        }
    else:
        raise ValueError(f"mirror does not exist: {mirror}")
    
    return Beam(direction=reflection[beam.direction], position=beam.position)
            
    
def split_beam(beam: Beam, splitter: str) -> list[Beam]:
    if splitter == "|" and beam.direction in (Dir.LEFT, Dir.RIGHT):
        return [
            Beam(direction=Dir.UP, position=beam.position),
            Beam(direction=Dir.DOWN, position=beam.position),
        ]
    if splitter == "-" and beam.direction in (Dir.UP, Dir.DOWN):
        return [
            Beam(direction=Dir.LEFT, position=beam.position),
            Beam(direction=Dir.RIGHT, position=beam.position),
        ]
    return [beam]
    

def get_input(file: str) -> list[list[str]]:
    with open(file, "r") as f:
        inp = [list(x.strip()) for x in f.readlines()]
    return inp


def advance_beams(map: matrix, energised_map: list[list[bool]], beams: list[Beam]) -> list[Beam]:
    new_beams = []
    for beam in beams:
        r, c = beam.position
        d_r, d_c = beam.direction.value
        energised_map[r][c] = True
        if not (0 <= r + d_r < len(map) and 0 <= c + d_c < len(map[0])):
            continue
        new_beam = Beam(direction=beam.direction, position=(r+d_r, c+d_c))
        el = map[r+d_r][c+d_c]
        if el in MIRRORS:
            new_beams.append(reflect_beam(new_beam, el))
        elif el in SPLITTERS:
            new_beams.extend(split_beam(new_beam, el))
        else:
            new_beams.append(new_beam)
    return new_beams


def energize_map(map: matrix, starting_beam: Beam) -> int:
    r, c = starting_beam.position
    el = map[r][c]
    if el in MIRRORS:
        beams = [reflect_beam(starting_beam, el)]
    elif el in SPLITTERS:
        beams = split_beam(starting_beam, el)
    else:
        beams = [starting_beam]
    energised_m = [[False]*len(map[0]) for _ in range(len(map))]
    seen_beams = set(beams)
    while beams:
        beams = advance_beams(map, energised_m, beams)
        beams = [b for b in beams if b not in seen_beams]
        seen_beams.update(set(beams))
    return sum([sum(x) for x in energised_m])


def part1(file: str):
    m = get_input(file)
    first_beam = Beam(direction=Dir.RIGHT, position=(0, 0))
    return energize_map(m, first_beam)


def part2(file: str):
    m = get_input(file)
    top_beams = [
        Beam(direction=Dir.DOWN, position=(0, i))
        for i in range(len(m[0]))
    ]
    bottom_beams = [
        Beam(direction=Dir.UP, position=(len(m)-1, i))
        for i in range(len(m[0]))
    ]
    left_beams = [
        Beam(direction=Dir.RIGHT, position=(i, 0))
        for i in range(len(m))
    ]
    right_beams = [
        Beam(direction=Dir.LEFT, position=(i, len(m[0])-1))
        for i in range(len(m))
    ]
    try_beams = top_beams + bottom_beams + left_beams + right_beams
    max_en = 0
    for try_beam in try_beams:
        max_en = max(max_en, energize_map(m, try_beam))
    return max_en


if __name__ == "__main__":
    print(part1("day16-input.txt"))
    print(part2("day16-input.txt"))
