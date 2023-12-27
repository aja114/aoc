from collections import defaultdict
from functools import reduce

def get_input(s: str) -> tuple[int, list[dict[str, int]]]:
    id_, s = s.split(":")
    counters = []
    for colors in s.split(";"):
        counter = defaultdict(int)
        for color in colors.split(","):
            num, c = color.strip().split(" ")
            counter[c] = int(num)
        counters.append(counter)
    return int(id_[5:]), counters



with open("day2-input.txt", "r") as f:
   inp = f.readlines()

s = 0
for line in inp:
    id_, colors = get_input(line)
    limits = {
        "red": 0,
        "green": 0,
        "blue": 0 
    }
    for color in colors:
        for k, v in limits.items():
            if color[k] > v:
                limits[k] = color[k]
    s += reduce((lambda x, y: x * y), limits.values())
print(s)

