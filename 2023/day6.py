from functools import reduce


def get_input(file: str) -> list[tuple[int, int]]:
    with open(file, "r") as f:
        time_str, dist_str, *_ = f.readlines()
    times = [int(x) for x in time_str.strip().split(" ") if x.isdigit()]
    dists = [int(x) for x in dist_str.strip().split(" ") if x.isdigit()]
    return list(zip(times, dists))
    
    
def get_input_no_kerning(file: str) -> tuple[int, int]:
    with open(file, "r") as f:
        time_str, dist_str, *_ = f.readlines()
    time = int(time_str.strip().split(":")[1].replace(" ", ""))
    dist = int(dist_str.strip().split(":")[1].replace(" ", ""))
    return time, dist


def travelled_distance(pressed_time, total_time):
    remaining_time = total_time - pressed_time
    return remaining_time * pressed_time
    
    
def part1(races: list[tuple[int, int]]) -> int:
    res = []
    for race in races:
        time, dist = race
        min_pressed_t = 0
        while min_pressed_t < time:
            if travelled_distance(min_pressed_t, time) > dist:
                break
            min_pressed_t += 1
        max_pressed_t = time
        while max_pressed_t > min_pressed_t:
            if travelled_distance(max_pressed_t, time) > dist:
                break
            max_pressed_t -= 1
        res.append(max_pressed_t - min_pressed_t + 1)
    return reduce(lambda x, y: x*y, res)


def part2(time: int, dist: int):
    min_pressed_t = 0
    while min_pressed_t < time:
        if travelled_distance(min_pressed_t, time) > dist:
            break
        min_pressed_t += 1
    max_pressed_t = time
    while max_pressed_t > min_pressed_t:
        if travelled_distance(max_pressed_t, time) > dist:
            break
        max_pressed_t -= 1
    return max_pressed_t - min_pressed_t + 1


if __name__ == "__main__":
    r = get_input("inputs/day6-input.txt")
    print(part1(r))
    
    t, d = get_input_no_kerning("inputs/day6-input.txt")
    print(part2(t, d))
