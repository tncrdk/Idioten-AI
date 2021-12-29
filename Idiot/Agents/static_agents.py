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


class PlayLowAgent1(agent.AbstractAgent):
    def __init__(self, name="PlayLow1") -> None:
        super().__init__(name)

    def process_input(self, data: dict) -> None:
        playable_cards = data.get("playable_cards")
        if bool(playable_cards):
            self.output = (self.get_smallest_card(playable_cards), None, True)

    def get_smallest_card(self, playable_cards) -> int:
        smallest_card = 15
        for index, card in playable_cards:
            if card.value < smallest_card:
                smallest_card = card
                smallest_card_index = index

        return smallest_card_index


class PlayLowSaveAgent1(agent.AbstractAgent):
    def __init__(self, name="PlayLowSaving") -> None:
        super().__init__(name)
        self.prior_hand = None

    def process_input(self, data: dict) -> None:
        playable_cards = data["playable_cards"]
        must_play = data["must_play"]
        if bool(playable_cards):
            output = self.choose_card(playable_cards, must_play)
            if output != None:
                self.output = (output, None, True)
            else:
                self.output = ("n", None, True)

    def choose_card(self, playable_cards, must_play) -> int:
        cards_sorted = sorted([(card, index) for index, card in playable_cards])
        if must_play:
            for card, index in cards_sorted:
                if card.value not in {2, 10}:
                    return index
            return cards_sorted[0][1]

        for card, index in cards_sorted:
            if card.value not in {2, 10}:
                return index

        if len(cards_sorted) > 1:
            return cards_sorted[0][1]


class PlayHighAgent1(agent.AbstractAgent):
    def __init__(self, name="PlayHigh1") -> None:
        super().__init__(name)

    def process_input(self, data: dict) -> None:
        playable_cards = data.get("playable_cards")
        if bool(playable_cards):
            self.output = (self.get_highest_card(playable_cards), None, True)

    def get_highest_card(self, playable_cards):
        highest_card = 0
        for index, card in playable_cards:
            if card.value > highest_card:
                highest_card = card
                highest_card_index = index

        return highest_card_index


class RandomAgent(agent.AbstractAgent):
    def __init__(self, name="Random") -> None:
        super().__init__(name=name)

    def process_input(self, data: dict) -> None:
        playable_cards = data["playable_cards"]
        length = len(playable_cards)
        rand_index = randint(0, length)
        self.output = (playable_cards[rand_index][0], None, True)


if __name__ == "__main__":
    data = {"playable_cards": [(0, 8), (1, 8), (2, 8), (3, 9), (4, 9), (5, 9)]}
    a = RandomAgent()
    a.process_input(data)
    print(a.return_output())
