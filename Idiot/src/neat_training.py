import import_files
import pickle
import os
import neat
import static_agents as sa
import game_engine as ge
import glob


class Training:
    def __init__(self, config_path, NeatAgentClass, winners_dir_path) -> None:
        self.NeatAgentClass = NeatAgentClass
        self.winners_dir_path = winners_dir_path
        self.checkpoints_dir_path = os.path.join(
            os.path.dirname(__file__), "Checkpoints"
        )

        self.config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path,
        )
        if os.listdir(self.checkpoints_dir_path):
            list_of_files = glob.glob(os.path.join(self.checkpoints_dir_path, "*"))
            latest_file = max(list_of_files, key=os.path.getctime)
            self.population = neat.Checkpointer.restore_checkpoint(latest_file)
        else:
            self.population = neat.Population(self.config)

        self.population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.population.add_reporter(stats)
        self.population.add_reporter(
            neat.Checkpointer(
                10,
                filename_prefix=os.path.join(self.checkpoints_dir_path, "checkpoint-"),
            )
        )

        self.tot_games_played = 0
        self.tot_rounds_played = 0
        self.best_fitness = 0

    def train(self, save_file_name):
        winner_genome = self.population.run(self.eval_genomes)
        self.save_genome(winner_genome, save_file_name)

    def eval_genomes(self, genomes: neat.DefaultGenome, config: neat.Config):
        agents = [sa.PlayLowSaveAgent1()]
        for _, genome in genomes:
            self.tot_games_played = 0
            self.tot_rounds_played = 0
            GAMES_TO_PLAY = 100

            network = neat.nn.FeedForwardNetwork.create(genome, config)
            neat_agent = self.NeatAgentClass(genome, network)
            agents.append(neat_agent)

            avg_neat_win_rate, avg_rounds = self.play_games(
                GAMES_TO_PLAY, agents, neat_agent
            )

            if avg_neat_win_rate >= 0.4:
                avg_neat_win_rate, avg_rounds = self.play_games(
                    GAMES_TO_PLAY * 10, agents, neat_agent
                )

            if avg_neat_win_rate >= 0.5:
                avg_neat_win_rate, avg_rounds = self.play_games(
                    GAMES_TO_PLAY * 10, agents, neat_agent
                )

            print("-" * 10)
            print(avg_neat_win_rate)
            print(avg_rounds)

            if avg_rounds <= 40:
                neat_agent.add_reward((avg_neat_win_rate * 100))
            else:
                neat_agent.add_reward((avg_neat_win_rate * 100) - (avg_rounds) * 3 + 15)
            neat_fitness = agents[1].get_fitness()
            print(neat_fitness)

            if neat_fitness > self.best_fitness:
                self.best_fitness = neat_fitness
                path = os.path.join(self.winners_dir_path, "winner_temp.pkl")
                self.save_genome(genome, path)

            if neat_fitness >= 51.5:
                path = os.path.join(self.winners_dir_path, "winner_temp51_5.pkl")
                self.save_genome(genome, path)
            elif neat_fitness >= 51:
                path = os.path.join(self.winners_dir_path, "winner_temp51_0.pkl")
                self.save_genome(genome, path)
            elif neat_fitness >= 50.5:
                path = os.path.join(self.winners_dir_path, "winner_temp50_5.pkl")
                self.save_genome(genome, path)
            elif neat_fitness >= 50:
                path = os.path.join(self.winners_dir_path, "winner_temp50_0.pkl")
                self.save_genome(genome, path)
            elif neat_fitness >= 49.5:
                path = os.path.join(self.winners_dir_path, "winner_temp49_5.pkl")
                self.save_genome(genome, path)

            agents.pop()

    def play_games(self, games_to_play, agents, neat_agent):
        for _ in range(games_to_play):
            game = ge.AgentGame(
                run_game=False,
                agents=agents,
            )
            winner, rounds = game.run_game()
            self.tot_rounds_played += rounds
            self.tot_games_played += 1
            if winner and winner == neat_agent:
                neat_agent.wins += 1

        avg_neat_win_rate, avg_rounds = self.calculate_stats(neat_agent.wins)
        return avg_neat_win_rate, avg_rounds

    def calculate_stats(self, neat_agent_wins):
        avg_neat_win_rate = neat_agent_wins / self.tot_games_played
        avg_rounds = self.tot_rounds_played / self.tot_games_played
        return avg_neat_win_rate, avg_rounds

    def save_genome(self, genome, save_file_name):
        path = os.path.join(self.winners_dir_path, save_file_name)
        with open(path, "wb") as f:
            pickle.dump(genome, f)
            f.close()
