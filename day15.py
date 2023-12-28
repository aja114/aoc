import collections
import functools


def get_input(file: str) -> list[str]:
    with open(file, "r") as f:
        inp = [x.strip() for x in f.read().strip().split(",")]
    return inp


@functools.cache
def hash_str(string: str) -> int:
    s = 0
    for c in string:
        s += ord(c)
        s *= 17
        s %= 256
    return s


def hash_many_str(strings: list[str]) -> int:
    s = 0
    for string in strings:
        s += hash_str(string)
    return s


def part1(file: str) -> int:
    inp = get_input(file)
    return hash_many_str(inp)
    

def split_instruction(instruction: str) -> tuple[str, str]:
    if "=" in instruction:
        sep = "="
    elif "-" in instruction:
        sep = "-"
    else:
        raise ValueError(f"invalid instruction {instruction}")
    idx = instruction.index(sep)
    box = instruction[:idx]
    action = instruction[idx:]
    return box, action
    

def remove_from_box(box: list[tuple[str, int]], label: str):
    for i, (l, _) in enumerate(box):
        if l == label:
            box.pop(i)
            break


def add_to_box(box: list[tuple[str, int]], label: str, focus: int):
    for i, (l, _) in enumerate(box):
        if l == label:
            box[i] = (label, focus)
            break
    else:
        box.append((label, focus))


def part2(file: str) -> int:
    inp = get_input(file)
    instructions = [split_instruction(i) for i in inp]
    boxes = collections.defaultdict(list)
    for instruction in instructions:
        label = instruction[0]
        box = boxes[hash_str(label)]
        action = instruction[1]
        if action[0] == "=":
            add_to_box(box, label, int(action[1:]))
        if action[0] == "-":
            remove_from_box(box, label)
    print(boxes)
    s = 0
    for box, lenses in boxes.items():
        for i, lens in enumerate(lenses):
            s += (box+1)*(i+1)*(int(lens[1]))
    return s


if __name__ == "__main__":
    print(part2("day15-input.txt"))
