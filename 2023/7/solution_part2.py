from dataclasses import dataclass

JOKER = -1


def get_cards(line: str) -> list[int]:
    cards_as_strings = [c for c in line]
    strength_map = {"A": 14, "K": 13, "Q": 12, "J": JOKER, "T": 10}
    return [int(strength_map.get(c, c)) for c in cards_as_strings]


def is_five_of_a_kind(hand: list[int]) -> bool:
    joker_count = hand.count(JOKER)
    if joker_count == 5:
        return True
    for card in set(hand):
        if card == JOKER:
            continue
        if (hand.count(card) + joker_count) == 5:
            return True
    return False


def is_four_of_a_kind(hand: list[int]) -> bool:
    joker_count = hand.count(JOKER)
    if joker_count == 4:
        return True
    for card in set(hand):
        if card == JOKER:
            continue
        if (hand.count(card) + joker_count) >= 4:
            return True
    return False


def is_full_house(hand: list[int]) -> bool:
    if is_four_of_a_kind(hand):
        return False
    joker_count = hand.count(JOKER)
    if joker_count >= 3:
        # 3 jokers + always makes fullhouse
        return True

    counts = []
    for card in set(hand):
        if card == JOKER:
            continue
        counts.append(hand.count(card))

    sorted_counts = sorted(counts)
    if joker_count == 2:
        return sorted_counts in ([1, 2], [3])

    if joker_count == 1:
        # again, always 4 of kind here
        return sorted_counts in ([1, 1, 2], [2, 2])

    # 4 and 5 of kind are stronger so already covered
    return len(set(hand)) == 2


# This always gets caught by higher hands anyways
# basically no fullhouse exists with 2 jokers as any fullhouse could better be 4 of a kind


def is_three_of_a_kind(hand: list[int]) -> bool:
    joker_count = hand.count(JOKER)
    if joker_count >= 2:
        # 2 jokers + always makes three of a kind or higher
        return True

    counts = []
    for card in set(hand):
        if card == JOKER:
            continue
        counts.append(hand.count(card))

    if joker_count == 1:
        return 2 in set(counts)

    return 3 in set(counts)


def is_two_pair(hand: list[int]) -> bool:
    joker_count = hand.count(JOKER)
    if joker_count >= 2:
        return True

    counts = []
    for card in set(hand):
        if card == JOKER:
            continue
        counts.append(hand.count(card))

    sorted_counts = sorted(counts)
    if joker_count == 1:
        return min(counts) >= 2

    number_of_pairs = 0
    for card in set(hand):
        if hand.count(card) == 2:
            number_of_pairs += 1
    return number_of_pairs == 2


def is_one_pair(hand: list[int]) -> bool:
    if JOKER in hand:
        return True
    number_of_pairs = 0
    counts = set()
    for card in set(hand):
        c = hand.count(card)
        if c == 2:
            number_of_pairs += 1
        counts.add(c)
    return number_of_pairs == 1 and counts == {1, 2}


def is_high_card(hand: list[int]) -> bool:
    if JOKER in hand:
        return True
    return len(set(hand)) == 5


def hand_a_stronger_than_hand_b(hand_a: list[int], hand_b: list[int]) -> bool:
    for is_strongest_hand in [
        is_five_of_a_kind,
        is_four_of_a_kind,
        is_full_house,
        is_three_of_a_kind,
        is_two_pair,
        is_one_pair,
        is_high_card,
    ]:
        if is_strongest_hand(hand_a) and not is_strongest_hand(hand_b):
            return True
        elif not is_strongest_hand(hand_a) and is_strongest_hand(hand_b):
            return False
        elif not is_strongest_hand(hand_a) and not is_strongest_hand(hand_b):
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
