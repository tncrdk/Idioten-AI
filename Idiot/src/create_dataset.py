import import_files
import data_generator as dg


def main(config_path, genome_path, games):
    generator = dg.DataGenerator(config_path, genome_path)
    generator.run_neat_first(10)


if __name__ == "__main__":
    GENOME_PATH = r".\Winners\winner.pkl"
    CONFIG_PATH = r".\Config-files\config3.txt"
    GAMES = 100

    main(CONFIG_PATH, GENOME_PATH, GAMES)
