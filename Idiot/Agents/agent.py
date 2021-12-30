"""
Format på input:

data = {
    hand_cards: [...],
    playable_cards: [...],
    table_cards: [...],
    pile: [...],
    played_cards: [...],
    burnt_cards: [...]
}
"""


class AbstractAgent:
    def __init__(self, name="AbstractAgent") -> None:
        self.output = "no play"  # SKal være indeksen til kortet som skal spilles
        self.name = name

    def process_input(self, data: dict) -> None:
        """Choose best play according to the policy"""
        pass

    def return_output(self) -> int:
        return self.output
