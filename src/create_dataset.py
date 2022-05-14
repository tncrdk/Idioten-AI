import data_generator as dg


def main():
    GENOME_PATH = r".\Winners\winner.pkl"
    CONFIG_PATH = r".\Config-files\config3.txt"
    GROUPS = 100
    GROUP_SIZE = 1000

    generator = dg.DataGenerator(CONFIG_PATH, GENOME_PATH)
    generator.run_neat_first(GROUPS, GROUP_SIZE)


if __name__ == "__main__":
    main()
