import agent
import neat
import math

from deck import Card

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
        pass

    def get_fitness(self):
        return self.genome.fitness

    def add_reward(self, reward: int) -> None:
        self.genome.fitness += reward

    def format_data(self, data: dict) -> tuple:
        pass


class NEAT_Agent1(AbstractNEAT_Agent):
    def __init__(
        self, genome, network: neat.nn.FeedForwardNetwork, name="NEAT_V1"
    ) -> None:
        super().__init__(genome, network, name=name)

    def process_input(self, data: dict) -> None:
        """Output-format = (output, is_index?, safe?)"""
        input_data = self.format_data(data)
        output_data = self.network.activate(input_data)
        if output_data[1] < 1:
            self.output = ("n", None, True)
        else:
            chosen_card_value = math.floor(self.translate(output_data[0]))
            self.output = (None, chosen_card_value, False)

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

    def translate(self, value):
        return 2 + ((value + 1) * 12 / 2)


class NEAT_Agent2(AbstractNEAT_Agent):
    def __init__(
        self, genome, network: neat.nn.FeedForwardNetwork, name="NEAT_V2"
    ) -> None:
        super().__init__(genome, network, name=name)

    def process_input(self, data: dict) -> None:
        """Output-format = (output: card, is_index?, safe?) (card, False, True)"""
        input_data = self.format_data(data)
        output_data = self.network.activate(input_data)
        if output_data[-1] > 0.5 and not data["must_play"]:
            self.output = ("n", None, True)
        else:
            output_data.pop()
            playable_cards = data["playable_cards"]
            chosen_card_value, chosen_index = self.choose_card(
                output_data, playable_cards
            )
            self.output = (chosen_index, chosen_card_value, True)

    def format_data(self, data: dict) -> tuple:
        player_hand = data["hand_cards"]
        formatted_data = [0 for i in range(13)]
        must_play = 0
        pile_card = 0

        for card in player_hand:
            formatted_data[card.value - 2] += 1

        formatted_data = [self.transform_input(value) for value in formatted_data]

        if data["must_play"]:
            must_play = 1
        if bool(data["pile"]):
            pile_card = data["pile"].get_top_card().value

        formatted_data += [must_play, pile_card]

        return formatted_data

    def choose_card(self, output_data: list, playable_cards: list):
        data = [(value, index) for index, value in enumerate(output_data)]
        data.sort(reverse=True)

        for _, index in data:
            for i, card in playable_cards:
                if index + 2 == card.value:
                    return card, i

    def transform_input(self, data):
        return data / 2 - 1


class NEAT_Agent3(AbstractNEAT_Agent):
    def __init__(
        self, genome, network: neat.nn.FeedForwardNetwork, name="NEAT_V2"
    ) -> None:
        super().__init__(genome, network, name=name)

    def process_input(self, data: dict) -> None:
        """Output-format = (output: card, is_index?, safe?) (card, False, True)"""
        input_data = self.format_data(data)
        output_data = self.network.activate(input_data)
        if output_data[-1] > 0.5 and not data["must_play"]:
            self.output = ("n", None, True)
        else:
            output_data.pop()
            playable_cards = data["playable_cards"]
            chosen_card_value, chosen_index = self.choose_card(
                output_data, playable_cards
            )
            self.output = (chosen_index, chosen_card_value, True)

    def format_data(self, data: dict) -> tuple:
        player_hand = data["hand_cards"]
        burnt_cards = data["burnt_cards"]
        pile = data["pile"]
        formatted_hand_cards = [0 for _ in range(13)]
        formatted_burnt_cards = [0 for _ in range(13)]
        formatted_pile = [0 for _ in range(13)]
        must_play = 0
        top_pile_card = 0

        for card in player_hand:
            formatted_hand_cards[card.value - 2] += 1

        for card in burnt_cards:
            formatted_burnt_cards[card.value - 2] += 1

        for card in pile:
            formatted_pile[card.value - 2] += 1

        formatted_data = formatted_hand_cards + formatted_pile + formatted_burnt_cards
        formatted_data = [self.transform_input(value) for value in formatted_data]

        if data["must_play"]:
            must_play = 1
        if bool(data["pile"]):
            top_pile_card = data["pile"].get_top_card().value

        formatted_data += [must_play, top_pile_card]

        return formatted_data

    def choose_card(self, output_data: list, playable_cards: list):
        data = [(value, index) for index, value in enumerate(output_data)]
        data.sort(reverse=True)

        for _, index in data:
            for i, card in playable_cards:
                if index + 2 == card.value:
                    return card, i

    def transform_input(self, data):
        return data / 2 - 1
