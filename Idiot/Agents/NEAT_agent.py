import agent
import neat
import math

""" Input layer:    hand                                            pile?
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, ||(, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,) must_play, top_pile_value]

    Output:
    [chosen_card_value, will_play]
"""

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


class AbstractNEAT_Agent(agent.AbstractAgent):
    def __init__(
        self, genome, network: neat.nn.FeedForwardNetwork, name="AbstractNEAT"
    ) -> None:
        super().__init__(name=name)
        self.genome = genome
        self.network = network

    def process_input(self, data: dict) -> None:
        """Output-format = (output, {index: 0, card: 1})"""
        input_data = self.format_data(data)
        output_data = self.network.activate(input_data)
        if output_data[1] > 0.5:
            self.output = ("n", True)
        else:
            chosen_card = math.floor(output_data[0])
            self.output = (chosen_card, False)

    def add_reward(self, reward: int) -> None:
        self.genome += reward

    def format_data(self, data: dict) -> tuple:
        pass


class NEAT_Agent1(AbstractNEAT_Agent):
    def __init__(
        self, genome, network: neat.nn.FeedForwardNetwork, name="NEAT_V1"
    ) -> None:
        super().__init__(genome, network, name=name)

    def format_data(self, data: dict):
        player_hand = data["hand"]
        input_data = [0 for i in range(13)]

        for card in player_hand:
            input_data[card.value - 2] += 1

        must_play = 1 if data["must_play"] else 0
        pile_card = data["pile"].get_top_card()
        input_data += [must_play, pile_card]

        return input_data
