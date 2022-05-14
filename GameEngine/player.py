import agent_path
import deck
import agent


class AbstractPlayer:
    def __init__(self, name="x") -> None:
        self.name = name
        self.table_hidden = []
        self.hand = []
        self.table_visible = []
        self.finished = False
        self.is_agent = False

    def check_if_finished(self) -> bool:
        if not (self.hand or self.table_visible or self.table_hidden):
            self.finished = True
        return self.finished

    def get_hand_card(self, index: int) -> deck.Card:
        return self.hand[index]

    def get_hand_index(self, card: deck.Card) -> int:
        return self.hand.index(card)

    def play_hand_card(self, index: int) -> deck.Card:
        card = self.hand.pop(index)
        return card

    def sort_hand(self) -> None:
        self.hand.sort()


class Player(AbstractPlayer):
    def __init__(self, name="x") -> None:
        super().__init__(name=name)

    def show_hand(self) -> None:
        print("-" * 20)
        print(f"Player name: {self.name}")
        print("Hand cards")
        print("-" * 20)
        for index, card in enumerate(self.hand):
            print(f"Index: {index}", end="\n    ")
            card.show_card()
        print("-" * 20)

    def show_visible_table_cards(self) -> None:
        print("-" * 20)
        print(f"Table cards")
        print("-" * 20)
        for index, card in enumerate(self.table_visible):
            print(f"Index: {index}", end="\n    ")
            card.show_card()
        print("-" * 20)


class AgentPlayer(AbstractPlayer):
    def __init__(self, agent: agent.AbstractAgent, name="x") -> None:
        super().__init__(name=name)
        self.policy = agent


if __name__ == "__main__":
    p1 = Player()
