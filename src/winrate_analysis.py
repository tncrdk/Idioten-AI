import math
import ast
import statistics as stats
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
                data_str = f.readline().strip()
                if not data_str:
                    break
                datapoint = ast.literal_eval(data_str)

                wins = datapoint["NEAT_V3"]["wins"]
                games = datapoint["NEAT_V3"]["games"]
                avg_winrate = wins / games
                winrates.append(avg_winrate)

        avg_winrate = np.average(winrates)
        self.plot_group_winrates(winrates, avg_winrate)
        standard_deviation = stats.stdev(winrates)

        print(avg_winrate, standard_deviation)
        return avg_winrate, standard_deviation

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
                wins += datapoint["NEAT_V3"]["wins"]
                games += datapoint["NEAT_V3"]["games"]

                winrates.append((wins / games))

        self.plot_binomial_winrates(winrates)
        winrate = wins / games
        variance_win_rate = winrate * (1 - winrate) * games  # V = npq  hvor q = 1-p
        std = math.sqrt(variance_win_rate)
        std_rel = std / games
        p_value = self.get_p_value(winrate, games, math.ceil(games / 2))

        print(f"Wins: {wins}    Winrate: {round(winrate, 6)}")
        print(f"Stdev: {round(std, 2)}   Stdev (rel): {round(std_rel, 6)}")
        print(f"P-value: {p_value}")

    def plot_binomial_winrates(self, winrates):
        winrates = [100 * x for x in winrates]
        plt.plot(winrates, label="Gjennomsnittlig vinnrate")
        plt.title("NEAT-agent vinn-rate")
        plt.xlabel("Antall sett med spill analysert (1000 i hver)")
        plt.ylabel("Vinnrate (%)")
        plt.legend()
        plt.show()

    def plot_group_winrates(self, winrates, avg_winrate):
        winrates = [100 * x for x in winrates]
        plt.plot(winrates, label="Sett-vinnrate")
        plt.plot(
            np.arange(0, len(winrates), 1),
            [avg_winrate * 100] * len(winrates),
            label="Gjennomsnittlig vinnrate",
        )
        plt.title("NEAT-agent vinn-rate")
        plt.xlabel("Antall sett (1000 spill i hvert sett)")
        plt.ylabel("Vinnrate (%)")
        plt.legend()
        plt.show()

    @classmethod
    def get_p_value(cls, probability, population_size, criteria):
        p_value = 1 - binom.cdf(
            population_size - criteria - 1, population_size, probability
        )
        return p_value


if __name__ == "__main__":
    pass
