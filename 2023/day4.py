def get_card(s: str) -> tuple[str, list[str], list[str]]:
    id_str, all_nums, *_ = s.strip().split(":")
    id_ = id_str.split(" ")[-1]
    winning_nums_str, scratched_nums_str, *_ = all_nums.split("|")
    winning_nums = [x for x in winning_nums_str.split(" ") if x != ""]
    scratched_nums = [x for x in scratched_nums_str.split(" ") if x != ""]
    return id_, winning_nums, scratched_nums


def get_input(file: str) -> dict[int, tuple[list[str], list[str]]]:
    input_ = {}
    with open(file, "r") as f:
        for line in f.readlines():
            id_, winning_nums, scratched_nums = get_card(line)
            input_[int(id_)] = (winning_nums, scratched_nums)
    return input_


def part1(cards: dict[int, tuple[list[str], list[str]]]) -> int:
    s = 0
    for card in cards.values():
        winning_nums, scratched_nums = set(card[0]), set(card[1])
        count = len(set.intersection(scratched_nums, winning_nums))
        if count > 0:
            s += 2**(count-1)
    return s
    

def part2(cards: dict[int, tuple[list[str], list[str]]]) -> int:
    to_scratch = {
        card_id: 1
        for card_id in cards
    }
    scratched = {}
    for card_id, repeat in to_scratch.items():
        scratched[card_id] = repeat
        card = cards[card_id]
        winning_nums, scratched_nums = set(card[0]), set(card[1])
        count = len(set.intersection(scratched_nums, winning_nums))
        for i in range(1, count+1):
            to_scratch[card_id + i] += repeat
    return sum(scratched.values())


if __name__ == "__main__":
    print(part1(get_input("inputs/day4-input.txt")))
    print(part2(get_input("inputs/day4-input.txt")))
