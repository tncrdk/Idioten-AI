from asyncore import write
import math
import ast
import csv
import statistics as stats
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom


class WinrateAnalysis:
    def neat_analysis(self, log_path: str, mode: str, first_player_name: str):
        if mode == "binomial":
            self.neat_binomial_analysis(log_path, first_player_name)
        elif mode == "groups":
            self.neat_groups_analysis(log_path, first_player_name)
        else:
            raise Exception("Den gitte modus er ikke en modus")

    def identical_agents_analysis(self, log_path: str, mode: str, agents_type: str):
        if mode == "binomial":
            self.identical_agents_binomial_analysis(log_path, agents_type)
        elif mode == "groups":
            self.identical_agents_groups_analysis(log_path, agents_type)
        else:
            raise Exception("Den gitte modus er ikke en modus")

    def neat_groups_analysis(self, log_path: str, first_player_name: str):
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
        file_path = r".\Results\{}_first_binomial_results.csv".format(first_player_name)

        self.save_to_csv_file(
            file_path, [wins, avg_winrate, stdev], ["Wins", "Avg_winrate", "Stdev"]
        )
        print(f"Vinnrate: {avg_winrate}     Stdev: {stdev}")
        self.plot_group_winrates(winrates, avg_winrate)

    def neat_binomial_analysis(self, log_path: str, first_player_name: str):
        wins = 0
        games = 0
        winrates = []

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

        file_path = r".\Results\{}_first_binomial_results.csv".format(first_player_name)
        self.save_to_csv_file(
            file_path,
            [wins, winrate, stdev, stdev_rel, P_value],
            ["Wins", "Winrate", "Stdev", "Relative Stdev", "P-value"],
        )
        self.plot_binomial_winrates(winrates)

    def identical_agents_binomial_analysis(self, log_path: str, agents_type: str):
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

        file_path = r".\Results\two_{}_binomial_results.csv".format(agents_type)
        self.save_to_csv_file(
            file_path,
            [wins, winrate, stdev, stdev_rel, P_value],
            ["Wins", "Winrate", "Stdev", "Relative Stdev", "P-value"],
        )
        self.plot_binomial_winrates(winrates)

    def identical_agents_groups_analysis(self, log_path: str, agents_type):
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
        file_path = r".\Results\two_{}_groups_results.csv".format(agents_type)

        self.save_to_csv_file(
            file_path, [wins, avg_winrate, stdev], ["Wins", "Avg_winrate", "Stdev"]
        )
        print(f"Vinnrate: {avg_winrate}     Stdev: {stdev}")
        self.plot_group_winrates(winrates, avg_winrate)

    def plot_binomial_winrates(self, winrates: list[float]):
        winrates = [100 * x for x in winrates]
        plt.plot(winrates, label="Gjennomsnittlig vinnrate")

        plt.title("Vinnrate-utvikling")
        plt.xlabel("Grupper analysert (1000 spill i hver gruppe)")
        plt.ylabel("Vinnrate (%)")
        plt.legend()

        plt.show()

    def plot_group_winrates(self, winrates: list[float], avg_winrate: float):
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
