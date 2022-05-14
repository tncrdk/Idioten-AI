import import_files
import neat_training as nt
import NEAT_agent as na
import os


def main(config_file, NeatAgentClass, winners_dir_path, winner_file_name):
    training = nt.Training(config_file, NeatAgentClass, winners_dir_path)
    training.train(winner_file_name)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    winners_dir_path = os.path.join(local_dir, "Winners")
    config_file_path = os.path.join(local_dir, "Config-files\config3.txt")
    winner_file_name = "winner.pkl"

    main(config_file_path, na.NEAT_Agent3, winners_dir_path, winner_file_name)
