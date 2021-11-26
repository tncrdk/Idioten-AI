import agent
import static_policy as sp


class StaticAgent(agent.AbstractAgent):
    def __init__(self, policy) -> None:
        super().__init__()
        self.policy = sp.policies.get(policy)
