from dataclasses import dataclass
from itertools import product

JOKER = -1


def get_cards(line: str) -> list[int]:
    cards_as_strings = [c for c in line]
    strength_map = {"A": 14, "K": 13, "Q": 12, "J": JOKER, "T": 10}
    return [int(strength_map.get(c, c)) for c in cards_as_strings]


ALL_CARDS_BESIDES_JOKER = [14, 13, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2]


def is_five_of_a_kind(hand: list[int]) -> bool:
    return len(set(hand)) == 1


assert is_five_of_a_kind([1, 1, 1, 1, 1]) == True
assert is_five_of_a_kind([1, 1, 1, 1, 2]) == False


def is_four_of_a_kind(hand: list[int]) -> bool:
    for card in set(hand):
        if hand.count(card) == 4:
            return True
    return False


assert is_four_of_a_kind([1, 1, 1, 1, 1]) == False
assert is_four_of_a_kind([1, 1, 1, 1, 2]) == True


def is_full_house(hand: list[int]) -> bool:
    return len(set(hand)) == 2 and not is_four_of_a_kind(hand)


assert is_full_house([1, 1, 1, 2, 2]) == True
assert is_full_house([1, 1, 1, 3, 2]) == False


def is_three_of_a_kind(hand: list[int]) -> bool:
    if is_full_house(hand):
        return False
    for card in set(hand):
        if hand.count(card) == 3:
            return True
    return False


assert is_three_of_a_kind([1, 1, 1, 2, 2]) == False
assert is_three_of_a_kind([1, 1, 1, 3, 2]) == True
assert is_three_of_a_kind([1, 1, 7, 3, 2]) == False


def is_two_pair(hand: list[int]) -> bool:
    number_of_pairs = 0
    for card in set(hand):
        if hand.count(card) == 2:
            number_of_pairs += 1
    return number_of_pairs == 2


assert is_two_pair([1, 1, 1, 2, 2]) == False
assert is_two_pair([1, 1, 8, 2, 2]) == True
assert is_two_pair([1, 1, 1, 3, 2]) == False


def is_one_pair(hand: list[int]) -> bool:
    number_of_pairs = 0
    counts = set()
    for card in set(hand):
        c = hand.count(card)
        if c == 2:
            number_of_pairs += 1
        counts.add(c)
    return number_of_pairs == 1 and counts == {1, 2}


assert is_one_pair([1, 1, 1, 2, 2]) == False
assert is_one_pair([1, 1, 8, 2, 2]) == False
assert is_one_pair([1, 1, 8, 3, 2]) == True


def is_high_card(hand: list[int]) -> bool:
    return len(set(hand)) == 5


assert is_high_card([1, 1, 8, 2, 2]) == False
assert is_high_card([1, 9, 8, 3, 2]) == True


def generate_all_permutations(hand: list[int]) -> list[list[int]]:
    joker_count = hand.count(JOKER)
    possible_joker_usage = [
        list(t) for t in product(ALL_CARDS_BESIDES_JOKER, repeat=joker_count)
    ]
    # This is some magic to keep the same order
    return [
        [c if c != JOKER else jokers.pop() for c in hand]
        for jokers in possible_joker_usage
    ]


assert generate_all_permutations([1, 1, 1, JOKER, 1]) == [
    [1, 1, 1, 14, 1],
    [1, 1, 1, 13, 1],
    [1, 1, 1, 12, 1],
    [1, 1, 1, 10, 1],
    [1, 1, 1, 9, 1],
    [1, 1, 1, 8, 1],
    [1, 1, 1, 7, 1],
    [1, 1, 1, 6, 1],
    [1, 1, 1, 5, 1],
    [1, 1, 1, 4, 1],
    [1, 1, 1, 3, 1],
    [1, 1, 1, 2, 1],
]

assert [2, 2, 2, 2, 2] in generate_all_permutations([2, 2, 2, JOKER, JOKER])


def hand_a_stronger_than_hand_b(hand_a: list[int], hand_b: list[int]) -> bool:
    hand_a_permutations: list[list[int]] = []
    hand_b_permutations: list[list[int]] = []
    for is_strongest_hand in [
        is_five_of_a_kind,
        is_four_of_a_kind,
        is_full_house,
        is_three_of_a_kind,
        is_two_pair,
        is_one_pair,
        is_high_card,
    ]:
        if hand_a.count(JOKER) >= 4:
            # In case of 4 or 5 jokers, hand A will be 5 of a kind,
            # and the loop will for sure end this iteration.
            hand_a_is_this_hand = True
        else:
            if not hand_a_permutations:
                hand_a_permutations = generate_all_permutations(hand_a)
            hand_a_is_this_hand = any(
                [is_strongest_hand(hand) for hand in hand_a_permutations]
            )

        if hand_b.count(JOKER) >= 4:
            hand_b_is_this_hand = True
        else:
            if not hand_b_permutations:
                hand_b_permutations = generate_all_permutations(hand_b)
            hand_b_is_this_hand = any(
                [is_strongest_hand(hand) for hand in hand_b_permutations]
            )
        if hand_a_is_this_hand and not hand_b_is_this_hand:
            return True
        elif not hand_a_is_this_hand and hand_b_is_this_hand:
            return False
        elif not hand_a_is_this_hand and not hand_b_is_this_hand:
            # neither is the strongest hand currently
            continue
        # both are same strongest hand, go through hands left to right
        for card_a, card_b in zip(hand_a, hand_b):
            if card_a > card_b:
                return True
            elif card_a < card_b:
                return False
        raise ValueError("Getting here should be impossible")
    raise ValueError("Getting here should be impossible 2")


assert hand_a_stronger_than_hand_b([1, 1, 1, 1, 1], [1, 2, 5, 2, 8]) == True
assert hand_a_stronger_than_hand_b([2, 2, 2, 2, 2], [1, 1, 1, 1, 1]) == True
assert hand_a_stronger_than_hand_b([3, 3, 3, 8, 8], [1, 1, 1, 1, 5]) == False


assert hand_a_stronger_than_hand_b(get_cards("KK677"), get_cards("32T3K"))
assert hand_a_stronger_than_hand_b(get_cards("T55J5"), get_cards("32T3K"))
assert hand_a_stronger_than_hand_b(get_cards("QQQJA"), get_cards("32T3K"))
assert hand_a_stronger_than_hand_b(get_cards("KTJJT"), get_cards("32T3K"))

assert hand_a_stronger_than_hand_b(get_cards("T55J5"), get_cards("KK677"))
assert hand_a_stronger_than_hand_b(get_cards("QQQJA"), get_cards("KK677"))
assert hand_a_stronger_than_hand_b(get_cards("KTJJT"), get_cards("KK677"))

assert hand_a_stronger_than_hand_b(get_cards("QQQJA"), get_cards("T55J5"))
assert hand_a_stronger_than_hand_b(get_cards("KTJJT"), get_cards("T55J5"))


@dataclass
class SortWrapper:
    hand: list[int]
    bid: int

    def __eq__(self, other):
        return (
            all([a == b for a, b in zip(self.hand, other.hand)])
            and self.bid == other.bid
        )

    def __lt__(self, other):
        return not hand_a_stronger_than_hand_b(self.hand, other.hand)


def sort_hands(wrappers: list[SortWrapper]) -> list[SortWrapper]:
    return sorted(wrappers)


assert hand_a_stronger_than_hand_b([1, 1, 1, 1, 1], [2, 2, 2, 2, 4])
assert sort_hands(
    [
        SortWrapper([1, 1, 1, 1, 1], 5),
        SortWrapper([2, 2, 2, 2, 4], 10),
    ]
) == [
    SortWrapper([2, 2, 2, 2, 4], 10),
    SortWrapper([1, 1, 1, 1, 1], 5),
]


def get_answer(all_lines: list[str]) -> int:
    # we map cards to numbers, so A=14, K=13 etc.
    sort_wrappers: list[SortWrapper] = []

    for line in all_lines:
        if line == "\n":
            continue
        cards_part, bid_part = line.split(" ")
        bid = int(bid_part)
        hand = get_cards(cards_part)
        sort_wrappers.append(SortWrapper(hand, bid))

    sorted_wrappers = sort_hands(sort_wrappers)
    total_sum = 0
    for i, wrapper in enumerate(sorted_wrappers):
        rank = i + 1
        score = rank * wrapper.bid
        total_sum += score

    return total_sum
