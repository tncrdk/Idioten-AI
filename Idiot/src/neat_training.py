import import_files
import pickle
import neat
import static_agents as sa
import NEAT_agent as na
import game_engine as ge


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

        self.tot_games_played = 0
        self.tot_rounds_played = 0

    def train(self, save_file_name):
        winner_genome = self.population.run(self.eval_genomes)
        self.save_genome(winner_genome, save_file_name)

    def eval_genomes(self, genomes: neat.DefaultGenome, config: neat.Config):
        agents = [sa.PlayLowSaveAgent1()]
        best_fitness = 0
        for _, genome in genomes:
            self.tot_games_played = 0
            self.tot_rounds_played = 0
            GAMES_TO_PLAY = 100

            network = neat.nn.FeedForwardNetwork.create(genome, config)
            neat_agent = na.NEAT_Agent3(genome, network)
            agents.append(neat_agent)

            avg_neat_win_rate, avg_rounds = self.play_games(
                GAMES_TO_PLAY * 10, agents, neat_agent
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

            if neat_fitness > best_fitness:
                best_fitness = neat_fitness
                self.save_genome(genome, "Winners\winner_temp")

            if neat_fitness >= 51.5:
                self.save_genome(genome, "Winners\winner_temp51_5")
            elif neat_fitness >= 51:
                self.save_genome(genome, "Winners\winner_temp_51_0")
            elif neat_fitness >= 50.5:
                self.save_genome(genome, "Winners\winner_temp_50_5")
            elif neat_fitness >= 50:
                self.save_genome(genome, "Winners\winner_temp_50_0")
            elif neat_fitness >= 49.5:
                self.save_genome(genome, "Winners\winner_temp_49_5")

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

    def save_genome(self, genome, save_file_path):
        with open(save_file_path, "wb") as f:
            pickle.dump(genome, f)
            f.close()
