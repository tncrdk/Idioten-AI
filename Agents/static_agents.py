import agent
from numpy.random import randint

"""
Format på input:

data = {
    "hand_cards": [...],
    "playable_cards": [...],
    "table_cards": [...],
    "pile: [...]",
    "played_cards": [...],
    "burnt_cards": [...],
    "must_play": False
}
"""


class PlayLowAgent(agent.AbstractAgent):
    def __init__(self, name="PlayLow") -> None:
        super().__init__(name)

    def process_input(self, data: dict) -> None:
        playable_cards = data.get("playable_cards")
        if bool(playable_cards):
            self.output = self.get_smallest_card(playable_cards)

    def get_smallest_card(self, playable_cards) -> int:
        smallest_card = 15
        for index, card in playable_cards:
            if card.value < smallest_card:
                smallest_card = card
                smallest_card_index = index

        return smallest_card_index, smallest_card


class PlayLowSaveAgent(agent.AbstractAgent):
    def __init__(self, name="PlayLowSaving") -> None:
        super().__init__(name)
        self.prior_hand = None

    def process_input(self, data: dict) -> None:
        playable_cards = data["playable_cards"]
        must_play = data["must_play"]
        if playable_cards:
            chosen_index, chosen_card = self.choose_card(playable_cards, must_play)
            if chosen_index != None:
                self.output = (chosen_index, chosen_card)
            else:
                self.output = (None, None)

    def choose_card(self, playable_cards: list, must_play) -> int:
        cards_sorted = sorted(playable_cards, key=lambda x: x[1])
        if must_play:
            for index, card in cards_sorted:
                if card.value not in {2, 10}:
                    return index, card
            return cards_sorted[0]

        for index, card in cards_sorted:
            if card.value not in {2, 10}:
                return index, card

        if len(cards_sorted) > 1:
            return cards_sorted[0]


class PlayHighAgent(agent.AbstractAgent):
    def __init__(self, name="PlayHigh") -> None:
        super().__init__(name)

    def process_input(self, data: dict) -> None:
        playable_cards = data.get("playable_cards")
        if bool(playable_cards):
            self.output = self.get_highest_card(playable_cards)

    def get_highest_card(self, playable_cards):
        highest_card = 0
        for index, card in playable_cards:
            if card.value > highest_card:
                highest_card = card
                highest_card_index = index

        return highest_card_index, highest_card


class RandomAgent(agent.AbstractAgent):
    def __init__(self, name="Random") -> None:
        super().__init__(name=name)

    def process_input(self, data: dict) -> None:
        playable_cards = data["playable_cards"]
        length = len(playable_cards)
        rand_index = randint(0, length)
        self.output = playable_cards[rand_index]


if __name__ == "__main__":
    data = {"playable_cards": [(0, 8), (1, 8), (2, 8), (3, 9), (4, 9), (5, 9)]}
    a = RandomAgent()
    a.process_input(data)
    print(a.return_output())
