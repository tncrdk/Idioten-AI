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
        self.genome.fitness = 0
        self.wrongs = 0

    def process_input(self, data: dict) -> None:
        """Output-format = (output, safe?)"""
        input_data = self.format_data(data)
        output_data = self.network.activate(input_data)
        if output_data[1] < 1:
            self.output = ("n", True)
        else:
            chosen_card_value = math.ceil(output_data[0])
            self.output = (chosen_card_value, False)

    def add_reward(self, reward: int) -> None:
        self.genome.fitness += reward

    def format_data(self, data: dict) -> tuple:
        pass


class NEAT_Agent1(AbstractNEAT_Agent):
    def __init__(
        self, genome, network: neat.nn.FeedForwardNetwork, name="NEAT_V1"
    ) -> None:
        super().__init__(genome, network, name=name)

    def format_data(self, data: dict) -> list:
        player_hand = data["hand_cards"]
        formatted_data = [0 for i in range(13)]
        must_play = 0
        pile_card = 0

        for card in player_hand:
            formatted_data[card.value - 2] += 1

        if data["must_play"]:
            must_play = 1
        if bool(data["pile"]):
            pile_card = data["pile"].get_top_card().value

        formatted_data += [must_play, pile_card]

        return formatted_data
