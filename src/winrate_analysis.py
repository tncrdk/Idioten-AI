from asyncore import write
import math
import ast
import csv
import statistics as stats
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom


class WinrateAnalysis:
    def neat_analysis(self, log_path: str, mode: str, agent1: str, agent2: str):
        if mode == "binomial":
            self.neat_binomial_analysis(log_path, agent1, agent2)
        elif mode == "groups":
            self.neat_groups_analysis(log_path, agent1, agent2)
        else:
            raise Exception("Den gitte modus er ikke en modus")

    def identical_agents_analysis(self, log_path: str, mode: str, agents_type: str):
        if mode == "binomial":
            self.identical_agents_binomial_analysis(log_path, agents_type)
        elif mode == "groups":
            self.identical_agents_groups_analysis(log_path, agents_type)
        else:
            raise Exception("Den gitte modus er ikke en modus")

    def neat_groups_analysis(self, log_path: str, agent1: str, agent2: str):
        results_file_path = r".\Results\{}_vs_{}_groups.csv".format(agent1, agent2)

        with open(log_path, "r") as f:
            winrates = []
            while True:
                data_str = f.readline().strip()  # Hver linje er en gruppe på 1000 spill
                if not data_str:
                    break
                datapoint = ast.literal_eval(data_str)
                wins = datapoint.get("NEAT_V3").get("wins")
                games = datapoint.get("NEAT_V3").get("games")
                winrates.append((wins / games))

        avg_winrate = np.average(winrates)
        stdev = stats.stdev(winrates)

        self.save_to_csv_file(
            results_file_path,
            [wins, avg_winrate, stdev],
            ["Wins", "Avg_winrate", "Stdev"],
        )
        print(f"Vinnrate: {avg_winrate}     Stdev: {stdev}")
        self.plot_group_winrates(winrates, avg_winrate, agent1, agent2)

    def neat_binomial_analysis(self, log_path: str, agent1: str, agent2: str):
        wins = 0
        games = 0
        winrates = []
        results_file_path = r".\Results\{}_vs_{}_binom.csv".format(agent1, agent2)

        with open(log_path, "r") as f:
            while True:
                data_str = f.readline().strip()
                if not data_str:
                    break
                datapoint = ast.literal_eval(data_str)
                wins += datapoint.get("NEAT_V3").get("wins")
                games += datapoint.get("NEAT_V3").get("games")
                winrates.append((wins / games))

        winrate = wins / games
        winrate_variance = winrate * (1 - winrate) * games  # V = n*p*(1-p)
        stdev = math.sqrt(winrate_variance)
        stdev_rel = stdev / games
        P_value = self.get_P_value(winrate, games, math.ceil(games / 2))

        print(f"Wins: {wins}    Winrate: {round(winrate, 6)}")
        print(f"Stdev: {round(stdev, 2)}   Stdev (rel): {round(stdev_rel, 6)}")
        print(f"P-value: {P_value}")

        self.save_to_csv_file(
            results_file_path,
            [wins, winrate, stdev, stdev_rel, P_value],
            ["Wins", "Winrate", "Stdev", "Relative Stdev", "P-value"],
        )
        self.plot_binomial_winrates(winrates, agent1, agent2)

    def identical_agents_binomial_analysis(self, log_path: str, agents: str):
        save_results_path = r".\Results\id_{}_binom.csv".format(agents)
        wins = 0
        games = 0
        winrates = []

        with open(log_path, "r") as f:
            while True:
                data_str = f.readline().strip()
                if not data_str:
                    break
                datapoint = ast.literal_eval(data_str)
                wins += datapoint.get("First").get("wins")
                games += datapoint.get("First").get("games")
                winrates.append((wins / games))

        winrate = wins / games
        winrate_variance = winrate * (1 - winrate) * games  # V = n*p*(1-p)
        stdev = math.sqrt(winrate_variance)
        stdev_rel = stdev / games
        P_value = 1 - self.get_P_value(winrate, games, math.ceil(games / 2))

        print(f"Wins: {wins}    Winrate: {round(winrate, 6)}")
        print(f"Stdev: {round(stdev, 2)}   Stdev (rel): {round(stdev_rel, 6)}")
        print(f"P-value: {P_value}")

        self.save_to_csv_file(
            save_results_path,
            [wins, winrate, stdev, stdev_rel, P_value],
            ["Wins", "Winrate", "Stdev", "Relative Stdev", "P-value"],
        )
        self.plot_binomial_winrates(winrates, agents, agents)

    def identical_agents_groups_analysis(self, log_path: str, agents_type):
        file_path = r".\Results\id_{}_groups.csv".format(agents_type)

        with open(log_path, "r") as f:
            winrates = []
            while True:
                data_str = f.readline().strip()  # Hver linje er en gruppe på 1000 spill
                if not data_str:
                    break
                datapoint = ast.literal_eval(data_str)
                wins = datapoint.get("First").get("wins")
                games = datapoint.get("First").get("games")
                winrates.append((wins / games))

        avg_winrate = np.average(winrates)
        stdev = stats.stdev(winrates)

        self.save_to_csv_file(
            file_path, [wins, avg_winrate, stdev], ["Wins", "Avg_winrate", "Stdev"]
        )
        print(f"Vinnrate: {avg_winrate}     Stdev: {stdev}")
        self.plot_group_winrates(winrates, avg_winrate, agents_type, agents_type)

    def plot_binomial_winrates(self, winrates: list[float], agent1, agent2):
        winrates = [100 * x for x in winrates]
        plt.plot(winrates, label="Gjennomsnittlig vinnrate")

        plt.title("Vinnrate-utvikling")
        plt.xlabel("Grupper analysert (1000 spill i hver gruppe)")
        plt.ylabel("Vinnrate (%)")
        plt.legend()

        plt.show()
        file_path = r".\Plots\binom_{}_vs_{}.png".format(agent1, agent2)
        plt.savefig(file_path)

    def plot_group_winrates(
        self, winrates: list[float], avg_winrate: float, agent1, agent2
    ):
        winrates = [100 * x for x in winrates]
        plt.plot(winrates, label="Gruppe-vinnrate")
        plt.plot(
            np.arange(0, len(winrates), 1),
            np.full(len(winrates), avg_winrate * 100),
            label="Gjennomsnitt",
        )

        plt.title("Vinnrate")
        plt.xlabel("Gruppe-nummer (1000 spill i hver gruppe)")
        plt.ylabel("Vinnrate (%)")
        plt.legend()

        plt.show()
        file_path = r".\Plots\groups_{}_vs_{}.png".format(agent1, agent2)
        plt.savefig(file_path)

    def save_to_csv_file(self, file_path: str, csv_data: list[int], headers: list[int]):
        with open(file_path, "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)
            writer.writerow(csv_data)

    @classmethod
    def get_P_value(cls, probability, population_size, criteria):
        p_value = 1 - binom.cdf(
            population_size - criteria - 1, population_size, probability
        )
        return p_value


if __name__ == "__main__":
    pass
