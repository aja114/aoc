import dataclasses
from collections import defaultdict

CARDS = ("A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2")
CARD_STRENGTH = {c: i for i, c in enumerate(CARDS[::-1])}
HAND_TYPE = ("Five", "Four", "FullHouse", "Three", "TwoPairs", "OnePair", "HighCard")
HAND_TYPE_STRENGHT = {h: i for i, h in enumerate(HAND_TYPE[::-1])}

print(HAND_TYPE_STRENGHT)


def get_hand_strenght(hand_counter: dict[str, int]) -> int:
    val = tuple(sorted(hand_counter.values()))
    if val == (5,):
        return HAND_TYPE_STRENGHT["Five"]
    if val == (1, 4):
        return HAND_TYPE_STRENGHT["Four"]
    if val == (2, 3):
        return HAND_TYPE_STRENGHT["FullHouse"]
    if val == (1, 1, 3):
        return HAND_TYPE_STRENGHT["Three"]
    if val == (1, 2, 2):
        return HAND_TYPE_STRENGHT["TwoPairs"]
    if val == (1, 1, 1, 2):
        return HAND_TYPE_STRENGHT["OnePair"]
    if val == (1, 1, 1, 1, 1):
        return HAND_TYPE_STRENGHT["HighCard"]


def get_hand_strenght_with_joker(hand_counter: dict[str, int]) -> int:
    if "J" not in hand_counter.keys() or len(hand_counter.keys()) == 1:
        return get_hand_strenght(hand_counter)
    num_j = hand_counter.pop("J")
    highest_card = max(hand_counter.keys(), key=lambda x: hand_counter[x]) 
    hand_counter[highest_card] += num_j
    return get_hand_strenght(hand_counter)


def counter(cards: list[str]) -> dict[str, int]:
    count = defaultdict(int)
    for card in cards:
        count[card] += 1
    return count


@dataclasses.dataclass
class Hand:
    cards: list[str]
    bid: int
    with_joker: bool
    hand_counter: dict[str, int] = dataclasses.field(init=False)
    hand_strength: int = dataclasses.field(init=False)
    
    def __post_init__(self):
        self.hand_counter = counter(self.cards)
        if self.with_joker:
            self.hand_strength = get_hand_strenght_with_joker(self.hand_counter)
        else:
            self.hand_strength = get_hand_strenght(self.hand_counter)
    
    def __lt__(self, other: "Hand"):
        if self.hand_strength == other.hand_strength:
            for sc, oc in zip(self.cards, other.cards):
                if sc == oc:
                    continue
                return CARD_STRENGTH[sc] < CARD_STRENGTH[oc]
        return self.hand_strength < other.hand_strength
    

def part1(h: list[Hand]) -> int:
    sorted_hands = sorted(h)
    return sum([hand.bid*(i+1) for i, hand in enumerate(sorted_hands)])
    
    
def part2(h: list[Hand]) -> int:
    CARD_STRENGTH["J"] = -1
    sorted_hands = sorted(h)
    return sum([hand.bid*(i+1) for i, hand in enumerate(sorted_hands)])


def get_input(file: str) -> list[Hand]:
    hands = []
    with open(file, "r") as f:
        for line in f.readlines():
            cards, bid = line.strip().split(" ")
            hands.append(Hand(bid=int(bid), cards=cards, with_joker=False))
    return hands


def get_input_with_joker(file: str) -> list[Hand]:
    hands_with_joker= []
    with open(file, "r") as f:
        for line in f.readlines():
            cards, bid = line.strip().split(" ")
            hands_with_joker.append(Hand(bid=int(bid), cards=cards, with_joker=True))
    return hands_with_joker


if __name__ == "__main__":
    hands = get_input("day7-input.txt")
    print(part1(hands))

    hands_with_joker = get_input_with_joker("day7-input.txt")
    print(part2(hands_with_joker))
