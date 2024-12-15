from math import lcm


def get_input(file: str) -> tuple[list[str], dict[str, dict[str, str]]]:
    with open(file, "r") as f:
        instruction_str, nodes_str, *_ = f.read().strip().split("\n\n")
    
    instructions = list(instruction_str.strip())
    nodes = {}
    for node_str in nodes_str.strip().split("\n"):
        node_id = node_str[:3]
        left_node = node_str[7:10]
        right_node = node_str[12:15]
        nodes[node_id] = {
            "L": left_node,
            "R": right_node,
        }
    return instruction_str, nodes


def part1(file: str) -> int:
    inst, n = get_input(file)
    i = 0
    start = "AAA"
    target = "ZZZ"
    curr_node = start
    while curr_node != target:
        curr_node = n[curr_node][inst[i % len(inst)]]
        i += 1
    return i


def part2(file: str):
    inst, nodes = get_input(file)
    start_nodes = [
        n for n in nodes.keys()
        if n[-1] == "A"
    ]
    target_nodes = set(
        n for n in nodes.keys()
        if n[-1] == "Z"
    )
    cur_nodes = start_nodes
    node_step = {}
    for start in cur_nodes:
        i = 0
        curr_node = start
        while curr_node not in target_nodes:
            curr_node = nodes[curr_node][inst[i % len(inst)]]
            i += 1
        node_step[start] = i
    return lcm(*node_step.values())


if __name__ == "__main__":
    print(part1("inputs/day8-input.txt"))
    print(part2("inputs/day8-input.txt"))
