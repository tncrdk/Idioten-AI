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
    def __init__(self) -> None:
        self.output = None

    def process_input(self) -> None:
        """Choose best play according to the policy"""
        pass

    def return_output(self) -> int:
        return self.output
