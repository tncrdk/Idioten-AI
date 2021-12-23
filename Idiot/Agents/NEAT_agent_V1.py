import agent
import neat


class NEAT_Agent(agent.AbstractAgent):
    def __init__(self, name="NEAT_V1") -> None:
        super().__init__(name=name)

    def process_input(self, data: dict) -> None:
        pass
