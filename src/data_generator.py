import import_files
import agent
import game_engine as ge
import static_agents as sa
import NEAT_agent as na
import neat
import pickle


class DataGenerator:
    def __init__(self, config_path, genome_path) -> None:
        self.config_path = config_path
        self.genome_path = genome_path
        self.GROUP_SIZE = 1000

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

    def run_games(self, games: int, players: list[agent.AbstractAgent]) -> dict:
        for player in players:
            player.wins = 0

        for _ in range(games):
            game = ge.AgentGame(agents=players, run_game=False, log_game=False)
            winner, _ = game.run_game()
            if winner:
                winner.wins += 1

        return_value = {
            player.name: {"wins": player.wins, "games": games} for player in players
        }
        return return_value

    def run_groups(self, players: list, groups: int, save_path):
        results = {player.name: {"wins": 0, "games": 0} for player in players}

        for _ in range(groups):
            result = self.run_games(self.GROUP_SIZE, players)
            self.log_result(save_path, result)
            for player_name, data in result.items():
                results[player_name]["wins"] += data["wins"]
                results[player_name]["games"] += data["games"]

        self.print_results(results)

    def run_neat_first(self, groups: int, static_agent):
        neat_agent = self.create_NEAT_agent(self.config_path, self.genome_path)
        agents = [neat_agent, static_agent]
        SAVE_PATH = r".\Log\log_NEAT_vs_{}.txt".format(static_agent.name)
        self.run_groups(agents, groups, SAVE_PATH)

    def run_static_first(self, groups: int, static_agent):
        neat_agent = self.create_NEAT_agent(self.config_path, self.genome_path)
        agents = [static_agent, neat_agent]
        SAVE_PATH = r".\Log\log_{}_vs_NEAT.txt".format(static_agent.name)
        self.run_groups(agents, groups, SAVE_PATH)

    def run_identical_static_agents(self, groups: int):
        static_agent_1 = sa.PlayLowSaveAgent("First")
        static_agent_2 = sa.PlayLowSaveAgent("Second")
        agents = [static_agent_1, static_agent_2]
        SAVE_PATH = r".\Log\log_id_PlaylowSaving.txt"
        self.run_groups(agents, groups, SAVE_PATH)

    def log_result(self, file_path, result):
        with open(file_path, "a") as f:
            f.write(str(result))
            f.write("\n")

    def print_results(self, results: dict):
        for player_name, data in results.items():
            print(f'{player_name}: {data.get("wins") / data.get("games")}')


if __name__ == "__main__":
    GENOME_PATH = r".\Winners\winner.pkl"
    CONFIG_PATH = r".\Config-files\config3.txt"
    GROUPS = 300
    static_agent = sa.PlayLowAgent()

    generator = DataGenerator(CONFIG_PATH, GENOME_PATH)
    generator.run_neat_first(GROUPS, static_agent)
