import import_files
import neat
import pickle
import game_engine as ge
import NEAT_agent as na
import static_agents as sa
import os


def main(config_path, genome_path):
    neat_agent = create_neat_agent(config_path, genome_path)
    play_low_save_agent = sa.PlayLowSaveAgent1()
    agents = [neat_agent, play_low_save_agent]

    game = ge.AgentGame(run_game=False, agents=agents, log_game=True)
    winner, turns_played = game.run_game()


def create_neat_agent(config_path, genome_path):
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
    agent = na.NEAT_Agent3(genome, network)
    return agent


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    winners_dir_path = os.path.join(local_dir, "Winners")
    config_file_path = os.path.join(local_dir, "Config-files\config3.txt")
    winner_file_name = "winner.pkl"

    main(config_file_path, winner_file_name)
