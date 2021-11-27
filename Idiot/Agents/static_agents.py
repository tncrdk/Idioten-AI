import agent

"""
Format på input:

data = {
    "hand_cards": [...],
    "playable_cards": [...],
    "table_cards": [...],
    "pile: [...]",
    "played_cards": [...],
    "burnt_cards": [...]
}
"""


class PlayLowAgent1(agent.AbstractAgent):
    def __init__(self) -> None:
        super().__init__()

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

        return smallest_card_index


class PlayHighAgent1(agent.AbstractAgent):
    def __init__(self) -> None:
        super().__init__()

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

        return highest_card_index


if __name__ == "__main__":
    a = PlayLowAgent1()
