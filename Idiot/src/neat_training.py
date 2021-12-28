import import_files
import game_engine as ge
import static_agents as sa
import NEAT_agent as na
import time
import os
import neat

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


def eval_genomes(genomes, config):
    agents = [sa.RandomAgent()]
    for _, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        agents.append(na.NEAT_Agent1(genome, network))

        for _ in range(10):
            game = ge.AgentGame(run_game=False, agents=agents)
            winner = game.run_game()
            if bool(winner) and winner.name == "NEAT_V1":
                winner.add_reward(100)

        print(agents[1].wrongs)
        agents.pop()


def main(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    winner = population.run(eval_genomes)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, r"Config-files\config.txt")
    main(config_path)
