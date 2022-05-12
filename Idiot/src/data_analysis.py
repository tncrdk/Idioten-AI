import import_files
import game_engine as ge
import static_agents as sa
import NEAT_agent as na
import neat
import pickle


class DataAnalysis:
    def __init__(self, config_path, genome_path) -> None:
        self.config_path = config_path
        self.genome_path = genome_path

    def create_NEAT_agent(self, config_path, genome_path) -> na.NEAT_Agent3:
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path,
        )

        with open(genome_path, "rb") as f:
            genome = pickle.load(f)

        network = neat.nn.FeedForwardNetwork.create(genome, config)
        neat_agent = na.NEAT_Agent3(genome, network)
        return neat_agent

    def run_games(self, games: int, players: list) -> list[dict]:
        for player in players:
            player.wins = 0

        for _ in range(games):
            game = ge.AgentGame(agents=players, run_game=False, log_game=True)
            winner, _ = game.run_game()
            if winner:
                winner.wins += 1

        return_value = [
            {"name": player.name, "winrate": player.wins / games} for player in players
        ]
        return return_value

    def run_neat_first(self, games):
        neat_agent = self.create_NEAT_agent(self.config_path, self.genome_path)
        static_agent = sa.PlayLowSaveAgent1()

        agents = [neat_agent, static_agent]
        stats = self.run_games(games, agents)

        for stat in stats:
            print(f'{stat.get("name")}: {stat.get("winrate")}')

    def run_static_first(self, games):
        neat_agent = self.create_NEAT_agent(self.config_path, self.genome_path)
        static_agent = sa.PlayLowSaveAgent1()

        agents = [static_agent, neat_agent]
        stats = self.run_games(games, agents)

        for stat in stats:
            print(f'{stat.get("name")}: {stat.get("winrate")}')


if __name__ == "__main__":
    GENOME_PATH = r"Winners\winner.pkl"
    CONFIG_PATH = r"Config-files\config3.txt"

    analyzer = DataAnalysis(CONFIG_PATH, GENOME_PATH)
    analyzer.run_neat_first(1000)
