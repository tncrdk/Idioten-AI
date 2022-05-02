import import_files
import deck
import game_engine as ge
import static_agents as sa
import NEAT_agent as na
import os
import neat
import pickle
from numpy.random import randint
import copy

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
                winner, _ = game.run_game()
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
    def __init__(self, config_path, decks) -> None:
        super().__init__(config_path)
        self.decks = decks

    def eval_genomes(self, genomes, config):
        agents = [sa.PlayLowSaveAgent1()]
        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            agents.append(na.NEAT_Agent2(genome, network))
            neat_wins = 0
            games = 50
            tot_turns = 0

            for _ in range(games):
                custom_deck = copy.deepcopy(self.decks[randint(len(self.decks))])
                game = ge.AgentGame(
                    run_game=False,
                    agents=agents,
                    custom_deck=custom_deck,
                )
                winner, turns = game.run_game()
                tot_turns += turns
                if bool(winner) and winner.name == "NEAT_V2":
                    neat_wins += 1

            print("-" * 10)
            print(neat_wins / games)
            # print(agents[1].wrongs / games)
            print(tot_turns / games)
            agents[1].add_reward(
                (neat_wins * 100 / games) - (tot_turns / games) * 3 + 15
            )
            agents.pop()


class Training3(AbstractTraining):
    def __init__(self, config_path) -> None:
        super().__init__(config_path)

    def eval_genomes(self, genomes, config):
        agents = [sa.PlayLowSaveAgent1()]
        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            agents.append(na.NEAT_Agent2(genome, network))
            neat_wins = 0
            games = 100
            tot_turns = 0
            tot_games = 0

            for _ in range(games):
                game = ge.AgentGame(
                    run_game=False,
                    agents=agents,
                )
                winner, turns = game.run_game()
                tot_turns += turns
                tot_games += 1
                if bool(winner) and winner.name == "NEAT_V2":
                    neat_wins += 1

            avg_turns = tot_turns / tot_games
            avg_win = neat_wins / tot_games

            if avg_win >= 0.4:
                games *= 10
                for _ in range(games):
                    game = ge.AgentGame(
                        run_game=False,
                        agents=agents,
                    )
                    winner, turns = game.run_game()
                    tot_turns += turns
                    tot_games += 1
                    if bool(winner) and winner.name == "NEAT_V2":
                        neat_wins += 1
                avg_turns = tot_turns / tot_games
                avg_win = neat_wins / tot_games

            if avg_win >= 0.5:
                games *= 10
                for _ in range(games):
                    game = ge.AgentGame(
                        run_game=False,
                        agents=agents,
                    )
                    winner, turns = game.run_game()
                    tot_turns += turns
                    tot_games += 1
                    if bool(winner) and winner.name == "NEAT_V2":
                        neat_wins += 1
                avg_turns = tot_turns / tot_games
                avg_win = neat_wins / tot_games

            print("-" * 10)
            print(avg_win)
            print(avg_turns)

            if avg_turns <= 30:
                agents[1].add_reward(avg_win * 100)
            elif avg_turns <= 40:
                agents[1].add_reward((avg_win * 100) - (avg_turns) + 15)
            else:
                agents[1].add_reward((avg_win * 100) - (avg_turns) * 3 + 15)
            print(agents[1].get_fitness())

            agents.pop()


class Training4(AbstractTraining):
    def __init__(self, config_path) -> None:
        super().__init__(config_path)

    def eval_genomes(self, genomes, config):
        agents = [sa.PlayLowSaveAgent1()]
        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            agents.append(na.NEAT_Agent3(genome, network))
            neat_wins = 0
            games = 100
            tot_turns = 0
            tot_games = 0

            for _ in range(games):
                game = ge.AgentGame(
                    run_game=False,
                    agents=agents,
                )
                winner, turns = game.run_game()
                tot_turns += turns
                tot_games += 1
                if bool(winner) and winner.name == "NEAT_V2":
                    neat_wins += 1

            avg_turns = tot_turns / tot_games
            avg_win = neat_wins / tot_games

            if avg_win >= 0.4:
                games *= 10
                for _ in range(games):
                    game = ge.AgentGame(
                        run_game=False,
                        agents=agents,
                    )
                    winner, turns = game.run_game()
                    tot_turns += turns
                    tot_games += 1
                    if bool(winner) and winner.name == "NEAT_V2":
                        neat_wins += 1
                avg_turns = tot_turns / tot_games
                avg_win = neat_wins / tot_games

            if avg_win >= 0.5:
                games *= 10
                for _ in range(games):
                    game = ge.AgentGame(
                        run_game=False,
                        agents=agents,
                    )
                    winner, turns = game.run_game()
                    tot_turns += turns
                    tot_games += 1
                    if bool(winner) and winner.name == "NEAT_V2":
                        neat_wins += 1
                avg_turns = tot_turns / tot_games
                avg_win = neat_wins / tot_games

            print("-" * 10)
            print(avg_win)
            print(avg_turns)

            if avg_turns <= 40:
                agents[1].add_reward((avg_win * 100))
            else:
                agents[1].add_reward((avg_win * 100) - (avg_turns) * 3 + 15)
            print(agents[1].get_fitness())

            if agents[1].get_fitness() >= 51.5:
                with open("winner_temp51_5.pkl", "wb") as f:
                    pickle.dump(genome, f)
                    f.close()
            elif agents[1].get_fitness() >= 51:
                with open("winner_temp51.pkl", "wb") as f:
                    pickle.dump(genome, f)
                    f.close()
            elif agents[1].get_fitness() >= 50.5:
                with open("winner_temp50_5.pkl", "wb") as f:
                    pickle.dump(genome, f)
                    f.close()
            elif agents[1].get_fitness() >= 50:
                with open("winner_temp50.pkl", "wb") as f:
                    pickle.dump(genome, f)
                    f.close()
            elif agents[1].get_fitness() >= 49.5:
                with open("winner_temp49_5.pkl", "wb") as f:
                    pickle.dump(genome, f)
                    f.close()

            agents.pop()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, r"Config-files\config3.txt")

    file_name = "winner.pkl"
    decks = [deck.Deck() for _ in range(1000)]

    t = Training4(config_path)
    t.train(file_name)
