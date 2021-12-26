import agent
import neat

""" Input layer:    hand                                            pile?
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, ||(, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,) must_play, top_pile_value]

    Output:
    [int, bool]
"""


class AbstractNEAT_Agent(agent.AbstractAgent):
    def __init__(self, genome, network, name="NEAT_V1") -> None:
        super().__init__(name=name)
        self.genome = genome
        self.network = network

    def process_input(self, data: dict) -> None:
        pass
