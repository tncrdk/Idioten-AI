import math
import ast
import statistics as stats
from unittest import result
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom


class WinRateAnalysis:
    def __init__(self, log_path: str) -> None:
        self.log_path = log_path

    def analyze(self, mode):
        if mode == "binomial":
            self.binomial_analysis()
        elif mode == "groups":
            self.groups_analysis()
        else:
            raise Exception("Det er ikke en modus")

    def groups_analysis(self):
        with open(self.log_path, "r") as f:
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
        standard_deviation = stats.stdev(winrates)

        print(f"Vinnrate: {avg_winrate}     Stdev: {standard_deviation}")
        self.plot_group_winrates(winrates, avg_winrate)

    def binomial_analysis(self):
        wins = 0
        games = 0
        winrates = []

        with open(self.log_path, "r") as f:
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
        self.plot_binomial_winrates(winrates)

    def plot_binomial_winrates(self, winrates):
        winrates = [100 * x for x in winrates]
        plt.plot(winrates, label="Gjennomsnitt")

        plt.title("NEAT-agent vinnrate")
        plt.xlabel("Grupper (1000 spill i hver gruppe)")
        plt.ylabel("Vinnrate (%)")
        plt.legend()

        plt.show()

    def plot_group_winrates(self, winrates, avg_winrate):
        winrates = [100 * x for x in winrates]
        plt.plot(winrates, label="Gruppe-vinnrate")
        plt.plot(
            np.arange(0, len(winrates), 1),
            np.full(len(winrates), avg_winrate * 100),
            label="Gjennomsnitt",
        )
        plt.title("NEAT-agent vinnrate")
        plt.xlabel("Gruppe-nummer (1000 spill i hver gruppe)")
        plt.ylabel("Vinnrate (%)")
        plt.legend()
        plt.show()

    @classmethod
    def get_P_value(cls, probability, population_size, criteria):
        p_value = 1 - binom.cdf(
            population_size - criteria - 1, population_size, probability
        )
        return p_value


if __name__ == "__main__":
    pass
