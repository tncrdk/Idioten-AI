from agent import AbstractAgent
import import_files
import game_engine as ge
import static_agents as sa
import NEAT_agent as na
import neat
import pickle


class DataGenerator:
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

    def run_games(self, games: int, players: list[AbstractAgent]) -> dict:
        for player in players:
            player.wins = 0

        for _ in range(games):
            game = ge.AgentGame(agents=players, run_game=False, log_game=True)
            winner, _ = game.run_game()
            if winner:
                winner.wins += 1

        return_value = {
            player.name: {"wins": player.wins, "games": games} for player in players
        }
        return return_value

    def run_groups(self, players, groups, group_size, save_path):
        results = {player.name: {"wins": 0, "games": 0} for player in players}

        for _ in range(groups):
            result = self.run_games(group_size, players)
            self.log_result(save_path, result)
            for player_name, data in result.items():
                results[player_name]["wins"] += data["wins"]
                results[player_name]["games"] += data["games"]

        self.print_results(results)

    def run_neat_first(self, groups, group_size):
        neat_agent = self.create_NEAT_agent(self.config_path, self.genome_path)
        static_agent = sa.PlayLowSaveAgent1()
        agents = [neat_agent, static_agent]
        SAVE_PATH = r".\Log\log_neat_first_results.txt"
        self.run_groups(agents, groups, group_size, SAVE_PATH)

    def run_static_first(self, groups, group_size):
        neat_agent = self.create_NEAT_agent(self.config_path, self.genome_path)
        static_agent = sa.PlayLowSaveAgent1()
        agents = [static_agent, neat_agent]
        SAVE_PATH = r".\Log\log_static_first_results.txt"
        self.run_groups(agents, groups, group_size, SAVE_PATH)

    def log_result(self, file_path, result):
        with open(file_path, "a") as f:
            f.write(str(result))
            f.write("\n")

    def print_results(self, results: dict):
        for player_name, data in results.items():
            print(f'{player_name}: {data.get("wins") / data.get("games")}')
