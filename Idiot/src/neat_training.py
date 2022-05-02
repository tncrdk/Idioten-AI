from copyreg import pickle
import neat

class Training:
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

    def save_AI(self, AI, save_file_path):
        with open(save_file_path, "wb") as f:
            pickle.dump(AI, f)
            f.close()