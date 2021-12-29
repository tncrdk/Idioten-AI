import import_files
import game_engine as ge
import static_agents as sa
import NEAT_agent as na
import os
import neat
import pickle

from turn import AgentTurn

"""
data = {
    "hand_cards": [...],
    "playable_cards": [...],
    "table_cards": [...],
    "pile": [...],
    "played_cards": [...],
    "burnt_cards": [...],
}
"""


class AbstractTraining:
    def __init__(self, config_path) -> None:
        self.config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path,
        )

        self.population = neat.Population(self.config)
        self.population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.population.add_reporter(stats)

    def train(self, save_file_name):
        winner = self.population.run(self.eval_genomes)

        with open(save_file_name, "wb") as f:
            pickle.dump(winner, f)
            f.close()

    def eval_genomes(self, genomes, config):
        pass


class Training1(AbstractTraining):
    def __init__(self, config_path) -> None:
        super().__init__(config_path)

    def eval_genomes(self, genomes, config):
        agents = [sa.PlayLowAgent1()]
        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            agents.append(na.NEAT_Agent1(genome, network))
            neat_wins = 0
            games = 50
            for _ in range(games):
                game = ge.AgentGame(run_game=False, agents=agents)
                winner = game.run_game()
                if bool(winner) and winner.name == "NEAT_V1":
                    neat_wins += 1

            print("-" * 10)
            print(neat_wins / games)
            print(agents[1].wrongs / games)
            agents[1].add_reward(
                (neat_wins * 1000 / games) - (agents[1].wrongs / (10 * games))
            )
            agents.pop()


class Training2(AbstractTraining):
    def __init__(self, config_path) -> None:
        super().__init__(config_path)

    def eval_genomes(self, genomes, config):
        agents = [sa.PlayLowAgent1()]
        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            agents.append(na.NEAT_Agent2(genome, network))
            neat_wins = 0
            games = 50
            for _ in range(games):
                game = ge.AgentGame(run_game=False, agents=agents)
                winner = game.run_game()
                if bool(winner) and winner.name == "NEAT_V2":
                    neat_wins += 1

            print("-" * 10)
            print(neat_wins / games)
            # print(agents[1].wrongs / games)
            print(agents[1].turns / games)
            agents[1].add_reward(
                (neat_wins * 100 / games) - (agents[1].turns / games) / 1000
            )
            # agents[1].add_reward(neat_wins * 100 / games)
            agents.pop()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, r"Config-files\config2.txt")

    file_name = "winner2.pkl"

    t = Training2(config_path)
    t.train(file_name)
